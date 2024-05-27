from os.path import join

BASE_DIR = "neoforge"

JARS_DIR = join(BASE_DIR, "jars")
INSTALLER_INFO_DIR = join(BASE_DIR, "installer_info")
VERSION_MANIFEST_DIR = join(BASE_DIR, "version_manifests")
INSTALLER_MANIFEST_DIR = join(BASE_DIR, "installer_manifests")
INSTALLER_HASH_DIR = join(BASE_DIR, "installer_hashes")
DERIVED_INDEX_FILE = join(BASE_DIR, "derived_index.json")

NEOFORGE_COMPONENT = "net.neoforged.neoforge"
FORGEWRAPPER_MAVEN = "https://polymc.github.io/files/maven/%s"
