import asyncio
import json
import os
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from functools import partial
from pathlib import Path

import httpx

UPSTREAM = Path(os.environ.get("UPSTREAM_DIR", "upstream"))
PMC = Path(os.environ.get("PMC_DIR", "polymc"))
STATIC = Path(os.environ.get("STATIC_DIR", "static"))

MINECRAFT = "net.minecraft"
LWJGL_GROUPS = {"org.lwjgl", "org.lwjgl.lwjgl", "net.java.jinput", "net.java.jutils"}

log = partial(print, file=sys.stderr, flush=True)


@dataclass
class Coord:
    group: str
    artifact: str
    version: str
    classifier: str | None = None
    extension: str = "jar"

    @classmethod
    def parse(cls, value: str) -> "Coord":
        base, _, ext = value.partition("@")
        parts = base.split(":")
        return cls(parts[0], parts[1], parts[2], parts[3] if len(parts) == 4 else None, ext or "jar")

    def __str__(self):
        s = f"{self.group}:{self.artifact}:{self.version}" + (f":{self.classifier}" if self.classifier else "")
        return s if self.extension == "jar" else f"{s}@{self.extension}"

    def path(self) -> str:
        name = f"{self.artifact}-{self.version}" + (f"-{self.classifier}" if self.classifier else "")
        return f"{self.group.replace('.', '/')}/{self.artifact}/{self.version}/{name}.{self.extension}"

    @property
    def is_lwjgl(self) -> bool:
        return self.group in LWJGL_GROUPS

    @property
    def is_log4j(self) -> bool:
        return self.group == "org.apache.logging.log4j"


def prune(obj):
    if isinstance(obj, dict):
        return {k: prune(v) for k, v in obj.items() if v is not None}
    if isinstance(obj, list):
        return [prune(v) for v in obj]
    return obj


def dumps(obj) -> str:
    return json.dumps(obj, indent=4, sort_keys=True)


def read(path: Path):
    return json.loads(path.read_bytes())


def write(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data if isinstance(data, bytes) else dumps(data).encode())


def write_version(v: dict):
    write(PMC / v["uid"] / f"{v['version']}.json", prune(v))


def write_package(uid: str, name: str, **fields):
    write(PMC / uid / "package.json", prune({"formatVersion": 1, "uid": uid, "name": name, **fields}))


def iso(value: str | datetime) -> str:
    dt = value if isinstance(value, datetime) else datetime.fromisoformat(value)
    return (dt if dt.tzinfo else dt.replace(tzinfo=UTC)).isoformat()


def check_mojang(v: dict):
    if (v.get("minimumLauncherVersion") or 0) > 21 or (v.get("complianceLevel") or 0) > 1:
        raise ValueError(f"Unsupported version file {v.get('id')}")


def _artifact(a: dict) -> dict:
    return {k: a.get(k) for k in ("sha1", "size", "url", "path")}


def library(lib: dict, extra: bool = True) -> dict:
    dl = lib.get("downloads")
    out = {
        "name": lib.get("name") and str(Coord.parse(lib["name"])),
        "downloads": None if dl is None else {
            "artifact": dl.get("artifact") and _artifact(dl["artifact"]),
            "classifiers": None if dl.get("classifiers") is None
            else {k: _artifact(v) for k, v in dl["classifiers"].items()},
        },
        "extract": lib.get("extract") and {"exclude": lib["extract"]["exclude"]},
        "natives": lib.get("natives"),
        "rules": None if lib.get("rules") is None else [
            {"action": r["action"], "os": r.get("os") and {"name": r["os"]["name"], "version": r["os"].get("version")}}
            for r in lib["rules"]
        ],
    }
    if extra:
        out |= {"url": lib.get("url"), "MMC-hint": lib.get("MMC-hint")}
    return prune(out)


def client() -> httpx.AsyncClient:
    return httpx.AsyncClient(
        transport=httpx.AsyncHTTPTransport(retries=3, limits=httpx.Limits(max_connections=32)),
        timeout=httpx.Timeout(60),
        follow_redirects=True,
    )


async def get(http: httpx.AsyncClient, url: str) -> httpx.Response:
    r = await http.get(url)
    r.raise_for_status()
    return r


async def get_json(http: httpx.AsyncClient, url: str):
    return (await get(http, url)).json()


async def amap(fn, items) -> list:
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(fn(i)) for i in items]
    return [t.result() for t in tasks]
