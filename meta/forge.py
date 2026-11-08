import asyncio
import hashlib
import io
import json
import re
import zipfile
from functools import cache

from .common import (MINECRAFT, PMC, STATIC, UPSTREAM, Coord, amap, check_mojang, get, get_json, iso, library, log,
                     prune, read, write, write_package, write_version)

FORGE = "net.minecraftforge"
DIR = UPSTREAM / "forge"
FILES_URL = "https://files.minecraftforge.net/net/minecraftforge/forge/"
MAVEN = "https://maven.minecraftforge.net/"
BAD_VERSIONS = {"1.12.2-14.23.5.2851"}

WRAPPER_MAIN = "io.github.zekerzhayard.forgewrapper.installer.Main"
BASE_ARGS = ("--username ${auth_player_name} --version ${version_name} --gameDir ${game_directory} "
             "--assetsDir ${assets_root} --assetIndex ${assets_index_name} --uuid ${auth_uuid} "
             "--accessToken ${auth_access_token} --userType ${user_type} --versionType ${version_type}")
WRAPPER = {
    "name": "io.github.zekerzhayard:ForgeWrapper:mmc6",
    "downloads": {"artifact": {
        "url": "https://polymc.github.io/files/maven/io/github/zekerzhayard/ForgeWrapper/mmc6/ForgeWrapper-mmc6.jar",
        "sha1": "8dfb7d1151a7260ecb7ab7c01ac362df80469261",
        "size": 28912,
    }},
}

LEGACY_MC = {
    "1.1", "1.2.3", "1.2.4", "1.2.5", "1.3.2", "1.4.1", "1.4.2", "1.4.3", "1.4.4", "1.4.5", "1.4.6", "1.4.7", "1.5",
    "1.5.1", "1.5.2", "1.6.1", "1.6.2", "1.6.3", "1.6.4", "1.7.10", "1.7.10-pre4", "1.7.2", "1.8", "1.8.8", "1.8.9",
    "1.9", "1.9.4", "1.10", "1.10.2", "1.11", "1.11.2", "1.12", "1.12.1", "1.12.2",
}
LEGACY_FML = {"1.3.2", "1.4", "1.4.1", "1.4.2", "1.4.3", "1.4.4", "1.4.5", "1.4.6", "1.4.7", "1.5", "1.5.1", "1.5.2"}

PROMO_RE = re.compile(r"(?P<mc>[^-]+)-(?P<promotion>latest|recommended)(-(?P<branch>[a-zA-Z0-9.]+))?")
VERSION_RE = re.compile(r"^(?P<mc>[0-9a-zA-Z_.]+)-(?P<ver>[0-9.]+\.(?P<build>[0-9]+))(-(?P<branch>[a-zA-Z0-9.]+))?$")
BAD_TZ_RE = re.compile(rb"([T ][0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]+)?)([+-])([0-9]):([0-9]{2})")


def artifact_url(entry: dict) -> tuple[bool, str | None]:
    installer = universal = None
    long = entry["longversion"]
    for cls, f in entry["files"].items():
        url = f"{MAVEN}net/minecraftforge/forge/{long}/forge-{long}-{cls}.{f['extension']}"
        if cls == "installer" and f["extension"] == "jar":
            installer = url
        if cls in ("universal", "client") and f["extension"] in ("jar", "zip"):
            universal = url
    uses_installer = installer is not None and entry["mcversion"] != "1.5.2"
    return uses_installer, installer if uses_installer else universal


async def files_manifest(http, long: str) -> dict:
    path = DIR / "files_manifests" / f"{long}.json"
    data = read(path) if path.exists() else await get_json(http, f"{FILES_URL}{long}/meta.json")
    files = {}
    for cls, exts in data["classifiers"].items():
        if not exts:
            continue
        ext, digest = list(exts.items())[-1]
        digest = re.sub(r"\W", "", digest) if isinstance(digest, str) else ""
        if len(digest) != 32:
            log(f"{long}: skipping invalid hash for {cls}")
            continue
        if len(exts) > 1:
            raise ValueError(f"{long}: multiple files for classifier {cls}")
        files[cls] = {"classifier": cls, "hash": digest, "extension": ext}
    if not path.exists():
        write(path, data)
    return files


