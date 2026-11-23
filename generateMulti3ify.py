"""Generate lwjgl3ify (1.7.10) and Cleanroom (1.12.2) profiles.

Ported from https://github.com/AngelicIndustries/multi3ify. Must run after
generateMojang.py and generateForge.py, and before index.py.

Each integration publishes three things:
- a Minecraft alias (1.7.10-lwjgl3ify / 1.12.2-cleanroom) whose payload version
  stays the vanilla version, so mod searches keep working,
- a dependency-only Forge bridge occupying the Forge slot,
- a dedicated runtime component with `latest` and pinned numbered versions.
All runtime libraries and Java requirements live in the runtime component, so
vanilla LWJGL 2 / Java 8 never mix with a modern runtime.
"""
import copy
import glob
import hashlib
import json
import os
import re
import shutil

from meta.common import polymc_path, upstream_path, static_path, ensure_component_dir
from meta.common.json import dumps
from meta.common.multi3ify import (
    LWJGL3IFY_DIR, LWJGL3IFY_UID, LWJGL3IFY_MC_VERSION, LWJGL3IFY_GAME_VERSION,
    BOOTSTRAP_CLASS, BOOTSTRAP_VERSION, BOOTSTRAP_GROUP_PATH, BOOTSTRAP_MAVEN_DIR,
    CLEANROOM_DIR, CLEANROOM_UID, CLEANROOM_MC_VERSION, CLEANROOM_GAME_VERSION, CLEANROOM_BRIDGE_VERSION,
    CLEANROOM_MAIN_CLASS, CLEANROOM_JAVA_NAMES, CLEANROOM_LWJGL2_LIBRARIES, PATCH_FIELDS,
)
from meta.model import MetaPackage

PMC_DIR = polymc_path()
UPSTREAM_DIR = upstream_path()
STATIC_DIR = static_path()


def write_json(uid, filename, document):
    ensure_component_dir(uid)
    path = os.path.join(PMC_DIR, uid, f"{filename}.json")
    with open(path, "w", encoding="utf-8") as f:
        f.write(dumps(document, indent=4, sort_keys=True))


def read_json(*parts):
    with open(os.path.join(*parts), encoding="utf-8") as f:
        return json.load(f)


def write_package(uid, name, description, project_url):
    ensure_component_dir(uid)
    MetaPackage(uid=uid, name=name, description=description, project_url=project_url,
                recommended=["latest"]).write(os.path.join(PMC_DIR, uid, "package.json"))


def load_profiles(directory, key):
    paths = glob.glob(os.path.join(UPSTREAM_DIR, directory, "*.json"))
    return sorted((read_json(p) for p in paths), key=lambda p: key(p["version"]), reverse=True)


def check_alias_free(uid, version):
    # Never overwrite a document produced by another generator.
    if os.path.exists(os.path.join(PMC_DIR, uid, f"{version}.json")):
        raise ValueError(f"Refusing to replace generated version {uid}/{version}")


def minecraft_alias(base, name, release_time, bridge_version):
    minecraft = copy.deepcopy(base)
    for key in ("libraries", "logging", "mainClass", "compatibleJavaMajors", "compatibleJavaName",
                "+jvmArgs", "+tweakers", "+traits"):
        minecraft.pop(key, None)
    minecraft.update({"name": name, "order": -2, "releaseTime": release_time,
                      "requires": [{"uid": "net.minecraftforge", "equals": bridge_version}]})
    return minecraft


def forge_bridge(version, name, game_version, runtime_uid, release_time):
    # No libraries here, so dependency insertion order cannot put vanilla Forge
    # ahead of the runtime component.
    return {"formatVersion": 1, "uid": "net.minecraftforge", "version": version, "name": name,
            "order": 5, "type": "release", "releaseTime": release_time,
            "requires": [{"uid": "net.minecraft", "equals": game_version},
                         {"uid": runtime_uid, "suggests": "latest"}]}


# lwjgl3ify

def lwjgl3ify_key(version):
    return tuple(map(int, version.split(".")))


