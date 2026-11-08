import asyncio
import hashlib
import io
import itertools
import zipfile

from .common import MINECRAFT, PMC, UPSTREAM, Coord, amap, get_json, iso, log, read, write, write_package, write_version
from .forge import BASE_ARGS, WRAPPER_MAIN

NEOFORGE = "net.neoforged.neoforge"
DIR = UPSTREAM / "neoforge"
INDEX = DIR / "derived_index.json"
API = "https://maven.neoforged.net/api/maven/"
BAD_VERSIONS = {"1.20.1-47.1.7", "47.1.82"}
WRAPPER = {
    "name": "io.github.zekerzhayard:ForgeWrapper:mmc7",
    "downloads": {"artifact": {
        "url": "https://github.com/MultiMC/ForgeWrapper/releases/download/mmc7/ForgeWrapper-mmc7.jar",
        "sha1": "0c99747406998c933be78a368dfd8386949d1935",
        "size": 29346,
    }},
}


def mc_version(version: str) -> str:
    major = int(version.split(".")[0])
    parts = [p.split("-")[0] for p in version.split(".")]
    if major >= 26:
        return ".".join(p for p in parts[:3] if p != "0")
    return "1." + ".".join(p for p in parts[:2] if p != "0")


def is_forge(entry: dict) -> bool:
    return entry["mc_version"] == "1.20.1"


def sane_version(entry: dict) -> str:
    return entry["version"].split("-")[1] if is_forge(entry) else entry["version"]


def installer_url(entry: dict) -> str:
    loader, v = "forge" if is_forge(entry) else "neoforge", entry["version"]
    return f"https://maven.neoforged.net/releases/net/neoforged/{loader}/{v}/{loader}-{v}-installer.jar"


def extract(jar: bytes, sane: str):
    with zipfile.ZipFile(io.BytesIO(jar)) as z:
        version, profile = z.read("version.json"), z.read("install_profile.json")
    write(DIR / "version_manifests" / f"{sane}.json", version)
    write(DIR / "installer_manifests" / f"{sane}.json", profile)


async def update(http):
    try:
        cached = {e["version"]: e for e in read(INDEX)}
    except (OSError, ValueError):
        cached = {}
    neo, forge = await asyncio.gather(get_json(http, API + "versions/releases/net/neoforged/neoforge"),
                                      get_json(http, API + "versions/releases/net/neoforged/forge"))
    by_mc = {k: list(g) for k, g in itertools.groupby(sorted(neo["versions"], key=mc_version), mc_version)}
    by_mc["1.20.1"] = [v for v in forge["versions"] if v not in BAD_VERSIONS]
    latest = {versions[-1] for versions in by_mc.values()}

    async def process(entry):
        sane = sane_version(entry)
        old = cached.get(entry["version"])
        if old and (DIR / "installer_manifests" / f"{sane}.json").exists():
            return entry | {"installer_sha1": old["installer_sha1"], "installer_size": old["installer_size"]}
        if is_forge(entry):
            r = await http.get(f"{API}details/releases/net/neoforged/forge/{entry['version']}")
            if not r.is_success or "files" not in r.json():
                return None
        log(f"Downloading {installer_url(entry)}")
        r = await http.get(installer_url(entry))
        if not r.is_success:
            log(f"Skipping NeoForge {entry['version']}: installer download failed ({r.status_code})")
            return None
        sha1 = hashlib.sha1(r.content).hexdigest()
        if not is_forge(entry):
            expected = await http.get(installer_url(entry) + ".sha1")
            if not expected.is_success or expected.text.strip() != sha1:
                log(f"Skipping NeoForge {entry['version']}: installer hash missing or wrong")
                return None
        try:
            await asyncio.to_thread(extract, r.content, sane)
        except KeyError as e:
            log(f"Skipping NeoForge {entry['version']}: {e}")
            return None
        return entry | {"installer_sha1": sha1, "installer_size": len(r.content)}

    entries = [{"version": v, "mc_version": mc, "latest": v in latest, "installer_sha1": None, "installer_size": None}
               for mc, versions in by_mc.items() for v in versions]
    write(INDEX, [e for e in await amap(process, entries) if e])


def slim(lib: dict) -> dict:
    a = (lib.get("downloads") or {}).get("artifact")
    return {"name": str(Coord.parse(lib["name"])), "downloads": a and {"artifact": {
        "url": a["url"], "sha1": a.get("sha1") or None, "size": a.get("size"), "path": a.get("path") or None}}}


def version(installer: dict, profile: dict, entry: dict) -> dict:
    loader = "forge" if is_forge(entry) else "neoforge"
    return {
        "formatVersion": 1,
        "name": "NeoForge",
        "uid": NEOFORGE,
        "version": sane_version(entry),
        "requires": [{"uid": MINECRAFT, "equals": entry["mc_version"]}],
        "mainClass": WRAPPER_MAIN,
        "mavenFiles": [{"name": f"net.neoforged:{loader}:{entry['version']}:installer", "downloads": {"artifact": {
            "url": installer_url(entry), "sha1": entry["installer_sha1"] or None, "size": entry["installer_size"]}}},
            *(slim(lib) for lib in profile["libraries"] if not Coord.parse(lib["name"]).is_log4j)],
        "libraries": [WRAPPER, *(slim(lib) for lib in installer["libraries"] if not Coord.parse(lib["name"]).is_log4j)],
        "order": 5,
        "releaseTime": iso(installer["releaseTime"]),
        "minecraftArguments": BASE_ARGS + "".join(f" {a}" for a in installer["arguments"]["game"]),
    }


def generate():
    recommended = []
    for entry in read(INDEX):
        sane = sane_version(entry)
        if not (PMC / MINECRAFT / f"{entry['mc_version']}.json").exists():
            log(f"Skipping NeoForge {sane}: no Minecraft {entry['mc_version']}")
            continue
        if entry["latest"]:
            recommended.append(sane)
        profile = DIR / "installer_manifests" / f"{sane}.json"
        if not profile.exists():
            log(f"Skipping NeoForge {sane}: missing installer profile")
            continue
        write_version(version(read(DIR / "version_manifests" / f"{sane}.json"), read(profile), entry))
    write_package(NEOFORGE, "NeoForge", recommended=sorted(recommended), projectUrl="https://neoforged.net/")
