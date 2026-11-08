import asyncio
import copy
import hashlib
import io
import json
import re
import zipfile
from collections import defaultdict
from datetime import datetime

from .common import (MINECRAFT, STATIC, UPSTREAM, Coord, amap, check_mojang, get, get_json, iso, library, log,
                     prune, read, write, write_package, write_version)

LWJGL = "org.lwjgl"
LWJGL3 = "org.lwjgl3"
MANIFEST_URL = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
MANIFEST = UPSTREAM / "mojang/version_manifest_v2.json"
VERSIONS = UPSTREAM / "mojang/versions"
POLYMC_MAVEN = "https://polymc.github.io/files/maven/"

COMPATIBLE_JAVA = {16: [17, 18, 19, 20, 21], 17: [18, 19, 20, 21]}
IGNORED_GAME_ARGS = {"--clientId", "${clientid}", "--xuid", "${auth_xuid}"}

LOG4J = {
    "2.0-beta9-fixed": {
        "log4j-api": ("b61eaf2e64d8b0277e188262a8b771bbfa1502b3", 107347),
        "log4j-core": ("677991ea2d7426f76309a73739cecf609679492c", 677588),
    },
    "2.17.1": {
        "log4j-api": ("d771af8e336e372fb5399c99edabe0919aeaf5b2", 301872),
        "log4j-core": ("779f60f3844dadc3ef597976fcb1e5127b1f343d", 1790452),
        "log4j-slf4j18-impl": ("ca499d751f4ddd8afb016ef698c30be0da1d09f7", 21268),
    },
}

# Variants of each LWJGL version, identified by hash. Exactly one must pass for every version.
PASS_VARIANTS = {
    "40ee0dc8739c4539b51df3a92386941bd1d9d911",  # 3.4.3 (2026-09-01 11:29:01+00:00)
    "fd17e8d3473d57ff4141a36cbfcfabade5fbb7c5",  # 3.4.2 (2026-07-21 11:45:42+00:00)
    "317adbdf3b02845f7240549bb4aaa5fcd1344c49",  # 3.4.1, but with SDL
    "2b00f31688148fc95dbc8c8ef37308942cf0dce0",  # 3.3.6
    "6f32ef730d05562ede7db0b845b72ea16dd239d5",  # 3.3.3 (2024-05-29 12:04:43+00:00)
    "765b4ab443051d286bdbb1c19cd7dc86b0792dce",  # 3.3.2 (2024-01-17 13:19:20+00:00)
    "54c4fb1d6a96ac3007c947bf310c8bcf94a862be",  # 3.3.1 (2023-04-20 11:55:19+00:00) split natives, with WoA natives
    "ea4973ebc9eadf059f30f0958c89f330898bff51",  # 3.2.2 (2019-07-04 14:41:05+00:00) will be patched, missing tinyfd
    "235fc413bc4c76b269c207f7bca6464f1e1f1d80",  # 3.2.1 (2019-02-13 16:12:08+00:00)
    "deb1a436d806413207350735a00e04b54d113916",  # 3.1.6 (2018-10-18 14:46:12+00:00)
    "3e47f0f742fb759401754769fa59c508fd8fda75",  # 3.1.2 (2018-06-21 12:57:11+00:00)
    "a3f254df5a63a0a1635755733022029e8cfae1b3",  # 2.9.4-nightly-20150209 (2016-12-20 14:05:34+00:00)
    "879be09c0bd0d4bafc2ea4ea3d2ab8607a0d976c",  # 2.9.3 (2015-01-30 11:58:24+00:00)
    "8d4951d00253dfaa36a0faf1c8be541431861c30",  # 2.9.1 (2014-05-22 14:44:33+00:00)
    "cf58c9f92fed06cb041a7244c6b4b667e6d544cc",  # 2.9.1-nightly-20131120 (2013-12-06 13:55:34+00:00)
    "27dcadcba29a1a7127880ca1a77efa9ece866f24",  # 2.9.0 (2013-09-06 12:31:58+00:00)
}