def latest_forge_1710():
    versions = []
    for path in glob.glob(os.path.join(PMC_DIR, "net.minecraftforge", "*.json")):
        if os.path.basename(path) in ("index.json", "package.json"):
            continue
        document = read_json(path)
        if any(r.get("uid") == "net.minecraft" and r.get("equals") == LWJGL3IFY_GAME_VERSION
               for r in document.get("requires", [])) and re.fullmatch(r"[\d.]+", document["version"]):
            versions.append(document["version"])
    if not versions:
        raise ValueError("No generated Forge for Minecraft 1.7.10")
    return max(versions, key=lambda v: tuple(map(int, v.split("."))))


def bootstrap_library(base_url):
    """Publish the vendored helper under a content-addressed Maven version."""
    source = os.path.join(STATIC_DIR, "multi3ify", f"multi3ify-bootstrap-{BOOTSTRAP_VERSION}.jar")
    with open(source, "rb") as f:
        data = f.read()
    if hashlib.sha256(data).hexdigest()[:16] != BOOTSTRAP_VERSION:
        raise ValueError("Vendored multi3ify bootstrap checksum mismatch")
    relative = f"{BOOTSTRAP_MAVEN_DIR}/{BOOTSTRAP_GROUP_PATH}/{BOOTSTRAP_VERSION}/multi3ify-bootstrap-{BOOTSTRAP_VERSION}.jar"
    target = os.path.join(PMC_DIR, relative)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    shutil.copyfile(source, target)
    return {"name": f"io.github.jackofnonetrades:multi3ify-bootstrap:{BOOTSTRAP_VERSION}",
            "downloads": {"artifact": {"url": base_url.rstrip("/") + "/" + relative,
                                       "sha1": hashlib.sha1(data).hexdigest(), "size": len(data)}}}


def lwjgl3ify_document(profile, latest_forge, bootstrap):
    patches = profile["patches"]
    forge = next(p for p in patches if p["uid"] == "net.minecraftforge")
    minecraft = next(p for p in patches if p["uid"] == "net.minecraft")
    # forgePatches replaces classes in this exact Forge build: never mix builds.
    if forge["version"] != latest_forge:
        raise ValueError(f"lwjgl3ify {profile['version']} targets Forge {forge['version']}, "
                         f"but the latest generated 1.7.10 Forge is {latest_forge}")
    if minecraft["version"] != LWJGL3IFY_GAME_VERSION or any(j < 17 for j in minecraft["compatibleJavaMajors"]):
        raise ValueError("Unexpected upstream Minecraft/Java compatibility")
    for patch in patches:
        if set(patch) - PATCH_FIELDS:
            raise ValueError(f"Unrecognized upstream patch fields: {set(patch) - PATCH_FIELDS}")
    document = {"formatVersion": 1, "uid": LWJGL3IFY_UID, "version": profile["version"],
                "name": "lwjgl3ify", "order": 5, "volatile": True,
                "releaseTime": profile["releaseTime"], "type": "release",
                "requires": [{"uid": "net.minecraft", "equals": LWJGL3IFY_GAME_VERSION}],
                "mainClass": BOOTSTRAP_CLASS, "libraries": [], "+jvmArgs": [], "+tweakers": [], "+traits": [],
                "compatibleJavaMajors": minecraft["compatibleJavaMajors"],
                "compatibleJavaName": minecraft["compatibleJavaName"]}
    delegate = None
    for patch in patches:
        for key in ("libraries", "+jvmArgs", "+tweakers", "+traits"):
            document[key].extend(copy.deepcopy(patch.get(key, [])))
        delegate = patch.get("mainClass", delegate)
    if not delegate or not delegate.startswith("com.gtnewhorizons.retrofuturabootstrap."):
        raise ValueError("Unexpected upstream entry point")
    if any(lib.get("MMC-hint") == "local" for lib in document["libraries"]):
        raise ValueError("Unresolved local library in upstream profile")
    document["libraries"].append(copy.deepcopy(bootstrap))
    document["+jvmArgs"].extend([f"-Dmulti3ify.modUrl={profile['modUrl']}",
                                 f"-Dmulti3ify.modSha256={profile['modSha256']}",
                                 f"-Dmulti3ify.delegate={delegate}"])
    return document


