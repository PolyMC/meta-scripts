# important that this runs *AFTER* any mojang server-related scripts. it depends on normal launcher files already being there
import json
import os
from urllib.request import urlopen

from meta.common import ensure_component_dir, polymc_path
from meta.common.mojang import MINECRAFT_COMPONENT

PMC_DIR = polymc_path()
ensure_component_dir(MINECRAFT_COMPONENT)

net_minecraft_files = os.listdir(os.path.join(PMC_DIR, MINECRAFT_COMPONENT))

def gen_compatible_meta_obj(version_meta):
    out = {
        "assetIndex": version_meta["assetIndex"],
        "compatibleJavaMajors": [8],
        "formatVersion": 1,
        "mainClass": version_meta["mainClass"],
        "mainJar": {
            "downloads": {
                "artifact": version_meta["downloads"]["client"]
            },
            "name": f"com.mojang.minecraft:{meta_id}:client"
        },
        "name": "Minecraft",
        "omni": True,
        "order": -2,
        "releaseTime": version_meta["releaseTime"],
        "requires": [
            {
                "suggests": "2.9.4-nightly-20150209",
                "uid": "org.lwjgl"
            }
        ],
        "type": version_meta["type"],
        "uid": "net.minecraft",
        "version": meta_id
    }

    # make needed changes depending on version type
    if version_meta["type"] == "old_alpha":
        out["+jvmArgs"] = ["-Dhttp.proxyHost=betacraft.uk", "-Djava.util.Arrays.useLegacyMergeSort=true"]
        out["+traits"] = ["legacyLaunch", "no-texturepacks"]
    elif version_meta["type"] == "old_beta":
        out["+traits"] = ["legacyLaunch", "texturepacks"]

    # need launchwrapper, jopt, and asm-all for these versions to run
    out["libraries"] = []
    for library in version_meta["libraries"]:
        if "launchwrapper" in library["name"] or "jopt" in library["name"] or "asm-all" in library["name"]:
            out["libraries"].append(library)
    
    return out

with urlopen("https://raw.githubusercontent.com/skyrising/mc-versions/main/data/version_manifest.json") as ver_man_req:
    version_manifest = json.loads(ver_man_req.read())
    for version in version_manifest["versions"]:
        meta_id = version["id"]
        meta_filename = meta_id + ".json"

        # skip server versions and versions that are already there
        if meta_id.startswith("server") or meta_filename in net_minecraft_files:
            continue

        print(f"Found OmniArchive version {meta_id}")
        meta_url = version["url"]
        with urlopen(f"https://skyrising.github.io/mc-versions/{meta_url}") as ver_meta_req:
            version_meta = json.loads(ver_meta_req.read())
            # some server versions don't start with "server" for some reason, but they all don't have assetIndex
            if "assetIndex" not in version_meta:
                continue

            meta_obj = gen_compatible_meta_obj(version_meta)
            with open(os.path.join(PMC_DIR, MINECRAFT_COMPONENT, meta_filename), "wt") as meta_json_file:
                meta_json_file.write(json.dumps(meta_obj, indent=4))
