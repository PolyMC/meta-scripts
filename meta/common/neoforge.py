from os.path import join

BASE_DIR = "neoforge"

JARS_DIR = join(BASE_DIR, "jars")
VERSION_MANIFEST_DIR = join(BASE_DIR, "version_manifests")
INSTALLER_MANIFEST_DIR = join(BASE_DIR, "installer_manifests")
DERIVED_INDEX_FILE = join(BASE_DIR, "derived_index.json")

NEOFORGE_COMPONENT = "net.neoforged.neoforge"
BAD_VERSIONS = ["1.20.1-47.1.7", "47.1.82"]