def generate_lwjgl3ify():
    base_url = os.environ.get("META_BASE_URL")
    if not base_url:
        print("META_BASE_URL is not set; skipping lwjgl3ify (its helper jar needs a public URL)")
        return
    profiles = load_profiles(LWJGL3IFY_DIR, lwjgl3ify_key)
    if not profiles:
        print("No lwjgl3ify releases in upstream; skipping")
        return
    latest_forge = latest_forge_1710()
    bootstrap = bootstrap_library(base_url)
    documents = [lwjgl3ify_document(p, latest_forge, bootstrap) for p in profiles]
    latest = copy.deepcopy(documents[0])
    latest["version"] = "latest"
    release_time = profiles[0]["releaseTime"]
    # The bridge keeps multi3ify's ID, so instances moved from its feed match.
    bridge = forge_bridge(f"{latest_forge}-lwjgl3ify-latest", "Forge (lwjgl3ify)",
                          LWJGL3IFY_GAME_VERSION, LWJGL3IFY_UID, release_time)
    base = read_json(PMC_DIR, "net.minecraft", f"{LWJGL3IFY_GAME_VERSION}.json")
    minecraft = minecraft_alias(base, "Minecraft 1.7.10 + lwjgl3ify", release_time, bridge["version"])
    # multi3ify uses `suggests` for the 1.7.10 bridge.
    minecraft["requires"] = [{"uid": "net.minecraftforge", "suggests": bridge["version"]}]
    minecraft["order"] = base.get("order", -2)

    check_alias_free("net.minecraftforge", bridge["version"])
    check_alias_free("net.minecraft", LWJGL3IFY_MC_VERSION)
    for document in [latest, *documents]:
        write_json(LWJGL3IFY_UID, document["version"], document)
    write_package(LWJGL3IFY_UID, "lwjgl3ify", "LWJGL 3 and modern Java for Minecraft 1.7.10",
                  "https://github.com/GTNewHorizons/lwjgl3ify")
    write_json("net.minecraftforge", bridge["version"], bridge)
    write_json("net.minecraft", LWJGL3IFY_MC_VERSION, minecraft)
    print(f"Generated lwjgl3ify {', '.join(p['version'] for p in profiles)} (latest {profiles[0]['version']})")


# Cleanroom

def cleanroom_key(version):
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)(-alpha)?", version)
    if not match:
        raise ValueError(f"Unsupported Cleanroom version: {version}")
    return (*map(int, match.groups()[:3]), not bool(match[4]))


def validate_download(artifact):
    if (not artifact.get("url", "").startswith("https://")
            or not re.fullmatch(r"[a-f0-9]{40}", artifact.get("sha1", ""))
            or not isinstance(artifact.get("size"), int) or artifact["size"] <= 0):
        raise ValueError(f"Incomplete Cleanroom artifact: {artifact}")


def validate_library(library):
    if library.get("MMC-hint") == "local" or set(library) - {"name", "downloads", "rules", "natives", "extract"}:
        raise ValueError(f"Unsupported/local Cleanroom library: {library.get('name')}")
    downloads = library["downloads"]
    if set(downloads) - {"artifact", "classifiers"}:
        raise ValueError("Unknown Cleanroom download kind")
    # Cleanroom 0.7 splits ordinary jars and classifier-only native entries.
    if "artifact" in downloads:
        validate_download(downloads["artifact"])
    elif not library.get("natives"):
        raise ValueError("Cleanroom library has no artifact or natives")
    for artifact in downloads.get("classifiers", {}).values():
        validate_download(artifact)
    if any(c not in downloads.get("classifiers", {}) for c in library.get("natives", {}).values()):
        raise ValueError("Unresolved Cleanroom native classifier")


def cleanroom_components(profile):
    """Return LWJGL, Minecraft, loader, and the component owning Java settings."""
    patches = profile["patches"]
    if profile["modern"]:
        minecraft, lwjgl, loader = patches
        return lwjgl, minecraft, loader, loader
    lwjgl, minecraft, loader = patches
    return lwjgl, minecraft, loader, minecraft