BAD_VARIANTS = {
    "02a9f886ad37d391d2b34a08800e8bd852b92059",  # 3.4.3 (2026-09-11 10:34:40+00:00), no spng
    "b510ab8669cd8b031298f171aa810c7d3e7acb8f",  # 3.4.3 (2026-08-25 12:53:43+00:00), no spng
    "17754e4d1045947c3b99d22b9db7e75bfb6d252a",  # 3.4.2 (2026-08-17 11:46:16+00:00), doesn't launch
    "0ab5c885c21dfd8133277e8f557839f5fab35311",  # 3.4.1, but without SDL
    "472ee33f7a1294822aa2d617cd6ccdfd92f949a0",  # 3.4.1, marked as bad by Mojang
    "1fd0e4d1f0f7c97e8765a69d38225e1f27ee14ef",  # 3.4.1, but without Vulkan
    "73974b3af2afeb5b272ffbadcd7963014387c84f",  # 3.3.3 (2024-05-15 12:00:35+00:00)
    "8a9b08f11271eb4de3b50e5d069949500b2c7bc1",  # 3.3.3 (2024-04-16 11:57:30+00:00)
    "79bde9e46e9ad9accebda11e8293ed08d80dbdc3",  # 3.3.2 (2023-09-05 12:06:20+00:00)
    "8836c419f90f69a278b97d945a34af165c24ff60",  # 3.3.1 (2022-05-18 13:51:54+00:00) split natives, with workaround, replaced by 23w26a
    "3c624b94c06dbc4abae08fe6156d74abe4a2cca5",  # 3.3.1 (2022-05-04 14:41:35+00:00) we already have a nice 3.3.1
    "e1106ca765798218323b7a6d7528050260ea9d88",  # 3.3.1 (2022-05-04 14:41:35+00:00) doesn't use split natives
    "90b3d9ca01058286c033b6b7ae7f6dc370a04015",  # 3.2.2 (2022-03-31 14:53:25+00:00) only linux, windows
    "d986df9598fa2bcf4a5baab5edf044548e66d011",  # 3.2.2 (2021-12-10 03:36:38+00:00) only linux, windows
    "4b73fccb9e5264c2068bdbc26f9651429abbf21a",  # 3.2.2 (2021-08-25 14:41:57+00:00) only linux, windows
    "090cec3577ecfe438b890b2a9410ea07aa725e16",  # 3.2.2 (2021-04-07 14:04:09+00:00) only linux, windows
    "ab463e9ebc6a36abf22f2aa27b219dd372ff5069",  # 3.2.2 (2019-08-13 07:33:42+00:00) only linux, windows
    "51d8ff5a7efc949b4ad2088930e151d6b88ba616",  # 3.2.2 (2019-07-19 09:25:47+00:00) only linux, windows
    "854649a5bd1455b89117593ae82ff90c8132cacf",  # 3.2.1 (2019-04-18 11:05:19+00:00) only osx, windows
    "89fcb489261b05f622e8052fe0b588b0cfe49c24",  # 3.1.6 (2019-04-18 11:05:19+00:00) only linux
    "f04052162b50fa1433f67e1a90bc79466c4ab776",  # 2.9.0 (2013-10-21 16:34:47+00:00) only linux, windows
    "6442fc475f501fbd0fc4244fd1c38c02d9ebaf7e",  # 2.9.0 (2011-03-30 22:00:00+00:00) fine but newer variant available
}


async def update(http):
    remote = await get_json(http, MANIFEST_URL)
    local = {v["id"]: v for v in read(MANIFEST)["versions"]} if MANIFEST.exists() else {}
    pending = [
        v for v in remote["versions"]
        if v["id"] not in local or datetime.fromisoformat(v["time"]) > datetime.fromisoformat(local[v["id"]]["time"])
    ]

    async def fetch(v):
        log(f"Updating Minecraft {v['id']}")
        write(VERSIONS / f"{v['id']}.json", await get_json(http, v["url"]))

    async def fetch_experiment(e):
        path = VERSIONS / f"{e['id']}.json"
        if path.exists():
            return
        log(f"Updating experiment {e['id']}")
        with zipfile.ZipFile(io.BytesIO((await get(http, e["url"])).content)) as z:
            write(path, json.loads(z.read(next(n for n in z.namelist() if n.endswith(".json")))))

    experiments = read(STATIC / "mojang/minecraft-experiments.json")["experiments"]
    await asyncio.gather(amap(fetch, pending), amap(fetch_experiment, experiments))

    fields = ("id", "releaseTime", "time", "type", "url", "sha1", "complianceLevel")
    write(MANIFEST, prune({
        "latest": {"release": remote["latest"]["release"], "snapshot": remote["latest"]["snapshot"]},
        "versions": [
            {k: iso(v[k]) if k in ("releaseTime", "time") and v.get(k) else v.get(k) for k in fields}
            for v in remote["versions"]
        ],
    }))


def release_key(version: str):
    m = re.match(r"(\d+(?:\.\d+)*)(.*)", version)
    nums = [int(x) for x in m[1].split(".")]
    while nums and nums[-1] == 0:
        nums.pop()
    return tuple(nums), not m[2]


def uniq(libs: list) -> list:
    seen = {}
    for lib in libs:
        seen.setdefault(json.dumps(lib, sort_keys=True), lib)
    return list(seen.values())


def merge(ours: dict, theirs: dict):
    for k, v in copy.deepcopy(theirs).items():
        cur = ours.get(k)
        if cur is None:
            ours[k] = v
        elif isinstance(cur, list):
            ours[k] = cur + v
        elif isinstance(cur, dict):
            ours[k] = cur | v if k in ("natives", "classifiers") else merge(cur, v)
        else:
            ours[k] = v
    return ours


