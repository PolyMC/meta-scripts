"""Fetch lwjgl3ify and Cleanroom releases into upstream/multi3ify.

Ported from https://github.com/AngelicIndustries/multi3ify. Each processed
release is stored once; a later run refuses to silently change a release whose
upstream assets were replaced with different contents.
"""
import hashlib
import io
import json
import os
import re
import time
import zipfile

import requests

from meta.common import upstream_path, ensure_upstream_dir
from meta.common.multi3ify import (
    LWJGL3IFY_DIR, LWJGL3IFY_RELEASES_API, LWJGL3IFY_MINIMUM, LWJGL3IFY_PATCH_UIDS,
    CLEANROOM_DIR, CLEANROOM_RELEASES_API, CLEANROOM_MINIMUM, CLEANROOM_LWJGL2_LIBRARIES,
)

UPSTREAM_DIR = upstream_path()

ensure_upstream_dir(LWJGL3IFY_DIR)
ensure_upstream_dir(CLEANROOM_DIR)

sess = requests.Session()
sess.headers["User-Agent"] = "meta-scripts-multi3ify"


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def fetch(url):
    headers = {"Accept": "application/vnd.github+json"}
    # Never send the token to release download/CDN hosts.
    if url.startswith("https://api.github.com/") and os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    for attempt in range(4):
        try:
            r = sess.get(url, headers=headers, timeout=90)
            r.raise_for_status()
            return r.content
        except requests.RequestException as e:
            if attempt == 3:
                raise
            print(f"Download failed for {url} (attempt {attempt + 1}/4): {e}")
            time.sleep(2 ** attempt)


def github_releases(api, version_pattern, key, minimum):
    result = []
    page = 1
    while True:
        batch = json.loads(fetch(f"{api}?per_page=100&page={page}"))
        if not isinstance(batch, list):
            raise ValueError(f"Unexpected GitHub releases response from {api}")
        for release in batch:
            version = release["tag_name"].removeprefix("v")
            # Some upstream beta tags are not marked prerelease on GitHub, so
            # the version pattern is checked as well.
            if release["draft"] or release["prerelease"] or not re.fullmatch(version_pattern, version):
                continue
            if key(version) >= key(minimum):
                result.append(release)
        if len(batch) < 100:
            break
        page += 1
    if not result:
        raise ValueError(f"No supported releases found at {api}")
    return result


def asset_bytes(asset):
    data = fetch(asset["browser_download_url"])
    if len(data) != asset["size"]:
        raise ValueError(f"Truncated release asset: {asset['name']}")
    digest = asset.get("digest")
    if digest and digest != "sha256:" + sha256(data):
        raise ValueError(f"Release asset checksum mismatch: {asset['name']}")
    return data


def required_assets(release, names):
    assets = {a["name"]: a for a in release["assets"]}
    missing = [n for n in names if n not in assets]
    if missing:
        raise ValueError(f"Release {release['tag_name']} is missing assets {missing}; refusing a partial publication")
    return [assets[n] for n in names]


def fingerprints(assets):
    # download_count and uploader fields change without changing an asset.
    return [{k: a.get(k) for k in ("id", "name", "size", "updated_at", "digest", "browser_download_url")}
            for a in assets]


def store(directory, version, assets, process):
    """Process a release once; refuse silent content changes to stored releases."""
    path = os.path.join(UPSTREAM_DIR, directory, f"{version}.json")
    prints = fingerprints(assets)
    old = None
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            old = json.load(f)
        if old["assets"] == prints:
            return
    result = process()
    result["assets"] = prints
    if old is not None:
        if {k: v for k, v in old.items() if k != "assets"} != {k: v for k, v in result.items() if k != "assets"}:
            raise ValueError(f"Refusing to change already published {directory}/{version}: upstream assets changed")
        print(f"Updated asset fingerprints of {directory}/{version}")
    else:
        print(f"Prepared {directory}/{version}")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, sort_keys=True)
        f.write("\n")


