import io
import zipfile
from dataclasses import dataclass
from datetime import datetime
from email.utils import parsedate_to_datetime

from .common import MINECRAFT, UPSTREAM, Coord, amap, get, get_json, iso, library, log, read, write, write_package, \
    write_version

INTERMEDIARY = "net.fabricmc.intermediary"


@dataclass(frozen=True)
class Flavor:
    key: str
    meta: str
    meta_dir: str
    maven: str
    uid: str
    name: str
    description: str
    project_url: str
    authors: tuple[str, ...]
    components: tuple[str, ...]
    stable_only: bool


FLAVORS = {f.key: f for f in (
    Flavor("fabric", "https://meta.fabricmc.net/v2/versions/", "meta-v2", "https://maven.fabricmc.net",
           "net.fabricmc.fabric-loader", "Fabric Loader",
           "Fabric Loader is a tool to load Fabric-compatible mods in game environments.",
           "https://fabricmc.net", ("Fabric Developers",), ("intermediary", "loader"), False),
    Flavor("quilt", "https://meta.quiltmc.org/v3/versions/", "meta-v3", "https://maven.quiltmc.org/repository/release",
           "org.quiltmc.quilt-loader", "Quilt Loader",
           "The Quilt project is an open, community-driven modding toolchain designed primarily for Minecraft.",
           "https://quiltmc.org/", ("Quilt Project",), ("loader",), True),
)}


def maven_url(f: Flavor, key: str, ext: str) -> str:
    group, artifact, version = key.split(":")[:3]
    return f"{f.maven}/{group.replace('.', '/')}/{artifact}/{version}/{artifact}-{version}{ext}"


def jar_info_path(f: Flavor, item: dict):
    return UPSTREAM / f.key / "jars" / f"{item['maven'].replace(':', '.')}.json"


def installer_path(f: Flavor, item: dict):
    return UPSTREAM / f.key / "loader-installer-json" / f"{item['version']}.json"


async def fetch_jar_info(http, f: Flavor, item: dict) -> bool:
    path = jar_info_path(f, item)
    if path.exists():
        return True
    url = maven_url(f, item["maven"], ".jar")
    r = await http.head(url)
    if r.status_code == 404:
        log(f"Skipping {f.key} {item['maven']}: jar not found")
        return False
    if r.is_success and "last-modified" in r.headers:
        released = parsedate_to_datetime(r.headers["last-modified"])
    else:
        with zipfile.ZipFile(io.BytesIO((await get(http, url)).content)) as z:
            released = max((datetime(*i.date_time) for i in z.infolist()), default=datetime(1970, 1, 1))
    write(path, {"releaseTime": iso(released)})
    return True


async def fetch_installer(http, f: Flavor, item: dict) -> bool:
    path = installer_path(f, item)
    if path.exists():
        return True
    r = await http.get(maven_url(f, item["maven"], ".json"))
    if r.status_code == 404:
        log(f"Skipping {f.key} loader {item['version']}: installer json not found")
        return False
    r.raise_for_status()
    write(path, r.json())
    return True


async def update(http, key: str):
    f = FLAVORS[key]

    async def component(name: str):
        index = await get_json(http, f.meta + name)

        async def process(item) -> bool:
            return await fetch_jar_info(http, f, item) and (name != "loader" or await fetch_installer(http, f, item))

        kept = await amap(process, index)
        write(UPSTREAM / f.key / f.meta_dir / f"{name}.json", [i for i, ok in zip(index, kept) if ok])

    await amap(component, f.components)


def generate(key: str):
    f = FLAVORS[key]
    meta = UPSTREAM / f.key / f.meta_dir
    released = lambda item: iso(read(jar_info_path(f, item))["releaseTime"])
    loader_lib = lambda item: {"name": str(Coord.parse(item["maven"])), "url": f.maven}

    recommended = []
    for item in read(meta / "loader.json"):
        info = read(installer_path(f, item))
        main = info.get("mainClass")
        libs = info["libraries"]
        write_version({
            "formatVersion": 1, "name": f.name, "uid": f.uid, "version": item["version"], "type": "release",
            "order": 10, "releaseTime": released(item), "requires": [{"uid": INTERMEDIARY}],
            "mainClass": main.get("client") if isinstance(main, dict) else main,
            "libraries": [library(lib) for lib in (libs.get("common") or []) + (libs.get("client") or [])]
                         + [loader_lib(item)],
        })
        if not recommended and not (f.stable_only and "-" in item["version"]):
            recommended.append(item["version"])
    write_package(f.uid, f.name, recommended=recommended, description=f.description, projectUrl=f.project_url,
                  authors=list(f.authors))

    if "intermediary" in f.components:
        items = read(meta / "intermediary.json")
        for item in items:
            write_version({
                "formatVersion": 1, "name": "Intermediary Mappings", "uid": INTERMEDIARY, "version": item["version"],
                "type": "release", "order": 11, "volatile": True, "releaseTime": released(item),
                "requires": [{"uid": MINECRAFT, "equals": item["version"]}], "libraries": [loader_lib(item)],
            })
        write_package(INTERMEDIARY, "Intermediary Mappings", recommended=[i["version"] for i in items],
                      description="Intermediary mappings allow using Fabric Loader with mods for Minecraft in a more "
                                  "compatible manner.",
                      projectUrl="https://fabricmc.net", authors=["Fabric Developers"])