def load_patches() -> list:
    return [
        {
            "match": {str(Coord.parse(m)) for m in p["match"]},
            "override": p.get("override") and library(p["override"]),
            "additional": [library(lib) for lib in p.get("additionalLibraries") or []],
            "recurse": p.get("patchAdditionalLibraries", False),
        }
        for p in read(STATIC / "mojang/library-patches.json")
    ]


def patch_library(lib: dict, patches: list) -> list:
    queue, added = [lib], []
    while queue:
        target = queue.pop(0)
        for p in patches:
            if target.get("name") not in p["match"]:
                continue
            if p["override"]:
                merge(target, p["override"])
            if p["additional"]:
                extra = copy.deepcopy(p["additional"])
                added += uniq(extra)
                if p["recurse"]:
                    queue += extra
    return added


def to_meta(mv: dict) -> dict:
    level = mv.get("complianceLevel")
    if level and level != 1:
        raise ValueError(f"Unsupported compliance level {level}")
    major = (mv.get("javaVersion") or {}).get("majorVersion", 8)
    client, assets = mv["downloads"]["client"], mv.get("assetIndex")
    return prune({
        "formatVersion": 1,
        "name": "Minecraft",
        "uid": MINECRAFT,
        "version": mv["id"],
        "type": "experiment" if mv.get("type") == "pending" else mv.get("type"),
        "assetIndex": assets and {
            **{k: assets.get(k) for k in ("id", "sha1", "size", "totalSize")},
            "url": assets["url"].replace("://launchermeta.mojang.com/", "://piston-meta.mojang.com/", 1),
        },
        "libraries": [library(lib, extra=False) for lib in mv["libraries"]],
        "mainClass": mv.get("mainClass"),
        "minecraftArguments": mv.get("minecraftArguments"),
        "releaseTime": mv.get("releaseTime") and iso(mv["releaseTime"]),
        "compatibleJavaMajors": [major, *COMPATIBLE_JAVA.get(major, [])],
        "+traits": ["XR:Initial"] if level == 1 else None,
        "mainJar": {
            "name": f"com.mojang:minecraft:{mv['id']}:client",
            "downloads": {"artifact": {k: client.get(k) for k in ("sha1", "size", "url")}},
        },
    })


def macos_only(rules) -> bool:
    if not rules:
        return False
    osx = any(r["action"] == "allow" and (r.get("os") or {}).get("name") == "osx" for r in rules)
    everywhere = any(r["action"] == "allow" and not r.get("os") for r in rules)
    return osx and not everywhere


def add_variant(variants: dict, bucket: dict):
    b = copy.deepcopy(bucket)
    b["libraries"].sort(key=lambda lib: lib["name"])
    digest = hashlib.sha1(json.dumps(prune({**b, "releaseTime": None}), indent=4, sort_keys=True).encode()).hexdigest()
    if all(digest != d for d, _ in variants[b["version"]]):
        log(f"New variant for LWJGL {b['version']}")
        variants[b["version"]].append((digest, b))