def lwjgl3ify_key(version):
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError(f"Expected a stable semantic version: {version}")
    return tuple(map(int, version.split(".")))


def process_lwjgl3ify(release, version, assets):
    with zipfile.ZipFile(io.BytesIO(asset_bytes(assets[0]))) as archive:
        patches = [json.loads(archive.read(n)) for n in archive.namelist()
                   if n.startswith("patches/") and n.endswith(".json")]
        patch_jar = archive.read(f"libraries/lwjgl3ify-{version}-forgePatches.jar")
    by_uid = {p["uid"]: p for p in patches}
    if set(by_uid) != LWJGL3IFY_PATCH_UIDS:
        raise ValueError(f"Upstream patch layout changed in lwjgl3ify {version}: {sorted(by_uid)}")
    early = by_uid["me.eigenraven.lwjgl3ify.forgepatches"]
    if len(early["libraries"]) != 1 or early["libraries"][0].get("MMC-hint") != "local":
        raise ValueError(f"Unexpected early classpath in lwjgl3ify {version}")
    if len(patch_jar) != assets[2]["size"]:
        raise ValueError(f"Embedded Forge patches do not match lwjgl3ify release {version}")
    if assets[2].get("digest") and assets[2]["digest"] != "sha256:" + sha256(patch_jar):
        raise ValueError(f"Embedded Forge patches checksum mismatch in lwjgl3ify {version}")
    # Replace the instance-local jar with the identical release asset.
    early["libraries"][0].pop("MMC-hint")
    early["libraries"][0]["downloads"] = {"artifact": {
        "url": assets[2]["browser_download_url"], "size": len(patch_jar),
        "sha1": hashlib.sha1(patch_jar).hexdigest(),
    }}
    mod = asset_bytes(assets[1])
    # Make sure this is the client mod, not an API/dev jar.
    with zipfile.ZipFile(io.BytesIO(mod)) as jar:
        if "Lwjgl3ifyCoremod" not in jar.read("META-INF/MANIFEST.MF").decode():
            raise ValueError(f"Missing lwjgl3ify coremod in {version}")
    return {"version": version, "releaseTime": release["published_at"],
            "patches": sorted(patches, key=lambda p: p["order"]),
            "modUrl": assets[1]["browser_download_url"], "modSha256": sha256(mod)}


def cleanroom_key(version):
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)(-alpha)?", version)
    if not match:
        raise ValueError(f"Unsupported Cleanroom version: {version}")
    return (*map(int, match.groups()[:3]), not bool(match[4]))


def cleanroom_empty_overrides(archive, loader):
    """Find upstream's empty local jars, which disable inherited libraries.

    The generator omits the disabled libraries instead, so the feed does not
    depend on instance-local files.
    """
    suppressed = set()
    members = set()
    for library in loader["libraries"]:
        if library.get("MMC-hint") != "local":
            continue
        parts = library["name"].split(":")
        if set(library) != {"name", "MMC-hint"} or len(parts) != 3 or parts[2] != "999999.0-empty":
            raise ValueError(f"Unsupported local Cleanroom override: {library}")
        member = f"libraries/{parts[1]}-{parts[2]}.jar"
        with zipfile.ZipFile(io.BytesIO(archive.read(member))) as jar:
            if jar.namelist():
                raise ValueError(f"Cleanroom override is not empty: {member}")
        members.add(member)
        suppressed.add(":".join(parts[:2]))
    if {n for n in archive.namelist() if n.endswith(".jar")} != members:
        raise ValueError("Unexpected bundled Cleanroom jars")
    loader["libraries"] = [lib for lib in loader["libraries"] if lib.get("MMC-hint") != "local"]
    return sorted(suppressed)