def cleanroom_patches(profile, vanilla):
    """Rebuild the pack's component list, inheriting generated vanilla 1.12.2 on 0.7+."""
    profile = copy.deepcopy(profile)
    if not profile["modern"]:
        return profile
    minecraft = copy.deepcopy(vanilla)
    # Accept overrides of inherited Minecraft libraries, plus its omitted LWJGL 2 package.
    allowed = CLEANROOM_LWJGL2_LIBRARIES | {":".join(lib["name"].split(":")[:2]) for lib in minecraft["libraries"]}
    suppressed = set(profile["suppressedLibraries"])
    if suppressed - allowed:
        raise ValueError(f"Cleanroom overrides unknown libraries: {sorted(suppressed - allowed)}")
    minecraft["libraries"] = [lib for lib in minecraft["libraries"]
                              if ":".join(lib["name"].split(":")[:2]) not in suppressed]
    profile["patches"] = [minecraft, *profile["patches"]]
    return profile


def validate_cleanroom(profile):
    patches = profile["patches"]
    if [p["uid"] for p in patches] != profile["componentOrder"]:
        raise ValueError("Unexpected Cleanroom component layout/order")
    lwjgl, minecraft, loader, java = cleanroom_components(profile)
    modern = profile["modern"]
    for patch in patches:
        fields = PATCH_FIELDS | ({"logging"} if modern and patch is minecraft else set())
        if patch.get("formatVersion") != 1 or set(patch) - fields:
            raise ValueError(f"Unrecognized Cleanroom patch fields/format: {patch['uid']} {set(patch) - fields}")
        for library in patch["libraries"]:
            validate_library(library)
    if minecraft["version"] != CLEANROOM_GAME_VERSION or loader["version"] != profile["version"]:
        raise ValueError("Unexpected Cleanroom Minecraft/loader version")
    requirements = [{"uid": "net.minecraft", "equals": CLEANROOM_GAME_VERSION}]
    if modern:
        requirements.append({"uid": "org.lwjgl", "equals": lwjgl["version"]})
    if loader["requires"] != requirements:
        raise ValueError("Unexpected Cleanroom loader requirements")
    if (len(minecraft["requires"]) != 1 or minecraft["requires"][0]["uid"] != lwjgl["uid"]
            or lwjgl.get("requires")):
        raise ValueError("Unexpected Cleanroom runtime requirements")
    if (loader["mainClass"] != CLEANROOM_MAIN_CLASS
            or loader["+tweakers"] != ["net.minecraftforge.fml.common.launcher.FMLTweaker"]):
        raise ValueError("Unsupported Cleanroom entry point")
    majors = java["compatibleJavaMajors"]
    if not majors or any(type(j) is not int or j < 25 for j in majors) or majors[0] not in CLEANROOM_JAVA_NAMES:
        raise ValueError("Unsupported Cleanroom Java compatibility")
    for patch in (lwjgl, loader):
        fields = {"mainJar", "assetIndex", "minecraftArguments"}
        if patch is not java:
            fields |= {"compatibleJavaMajors", "compatibleJavaName"}
        if fields & patch.keys():
            raise ValueError("Cleanroom moved game/Java fields between components")
    validate_download(minecraft["mainJar"]["downloads"]["artifact"])
    validate_download(minecraft["assetIndex"])
    libraries = [lib for patch in patches for lib in patch["libraries"]]
    if any(lib["name"].startswith(("net.minecraftforge:forge:", "net.minecraft:launchwrapper:",
                                   "org.lwjgl.lwjgl:", "org.ow2.asm:asm-all:")) for lib in libraries):
        raise ValueError("Obsolete runtime in Cleanroom profile")
    lwjgl_libraries = [lib for lib in libraries if lib["name"].startswith("org.lwjgl:")]
    # Upstream supplies a patched core module named <version>-unsafe.
    if not lwjgl_libraries or any(
        lib["name"].split(":")[2] != lwjgl["version"]
        and lib["name"] != f"org.lwjgl:lwjgl:{lwjgl['version']}-unsafe" for lib in lwjgl_libraries
    ):
        raise ValueError("Mismatched Cleanroom LWJGL versions")