def extract_installer(jar: bytes, long: str):
    profile = DIR / "installer_manifests" / f"{long}.json"
    if not profile.exists():
        with zipfile.ZipFile(io.BytesIO(jar)) as z:
            fix = lambda name: BAD_TZ_RE.sub(rb"\1\g<2>0\3:\4", z.read(name))
            if "version.json" in z.namelist():
                version = fix("version.json")
                check_mojang(json.loads(version))
                write(DIR / "version_manifests" / f"{long}.json", version)
            data = fix("install_profile.json")
            if not isinstance(json.loads(data), dict):
                raise ValueError(f"{long}: invalid install profile")
            write(profile, data)
    info = DIR / "installer_info" / f"{long}.json"
    if not info.exists():
        write(info, {"sha1hash": hashlib.sha1(jar).hexdigest(), "sha256hash": hashlib.sha256(jar).hexdigest(),
                     "size": len(jar)})


async def update(http):
    main, promos = await asyncio.gather(get_json(http, FILES_URL + "maven-metadata.json"),
                                        get_json(http, FILES_URL + "promotions_slim.json"))
    recommended = set()
    for key, short in promos["promos"].items():
        m = PROMO_RE.match(key)
        if not m:
            raise ValueError(f"Unparsable promotion {key}")
        if m["mc"] and not m["branch"] and m["promotion"] == "recommended":
            recommended.add(short)

    async def process(item):
        mc, long = item
        m = VERSION_RE.match(long)
        if not m or m["mc"] != mc:
            raise ValueError(f"Unparsable version {long}")
        entry = {"longversion": long, "mcversion": mc, "version": m["ver"], "build": int(m["build"]),
                 "branch": m["branch"], "latest": False, "recommended": m["ver"] in recommended,
                 "files": await files_manifest(http, long)}
        uses_installer, url = artifact_url(entry)
        if uses_installer and long not in BAD_VERSIONS and not all(
                (DIR / d / f"{long}.json").exists() for d in ("installer_manifests", "installer_info")):
            log(f"Downloading {url}")
            await asyncio.to_thread(extract_installer, (await get(http, url)).content, long)
        return entry

    entries = await amap(process, [(mc, long) for mc, longs in main.items() for long in longs])
    versions = {e["longversion"]: e for e in entries}
    by_mc = {}
    for e in entries:
        info = by_mc.setdefault(e["mcversion"], {"versions": []})
        info["versions"].append(e["longversion"])
        if e["recommended"]:
            info["recommended"] = e["longversion"]
    for info in by_mc.values():
        info["latest"] = info["versions"][-1]
        versions[info["latest"]]["latest"] = True

    write(DIR / "maven-metadata.json", main)
    write(DIR / "promotions_slim.json", promos)
    write(DIR / "derived_index.json", prune({"versions": versions, "by_mcversion": by_mc}))


def loose(version: str) -> list:
    return [int(x) if x.isdigit() else x for x in re.split(r"(\d+|[a-z]+|\.)", version) if x and x != "."]


@cache
def mc_libs(mc: str) -> tuple:
    return tuple(Coord.parse(lib["name"]) for lib in read(PMC / MINECRAFT / f"{mc}.json").get("libraries", []))


def ignored(c: Coord, mc: str) -> bool:
    if c.is_lwjgl or c.is_log4j:
        return True
    for m in mc_libs(mc):
        if (m.group, m.artifact, m.classifier) == (c.group, c.artifact, c.classifier):
            return m.version == c.version or loose(m.version) > loose(c.version)
    return False


def retarget(lib: dict, c: Coord):
    lib["name"] = str(c)
    lib["downloads"]["artifact"] |= {"path": c.path(), "url": MAVEN + c.path()}


def base(entry: dict, mc: str, release_time) -> dict:
    return {"formatVersion": 1, "name": "Forge", "uid": FORGE, "version": entry["version"], "order": 5,
            "requires": [{"uid": MINECRAFT, "equals": mc}], "releaseTime": release_time and iso(release_time)}


def tweakers(args: str) -> list | None:
    return re.findall(r"--tweakClass ([a-zA-Z0-9.]+)", args) or None


def from_profile(profile: dict, entry: dict) -> dict:
    info, mc = profile["versionInfo"], profile["install"]["minecraft"]
    v = base(entry, mc, info.get("time")) | {"mainClass": info.get("mainClass"),
                                             "+tweakers": tweakers(info["minecraftArguments"]), "libraries": []}
    for lib in info["libraries"]:
        c = Coord.parse(lib["name"])
        if ignored(c, mc):
            continue
        if c.group == FORGE and c.artifact == "minecraftforge":
            c.artifact, c.version, c.classifier = "forge", f"{mc}-{c.version}", "universal"
        elif c.group == FORGE and c.artifact == "forge":
            c.classifier = "universal"
        url = lib.get("url")
        v["libraries"].append({"name": str(c), "url": MAVEN if url == "http://maven.minecraftforge.net/" else url})
    return v


