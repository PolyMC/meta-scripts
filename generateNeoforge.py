from datetime import datetime

from meta.common.json import dumps, load
import os
import sys

from meta.common import ensure_component_dir, polymc_path, upstream_path, serialize_datetime
from meta.common.mojang import MINECRAFT_COMPONENT
from meta.common.neoforge import NEOFORGE_COMPONENT, INSTALLER_MANIFEST_DIR, VERSION_MANIFEST_DIR, DERIVED_INDEX_FILE
from meta.model.mojang import MojangVersion
from meta.model.neoforge import NeoForgeEntry, NeoForgeInstallerProfile

PMC_DIR = polymc_path()
UPSTREAM_DIR = upstream_path()

ensure_component_dir(NEOFORGE_COMPONENT)


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def _lib_dict(name_str, downloads=None, extract=None, natives=None, rules=None):
    d = {"name": name_str}
    if downloads:
        d["downloads"] = downloads
    if extract:
        d["extract"] = extract
    if natives:
        d["natives"] = natives
    if rules:
        d["rules"] = rules
    return d


def _artifact_dict(url, sha1=None, size=None, path=None):
    d = {"url": url}
    if sha1:
        d["sha1"] = sha1
    if size is not None:
        d["size"] = size
    if path:
        d["path"] = path
    return d


def _lib_from_upstream(upstream_lib):
    name_str = str(upstream_lib.name)
    downloads = None
    if upstream_lib.downloads and upstream_lib.downloads.artifact:
        a = upstream_lib.downloads.artifact
        downloads = {"artifact": _artifact_dict(url=a.url, sha1=a.sha1, size=a.size, path=a.path)}
    return _lib_dict(name_str, downloads=downloads)


def version_from_installer(installer: MojangVersion, profile: NeoForgeInstallerProfile,
                           entry: NeoForgeEntry):
    loader = "forge" if entry.mc_version == "1.20.1" else "neoforge"
    installer_name = f"net.neoforged:{loader}:{entry.version}:installer"
    installer_url = entry.installer_url()

    maven_files = []
    maven_files.append(_lib_dict(
        installer_name,
        downloads={"artifact": _artifact_dict(url=installer_url, sha1=entry.installer_sha1, size=entry.installer_size)}
    ))

    for upstream_lib in profile.libraries:
        if upstream_lib.name.is_log4j():
            continue
        maven_files.append(_lib_from_upstream(upstream_lib))

    libraries = []
    libraries.append(_lib_dict(
        "io.github.zekerzhayard:ForgeWrapper:mmc7",
        downloads={"artifact": _artifact_dict(
            url="https://github.com/MultiMC/ForgeWrapper/releases/download/mmc7/ForgeWrapper-mmc7.jar",
            sha1="0c99747406998c933be78a368dfd8386949d1935",
            size=29346
        )}
    ))

    for upstream_lib in installer.libraries:
        if upstream_lib.name.is_log4j():
            continue
        libraries.append(_lib_from_upstream(upstream_lib))

    mc_args = "--username ${auth_player_name} --version ${version_name} --gameDir ${game_directory} " \
              "--assetsDir ${assets_root} --assetIndex ${assets_index_name} --uuid ${auth_uuid} " \
              "--accessToken ${auth_access_token} --userType ${user_type} --versionType ${version_type}"
    for arg in installer.arguments.game:
        mc_args += f" {arg}"

    release_time = serialize_datetime(installer.release_time) if isinstance(installer.release_time, datetime) else installer.release_time

    return {
        "formatVersion": 1,
        "name": "NeoForge",
        "version": entry.sane_version(),
        "uid": NEOFORGE_COMPONENT,
        "requires": [{"uid": MINECRAFT_COMPONENT, "equals": entry.mc_version}],
        "mainClass": "io.github.zekerzhayard.forgewrapper.installer.Main",
        "mavenFiles": maven_files,
        "libraries": libraries,
        "order": 5,
        "releaseTime": release_time,
        "minecraftArguments": mc_args,
    }


def main():
    # load the locally cached version list
    with open(os.path.join(UPSTREAM_DIR, DERIVED_INDEX_FILE), 'r') as f:
        entries = [NeoForgeEntry.from_obj(e) for e in load(f)]

    recommended_versions = []

    for entry in entries:
        if not os.path.isfile(os.path.join(PMC_DIR, MINECRAFT_COMPONENT, f"{entry.mc_version}.json")):
            eprint(f"Skipping NeoForge {entry.sane_version()} with no corresponding Minecraft version {entry.mc_version}")
            continue

        if entry.latest:
            recommended_versions.append(entry.sane_version())

        # Path for new-style build system based installers
        profile_filepath = os.path.join(UPSTREAM_DIR, INSTALLER_MANIFEST_DIR, f"{entry.sane_version()}.json")
        installer_version_filepath = os.path.join(UPSTREAM_DIR, VERSION_MANIFEST_DIR, f"{entry.sane_version()}.json")

        if not os.path.isfile(profile_filepath):
            eprint(f"Skipping {entry.sane_version()} with missing profile json")
            continue
        eprint(f"Processing NeoForge {entry.sane_version()}")
        profile = NeoForgeInstallerProfile.parse_file(profile_filepath)
        installer = MojangVersion.parse_file(installer_version_filepath)
        v = version_from_installer(installer, profile, entry)

        with open(os.path.join(PMC_DIR, NEOFORGE_COMPONENT, f"{v['version']}.json"), 'w') as f:
            f.write(dumps(v, indent=4, sort_keys=True))

    recommended_versions.sort()
    print('Recommended versions:', recommended_versions)

    from meta.model import MetaPackage
    package = MetaPackage(uid=NEOFORGE_COMPONENT, name="NeoForge", project_url="https://neoforged.net/")
    package.recommended = recommended_versions
    package.write(os.path.join(PMC_DIR, NEOFORGE_COMPONENT, "package.json"))


if __name__ == '__main__':
    main()
