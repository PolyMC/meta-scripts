import hashlib
import json
from datetime import datetime

from .common import PMC, iso, prune, write


def generate():
    packages = []
    for pkg in sorted(p for p in PMC.iterdir() if p.is_dir() and not p.name.startswith(".")):
        shared = json.loads((pkg / "package.json").read_bytes())
        recommended = set(shared.get("recommended") or [])
        versions = []
        for f in pkg.iterdir():
            if f.name in ("index.json", "package.json") or not f.is_file():
                continue
            data = f.read_bytes()
            v = json.loads(data)
            versions.append({
                "version": v["version"], "type": v.get("type"), "releaseTime": iso(v["releaseTime"]),
                "requires": v.get("requires"), "conflicts": v.get("conflicts"), "volatile": v.get("volatile"),
                "recommended": v["version"] in recommended, "sha256": hashlib.sha256(data).hexdigest(),
            })
        versions.sort(key=lambda e: datetime.fromisoformat(e["releaseTime"]), reverse=True)
        write(pkg / "index.json", prune({"formatVersion": 1, "name": shared["name"], "uid": pkg.name, "versions": versions}))
        packages.append({"name": shared["name"], "uid": pkg.name,
                         "sha256": hashlib.sha256((pkg / "index.json").read_bytes()).hexdigest()})
    write(PMC / "index.json", {"formatVersion": 1, "packages": packages})
