from datetime import UTC, datetime

from .common import MINECRAFT, UPSTREAM, get_json, iso, library, read, write, write_package, write_version

LITELOADER = "com.mumfrey.liteloader"
INDEX = UPSTREAM / "liteloader/versions.json"
ASM_URLS = {"org.ow2.asm:asm-all:5.0.3": "https://repo.maven.apache.org/maven2/",
            "org.ow2.asm:asm-all:5.2": "http://repo.liteloader.com/"}


async def update(http):
    write(INDEX, await get_json(http, "http://dl.liteloader.com/versions/versions.json"))


def generate():
    index = read(INDEX)
    versions, recommended = [], []
    for mc, entry in index["versions"].items():
        if mc == "1.5.2":
            continue
        for section, snapshot in (("artefacts", False), ("snapshots", True)):
            for key, a in ((entry.get(section) or {}).get("com.mumfrey:liteloader") or {}).items():
                if key == "latest":
                    if not snapshot:
                        recommended.append(a["version"])
                    continue
                libs = [library(lib) for lib in a["libraries"]]
                for lib in libs:
                    lib["url"] = ASM_URLS.get(lib["name"], lib.get("url"))
                libs.append({"name": f"com.mumfrey:liteloader:{a['version']}", "url": "http://dl.liteloader.com/versions/",
                             "MMC-hint": "always-stale" if snapshot else None})
                versions.append({
                    "formatVersion": 1, "name": "LiteLoader", "uid": LITELOADER, "version": a["version"],
                    "type": "snapshot" if snapshot else "release", "order": 10, "libraries": libs,
                    "requires": [{"uid": MINECRAFT, "equals": mc}],
                    "releaseTime": iso(datetime.fromtimestamp(int(a["timestamp"]), UTC)),
                    "mainClass": "net.minecraft.launchwrapper.Launch", "+tweakers": [a["tweakClass"]],
                })

    for v in sorted(versions, key=lambda v: datetime.fromisoformat(v["releaseTime"]), reverse=True):
        write_version(v)
    meta = index["meta"]
    write_package(LITELOADER, "LiteLoader", recommended=sorted(recommended), description=meta["description"],
                  projectUrl=meta["url"], authors=[meta["authors"]])