def minecraft(mv: dict, overrides: dict, patches: list, variants: dict) -> bool:
    check_mojang(mv)
    v = to_meta(mv)
    split = any((Coord.parse(lib["name"]).classifier or "").startswith("natives-") for lib in v["libraries"])
    libs, extra, buckets, lwjgl3 = [], [], {}, False

    for lib in v["libraries"]:
        c = Coord.parse(lib["name"])
        dl = lib.get("downloads", {})
        for a in ([dl["artifact"]] if "artifact" in dl else []) + list(dl.get("classifiers", {}).values()):
            a.pop("path", None)
        if c.classifier and c.classifier.startswith("natives-"):
            c.artifact, c.classifier = f"{c.artifact}-{c.classifier}", None
            lib["name"] = str(c)

        if c.is_lwjgl:
            if split:
                key = None
                lwjgl3 = True
            else:
                rules = lib.pop("rules", None)
                if macos_only(rules):
                    log(f"Ignoring macOS-only {c}")
                    continue
                key = None if rules is None else json.dumps(rules, sort_keys=True)
            bucket = buckets.setdefault(key, {
                "formatVersion": 1, "name": "LWJGL", "version": "undetermined", "uid": LWJGL, "type": "release",
                "libraries": [],
            })
            if split or (c.group, c.artifact) in (("org.lwjgl.lwjgl", "lwjgl"), ("org.lwjgl", "lwjgl")):
                bucket["version"] = c.version
            if not split and (c.group, c.artifact) == ("org.lwjgl", "lwjgl"):
                lwjgl3 = True
            bucket["libraries"].append(lib)
            bucket["releaseTime"] = v.get("releaseTime")
        elif c.is_log4j:
            if release_key(c.version) <= release_key("2.0"):
                ver, maven = "2.0-beta9-fixed", POLYMC_MAVEN
            elif release_key(c.version) <= release_key("2.17.1"):
                ver, maven = "2.17.1", "https://repo1.maven.org/maven2/"
            else:
                libs.append(lib)
                continue
            sha1, size = LOG4J[ver][c.artifact]
            name = Coord(c.group, c.artifact, ver)
            libs.append({"name": str(name), "downloads": {"artifact": {"url": maven + name.path(), "sha1": sha1, "size": size}}})
        else:
            extra += patch_library(lib, patches)
            libs.append(lib)

    if len(buckets) == 1:
        add_variant(variants, next(iter(buckets.values())))
    else:
        common = buckets.pop(None, None)
        for b in buckets.values():
            if common:
                b["libraries"] = b["libraries"] + common["libraries"]
            add_variant(variants, b)

    dep = {"uid": LWJGL3 if lwjgl3 else LWJGL}
    if len(buckets) == 1:
        dep["suggests"] = next(iter(buckets.values()))["version"] if lwjgl3 else "2.9.4-nightly-20150209"
    elif {b["version"] for b in buckets.values()} == {"3.1.6", "3.2.1"}:
        dep["suggests"] = "3.2.1"
    else:
        raise ValueError(f"Cannot determine a single LWJGL version for {mv['id']}")

    if lwjgl3:
        v.setdefault("+traits", []).append("FirstThreadOnMacOS")
    v["libraries"] = libs + uniq(extra)
    v["requires"] = [dep]
    v["order"] = -2
    if not mv.get("minecraftArguments") and mv.get("arguments"):
        game = mv["arguments"].get("game") or []
        v["minecraftArguments"] = " ".join(a for a in game if isinstance(a, str) and a not in IGNORED_GAME_ARGS)
    if v["version"] in overrides:
        o = overrides[v["version"]]
        v["mainClass"], v["appletClass"] = o.get("mainClass"), o.get("appletClass")
        if o.get("releaseTime"):
            v["releaseTime"] = iso(o["releaseTime"])
        if o.get("+traits"):
            v.setdefault("+traits", []).extend(o["+traits"])
        v["libraries"] = v["minecraftArguments"] = None
    write_version(v)
    return lwjgl3


def write_lwjgl(variant: dict, patches: list):
    v = copy.deepcopy(variant)
    added = []
    for lib in v["libraries"]:
        added += patch_library(lib, patches)
    v["libraries"] += uniq(added)

    match v["version"][0]:
        case "2":
            v |= {"name": "LWJGL 2", "uid": LWJGL, "conflicts": [{"uid": LWJGL3}]}
        case "3":
            v |= {"name": "LWJGL 3", "uid": LWJGL3, "conflicts": [{"uid": LWJGL}]}
            v["libraries"] = [lib for lib in v["libraries"] if Coord.parse(lib["name"]).artifact not in ("jutils", "jinput")]
        case _:
            raise ValueError(f"LWJGL version not recognized: {v['version']}")
    v |= {"volatile": True, "order": -1}

    for lib in v["libraries"]:
        natives = lib.get("natives")
        if not natives or lib in added:
            continue
        classifiers = lib.get("downloads", {}).get("classifiers") or {}
        if not {"linux", "windows", "osx"} <= natives.keys() or (
                "downloads" in lib and any(natives[os] not in classifiers for os in ("linux", "windows", "osx"))):
            log(f"Skipped LWJGL {v['version']}: {lib['name']} lacks natives for a platform")
            return
    write_version(v)


def generate():
    overrides = read(STATIC / "mojang/minecraft-legacy-override.json")["versions"]
    patches = load_patches()
    variants = defaultdict(list)
    any_lwjgl3 = False
    for path in VERSIONS.iterdir():
        if path.suffix == ".json":
            any_lwjgl3 |= minecraft(read(path), overrides, patches, variants)

    for version, found in variants.items():
        passed = [b for d, b in found if d in PASS_VARIANTS and d not in BAD_VARIANTS]
        unknown = [(d, b) for d, b in found if d not in PASS_VARIANTS and d not in BAD_VARIANTS]
        for d, b in unknown:
            log(f'    "{d}",  # {version} ({b.get("releaseTime")})')
        if len(passed) != 1 or unknown:
            raise ValueError(f"No LWJGL {version} variant decided: {len(passed)} passed, {len(unknown)} unknown")
        write_lwjgl(passed[0], patches)

    write_package(LWJGL, "LWJGL 2", recommended=["2.9.4-nightly-20150209"])
    if any_lwjgl3:
        write_package(LWJGL3, "LWJGL 3", recommended=["3.1.2"])
    write_package(MINECRAFT, "Minecraft", recommended=[read(MANIFEST)["latest"]["release"]])