def from_modernized(installer: dict, entry: dict) -> dict:
    mc = entry["mcversion"]
    v = base(entry, mc, installer.get("releaseTime")) | {
        "mainClass": installer.get("mainClass"), "+tweakers": tweakers(installer["minecraftArguments"]), "libraries": []}
    for raw in installer["libraries"]:
        lib = library(raw, extra=False)
        c = Coord.parse(lib["name"])
        if ignored(c, mc):
            continue
        if c.group == FORGE and c.artifact in ("forge", "minecraftforge"):
            if c.artifact == "minecraftforge":
                c.artifact, c.version = "forge", f"{mc}-{c.version}"
            c.classifier = "universal"
            retarget(lib, c)
        v["libraries"].append(lib)
    return v


def from_build_system(installer: dict, profile: dict, entry: dict, mc: str) -> dict:
    long = entry["longversion"]
    info = read(DIR / "installer_info" / f"{long}.json")
    jar = Coord(FORGE, "forge", long, "installer")
    v = base(entry, mc, installer.get("releaseTime")) | {"mainClass": WRAPPER_MAIN, "libraries": [WRAPPER]}
    v["mavenFiles"] = [{"name": str(jar), "downloads": {"artifact": {
        "url": MAVEN + jar.path(), "sha1": info.get("sha1hash"), "size": info.get("size")}}}]

    for raw in profile.get("libraries") or []:
        lib = library(raw, extra=False)
        c = Coord.parse(lib["name"])
        if c.is_log4j:
            continue
        if (c.group, c.artifact, c.classifier) == (FORGE, "forge", "universal"):
            lib["downloads"]["artifact"]["url"] = MAVEN + c.path()
        v["mavenFiles"].append(lib)

    for raw in installer["libraries"]:
        lib = library(raw, extra=False)
        c = Coord.parse(lib["name"])
        if c.is_log4j:
            continue
        if c.group == FORGE:
            if c.artifact == "forge" and not c.classifier:
                c.classifier = "launcher"
                retarget(lib, c)
            if not lib["downloads"]["artifact"].get("url"):
                continue
        v["libraries"].append(lib)

    game = installer["arguments"]["game"]
    args = BASE_ARGS + "".join(f" {a}" for a in game)
    for flag, value in (("--fml.forgeGroup", FORGE), ("--fml.forgeVersion", entry["version"]),
                        ("--fml.mcVersion", entry["mcversion"])):
        if flag not in game:
            args += f" {flag} {value}"
    v["minecraftArguments"] = args
    return v


def from_legacy(info: dict, entry: dict, url: str, mc: str) -> dict:
    v = base(entry, mc, info.get("releaseTime"))
    if mc in LEGACY_FML:
        v["+traits"] = ["legacyFML"]
    cls = "universal" if "universal" in url else "client"
    v["jarMods"] = [{"name": f"{FORGE}:forge:{entry['longversion']}:{cls}", "downloads": {"artifact": {
        "url": url, "sha1": info.get("sha1"), "size": info.get("size")}}}]
    return v


def generate():
    index = read(DIR / "derived_index.json")
    legacy = read(STATIC / "forge/forge-legacyinfo.json")["number"]
    recommended = []
    for entry in index["versions"].values():
        long, mc = entry["longversion"], entry["mcversion"]
        uses_installer, url = artifact_url(entry)
        if long in BAD_VERSIONS or url is None or not entry["version"].split(".")[0].isnumeric():
            continue
        if entry.get("recommended"):
            recommended.append(entry["version"])
        sane = mc.replace("_pre", "-pre", 1)
        if not (PMC / MINECRAFT / f"{sane}.json").exists():
            log(f"Skipping Forge {long}: no Minecraft {sane}")
            continue

        manifest = DIR / "version_manifests" / f"{long}.json"
        profile = DIR / "installer_manifests" / f"{long}.json"
        if manifest.exists():
            installer = read(manifest)
            v = (from_modernized(installer, entry) if mc in LEGACY_MC
                 else from_build_system(installer, read(profile), entry, sane))
        elif uses_installer:
            if not profile.exists():
                log(f"Skipping Forge {long}: missing installer profile")
                continue
            v = from_profile(read(profile), entry)
        elif sane == "1.6.1" or str(entry["build"]) not in legacy:
            continue
        else:
            v = from_legacy(legacy[str(entry["build"])], entry, url, sane)
        write_version(v)

    write_package(FORGE, "Forge", recommended=sorted(recommended), projectUrl="https://www.minecraftforge.net/forum/")