def process_cleanroom(release, version, assets):
    # 0.7+ packs inherit vanilla Minecraft instead of shipping its patch.
    modern = cleanroom_key(version) >= cleanroom_key("0.7.0-alpha")
    uids = (["net.minecraft", "org.lwjgl", "net.minecraftforge"] if modern
            else ["org.lwjgl3", "net.minecraft", "net.minecraftforge"])
    archive_data = asset_bytes(assets[0])
    with zipfile.ZipFile(io.BytesIO(archive_data)) as archive:
        expected = {f"patches/{uid}.json" for uid in uids if not (modern and uid == "net.minecraft")}
        members = {n for n in archive.namelist() if n.endswith(".json")}
        if members != expected | {"mmc-pack.json"}:
            raise ValueError(f"Unexpected Cleanroom archive layout: {sorted(members)}")
        pack = json.loads(archive.read("mmc-pack.json"))
        if pack.get("formatVersion") != 1 or [c["uid"] for c in pack["components"]] != uids:
            raise ValueError("Unexpected Cleanroom component layout/order")
        patches = {uid: json.loads(archive.read(f"patches/{uid}.json"))
                   for uid in uids if not (modern and uid == "net.minecraft")}
        for component in pack["components"]:
            patch = patches.get(component["uid"])
            if patch is not None and patch["version"] != component["version"]:
                raise ValueError("Cleanroom pack and patch versions disagree")
        if modern and pack["components"][0]["version"] != "1.12.2":
            raise ValueError("Cleanroom pack targets an unexpected Minecraft version")
        suppressed = cleanroom_empty_overrides(archive, patches["net.minecraftforge"]) if modern else []
    loader = patches["net.minecraftforge"]
    jar_name = f"com.cleanroommc:cleanroom:{version}" + (":universal" if modern else "")
    jars = [lib for lib in loader["libraries"] if lib["name"] == jar_name]
    if len(jars) != 1:
        raise ValueError(f"Unexpected Cleanroom universal jar in {version}")
    artifact = jars[0]["downloads"]["artifact"]
    universal = asset_bytes(assets[1])
    if len(universal) != artifact["size"] or hashlib.sha1(universal).hexdigest() != artifact["sha1"]:
        raise ValueError(f"Cleanroom {version} universal jar and profile disagree")
    return {"version": version, "releaseTime": release["published_at"], "modern": modern,
            "componentOrder": uids, "patches": [patches[uid] for uid in uids if uid in patches],
            "suppressedLibraries": suppressed,
            "archiveSha256": sha256(archive_data), "universalSha256": sha256(universal)}


def main():
    minimum = os.environ.get("LWJGL3IFY_MIN_VERSION", LWJGL3IFY_MINIMUM)
    if lwjgl3ify_key(minimum) < lwjgl3ify_key(LWJGL3IFY_MINIMUM):
        raise ValueError("lwjgl3ify older than 3.0.0 uses an unsupported patch layout")
    for release in github_releases(LWJGL3IFY_RELEASES_API, r"\d+\.\d+\.\d+", lwjgl3ify_key, minimum):
        version = release["tag_name"].removeprefix("v")
        assets = required_assets(release, [f"lwjgl3ify-{version}{s}"
                                           for s in ("-multimc.zip", ".jar", "-forgePatches.jar")])
        store(LWJGL3IFY_DIR, version, assets, lambda: process_lwjgl3ify(release, version, assets))

    minimum = os.environ.get("CLEANROOM_MIN_VERSION", CLEANROOM_MINIMUM)
    if cleanroom_key(minimum) < cleanroom_key(CLEANROOM_MINIMUM):
        raise ValueError(f"Cleanroom older than {CLEANROOM_MINIMUM} uses an unverified patch layout")
    for release in github_releases(CLEANROOM_RELEASES_API, r"\d+\.\d+\.\d+(-alpha)?", cleanroom_key, minimum):
        version = release["tag_name"].removeprefix("v")
        assets = required_assets(release, [f"cleanroom-{version}{s}" for s in (".zip", "-universal.jar")])
        store(CLEANROOM_DIR, version, assets, lambda: process_cleanroom(release, version, assets))


if __name__ == "__main__":
    main()