def cleanroom_documents(profile):
    validate_cleanroom(profile)
    _, game, _, java_settings = cleanroom_components(profile)
    majors = java_settings["compatibleJavaMajors"]
    runtime = {"formatVersion": 1, "uid": CLEANROOM_UID, "version": profile["version"],
               "name": "Cleanroom", "order": 5, "volatile": True, "type": "release",
               "releaseTime": profile["releaseTime"],
               "requires": [{"uid": "net.minecraft", "equals": CLEANROOM_GAME_VERSION}],
               "compatibleJavaMajors": majors, "compatibleJavaName": CLEANROOM_JAVA_NAMES[majors[0]]}
    for field in ("libraries", "+jvmArgs", "+tweakers", "+traits"):
        runtime[field] = [copy.deepcopy(v) for patch in profile["patches"] for v in patch.get(field, [])]
    runtime["mainClass"] = CLEANROOM_MAIN_CLASS
    # The vanilla logging configuration targets its old Log4j runtime; leave
    # logging to Cleanroom's own configuration.
    minecraft = minecraft_alias(game, "Minecraft 1.12.2 + Cleanroom", profile["releaseTime"],
                                CLEANROOM_BRIDGE_VERSION)
    return minecraft, runtime


def generate_cleanroom():
    profiles = load_profiles(CLEANROOM_DIR, cleanroom_key)
    if not profiles:
        print("No Cleanroom releases in upstream; skipping")
        return
    vanilla = read_json(PMC_DIR, "net.minecraft", f"{CLEANROOM_GAME_VERSION}.json")
    runtimes = []
    base = None
    for stored in profiles:
        minecraft, runtime = cleanroom_documents(cleanroom_patches(stored, vanilla))
        # Assets/game arguments belong to the shared Minecraft alias. Refuse a
        # release that would change these for users pinned to an older runtime.
        game = {k: v for k, v in minecraft.items() if k != "releaseTime"}
        if base is not None and game != base:
            raise ValueError(f"Cleanroom {stored['version']} disagrees on base Minecraft metadata")
        base = game
        runtimes.append(runtime)
    latest = copy.deepcopy(runtimes[0])
    latest["version"] = "latest"
    minecraft, _ = cleanroom_documents(cleanroom_patches(profiles[0], vanilla))
    bridge = forge_bridge(CLEANROOM_BRIDGE_VERSION, "Forge (Cleanroom)", CLEANROOM_GAME_VERSION,
                          CLEANROOM_UID, profiles[0]["releaseTime"])

    check_alias_free("net.minecraftforge", bridge["version"])
    check_alias_free("net.minecraft", CLEANROOM_MC_VERSION)
    for document in [latest, *runtimes]:
        write_json(CLEANROOM_UID, document["version"], document)
    write_package(CLEANROOM_UID, "Cleanroom", "Forge replacement for Minecraft 1.12.2 with modern Java and LWJGL 3",
                  "https://github.com/CleanroomMC/Cleanroom")
    write_json("net.minecraftforge", bridge["version"], bridge)
    write_json("net.minecraft", CLEANROOM_MC_VERSION, minecraft)
    print(f"Generated Cleanroom {', '.join(p['version'] for p in profiles)} (latest {profiles[0]['version']})")


def main():
    # Remove stale output so a reprocessed run can't trip the overwrite guards.
    for uid, version in (("net.minecraft", LWJGL3IFY_MC_VERSION), ("net.minecraft", CLEANROOM_MC_VERSION),
                         ("net.minecraftforge", CLEANROOM_BRIDGE_VERSION)):
        path = os.path.join(PMC_DIR, uid, f"{version}.json")
        if os.path.exists(path):
            os.remove(path)
    for path in glob.glob(os.path.join(PMC_DIR, "net.minecraftforge", "*-lwjgl3ify-latest.json")):
        os.remove(path)
    generate_lwjgl3ify()
    generate_cleanroom()


if __name__ == "__main__":
    main()
