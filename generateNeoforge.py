import json
import os
import sys

from meta.common import ensure_component_dir, polymc_path, upstream_path, static_path
from meta.common.mojang import MINECRAFT_COMPONENT
from meta.common.neoforge import NEOFORGE_COMPONENT, INSTALLER_MANIFEST_DIR, VERSION_MANIFEST_DIR, DERIVED_INDEX_FILE
from meta.model import MetaVersion, Dependency, Library, GradleSpecifier, MojangLibraryDownloads, MojangArtifact, \
    MetaPackage
from meta.model.mojang import MojangVersion
from meta.model.neoforge import NeoForgeEntry, NeoForgeInstallerProfile

PMC_DIR = polymc_path()
UPSTREAM_DIR = upstream_path()
STATIC_DIR = static_path()

ensure_component_dir(NEOFORGE_COMPONENT)


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def version_from_installer(installer: MojangVersion, profile: NeoForgeInstallerProfile,
                           entry: NeoForgeEntry) -> MetaVersion:
    v = MetaVersion(name="NeoForge", version=entry.sane_version(), uid=NEOFORGE_COMPONENT)
    v.requires = [Dependency(uid=MINECRAFT_COMPONENT, equals=entry.mc_version)]
    v.main_class = "io.github.zekerzhayard.forgewrapper.installer.Main"

    # FIXME: Add the size and hash here
    v.maven_files = []

    # load the locally cached installer file info and use it to add the installer entry in the json
    installer_lib = Library(
        name=GradleSpecifier("net.neoforged", "forge" if entry.mc_version == "1.20.1" else "neoforge",
                             entry.version, "installer"))
    installer_lib.downloads = MojangLibraryDownloads()

    installer_lib.downloads.artifact = MojangArtifact(
        url=entry.installer_url(),
        sha1=entry.installer_sha1,
        size=entry.installer_size)
    v.maven_files.append(installer_lib)

    for upstream_lib in profile.libraries:
        forge_lib = Library.parse_obj(upstream_lib.dict())
        if forge_lib.name.is_log4j():
            continue

        v.maven_files.append(forge_lib)

    v.libraries = []

    wrapper_lib = Library(name=GradleSpecifier("io.github.zekerzhayard", "ForgeWrapper", "1.6.0"))
    wrapper_lib.downloads = MojangLibraryDownloads()
    wrapper_lib.downloads.artifact = MojangArtifact(
        url="https://github.com/ZekerZhayard/ForgeWrapper/releases/download/1.6.0/ForgeWrapper-1.6.0.jar",
        sha1="035a51fe6439792a61507630d89382f621da0f1f",
        size=28679
    )
    v.libraries.append(wrapper_lib)

    for upstream_lib in installer.libraries:
        forge_lib = Library.parse_obj(upstream_lib.dict())
        if forge_lib.name.is_log4j():
            continue

        v.libraries.append(forge_lib)

    v.release_time = installer.release_time
    v.order = 5
    mc_args = "--username ${auth_player_name} --version ${version_name} --gameDir ${game_directory} " \
              "--assetsDir ${assets_root} --assetIndex ${assets_index_name} --uuid ${auth_uuid} " \
              "--accessToken ${auth_access_token} --userType ${user_type} --versionType ${version_type}"
    for arg in installer.arguments.game:
        mc_args += f" {arg}"
    v.minecraft_arguments = mc_args
    return v


def main():
    # load the locally cached version list
    with open(os.path.join(UPSTREAM_DIR, DERIVED_INDEX_FILE), 'r') as f:
        entries = [NeoForgeEntry.from_obj(e) for e in json.load(f)]

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

        v.write(os.path.join(PMC_DIR, NEOFORGE_COMPONENT, f"{v.version}.json"))

        recommended_versions.sort()
        print('Recommended versions:', recommended_versions)

        package = MetaPackage(uid=NEOFORGE_COMPONENT, name="NeoForge", project_url="https://neoforged.net/")
        package.recommended = recommended_versions
        package.write(os.path.join(PMC_DIR, NEOFORGE_COMPONENT, "package.json"))


if __name__ == '__main__':
    main()
