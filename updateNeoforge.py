"""
 Get the source files necessary for generating NeoForge versions
"""
import hashlib
import itertools
import json
import os
import sys
import zipfile
from contextlib import suppress

import requests
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache

from meta.common import upstream_path, ensure_upstream_dir
from meta.common.neoforge import JARS_DIR, INSTALLER_MANIFEST_DIR, VERSION_MANIFEST_DIR, BAD_VERSIONS
from meta.model.mojang import MojangVersion
from meta.model.neoforge import NeoForgeEntry, NeoForgeInstallerProfile

UPSTREAM_DIR = upstream_path()

ensure_upstream_dir(JARS_DIR)
ensure_upstream_dir(INSTALLER_MANIFEST_DIR)
ensure_upstream_dir(VERSION_MANIFEST_DIR)

forever_cache = FileCache('caches/http_cache', forever=True)
sess = CacheControl(requests.Session(), forever_cache)


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def map_minecraft_ver_to_neo_forge_ver(neo_forge_version_list: list[str]) -> dict[str, list[str]]:
    return {k: list(v) for k, v in itertools.groupby(
        neo_forge_version_list,
        lambda x: "1." + ".".join(v for v in x.split(".")[:2] if v != "0"))}


def main():
    # get the remote version list fragments
    r = sess.get('https://maven.neoforged.net/api/maven/versions/releases/net/neoforged/neoforge')
    r.raise_for_status()
    by_mc_version = map_minecraft_ver_to_neo_forge_ver(r.json()["versions"])
    assert type(by_mc_version) is dict

    # separately retrieve legacy 1.20.1 versions
    r = sess.get('https://maven.neoforged.net/api/maven/versions/releases/net/neoforged/forge')
    r.raise_for_status()
    by_mc_version["1.20.1"] = [v for v in r.json()["versions"] if v not in BAD_VERSIONS]

    entries = []
    latest_set = {v[-1] for _, v in by_mc_version.items()}

    print("")
    print("Processing versions:")
    for mc_version, value in by_mc_version.items():
        assert type(mc_version) is str
        assert type(value) is list
        for version in value:
            assert type(version) is str

            entry = NeoForgeEntry(
                version=version,
                mc_version=mc_version,
                latest=version in latest_set
            )

            entries.append(entry)

    print("Grabbing installers and dumping installer profiles...")
    # get the installer jars - if needed - and get the installer profiles out of them

    for entry in entries:
        eprint(f"Updating NeoForge {entry.sane_version()}")

        jar_path = os.path.join(UPSTREAM_DIR, JARS_DIR, entry.installer_filename())
        version_path = os.path.join(UPSTREAM_DIR, VERSION_MANIFEST_DIR, f"{entry.sane_version()}.json")
        profile_path = os.path.join(UPSTREAM_DIR, INSTALLER_MANIFEST_DIR, f"{entry.sane_version()}.json")

        installer_refresh_required = not os.path.isfile(profile_path)

        if installer_refresh_required:
            # grab the installer if it's not there
            if not os.path.isfile(jar_path):
                if entry.mc_version == "1.20.1":
                    rfile = sess.get("https://maven.neoforged.net/api/maven/details/releases/net/neoforged/forge/"
                                     + entry.version, stream=True)
                    if "files" not in rfile.json():
                        eprint(f"Skipping {entry.sane_version()} with no valid files")
                        entries.remove(entry)
                        continue

                eprint(f"Downloading {entry.installer_url()}")
                installer_file = sess.get(entry.installer_url(), stream=True)
                installer_file.raise_for_status()
                with open(jar_path, 'wb') as f:
                    for chunk in installer_file.iter_content(chunk_size=128):
                        f.write(chunk)

        entry.installer_size = os.path.getsize(jar_path)

        with open(jar_path, "rb") as f:
            sha1 = hashlib.sha1()
            for block in iter(lambda: f.read(65536), b""):
                sha1.update(block)
            computed_hash = sha1.hexdigest()

        if entry.mc_version != "1.20.1":
            eprint(f"Downloading {entry.installer_url()}.sha1")
            hashfile = sess.get(entry.installer_url() + ".sha1", stream=True)
            hashfile.raise_for_status()
            upstream_hash = hashfile.text

            if upstream_hash != computed_hash:
                eprint(f"Skipping {entry.sane_version()} installer with invalid hash")
                continue

        entry.installer_sha1 = computed_hash

        eprint(f"Processing {entry.installer_url()}")
        if not os.path.isfile(profile_path):
            with zipfile.ZipFile(jar_path) as jar:
                with suppress(KeyError):
                    with jar.open('version.json') as profile_zip_entry:
                        version_data = profile_zip_entry.read()

                        # Process: does it parse?
                        MojangVersion.parse_raw(version_data)

                        with open(version_path, 'w') as version_json:
                            json.dump(json.loads(version_data), version_json, sort_keys=True, indent=4)
                            version_json.close()

                with jar.open('install_profile.json') as profile_zip_entry:
                    install_profile_data = profile_zip_entry.read()
                    NeoForgeInstallerProfile.parse_raw(install_profile_data)

                    with open(profile_path, 'w') as profile_json:
                        json.dump(json.loads(install_profile_data), profile_json, sort_keys=True, indent=4)
                        profile_json.close()

    print("")
    print("Dumping index files...")

    with open(UPSTREAM_DIR + "/neoforge/derived_index.json", 'w', encoding='utf-8') as f:
        json.dump([e.dict() for e in entries], f, sort_keys=True, indent=4)


if __name__ == '__main__':
    main()
