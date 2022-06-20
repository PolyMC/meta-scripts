import copy
import hashlib
import os
from collections import defaultdict, namedtuple
from operator import attrgetter
from pprint import pprint
import re
from typing import Dict, List, Optional
from libPatches import get_lib_patches

from meta.common import ensure_component_dir, polymc_path, upstream_path, static_path
from meta.common.mojang import VERSION_MANIFEST_FILE, MINECRAFT_COMPONENT, LWJGL3_COMPONENT, LWJGL_COMPONENT, \
    STATIC_LWJGL322_FILE, STATIC_OVERRIDES_FILE, VERSIONS_DIR
from meta.model import MetaVersion, Library, GradleSpecifier, MojangLibraryDownloads, MojangArtifact, Dependency, \
    MetaPackage, MojangRule, MojangRules, OSRule
from meta.model.mojang import MojangIndexWrap, MojangIndex, MojangVersion, LegacyOverrideIndex


PMC_DIR = polymc_path()
UPSTREAM_DIR = upstream_path()
STATIC_DIR = static_path()

ensure_component_dir(MINECRAFT_COMPONENT)
ensure_component_dir(LWJGL_COMPONENT)
ensure_component_dir(LWJGL3_COMPONENT)


def map_log4j_artifact(version):
    if version == "2.0-beta9":
        return "2.0-beta9-fixed", "https://polymc.github.io/files/maven/%s"
    return "2.17.1", "https://repo1.maven.org/maven2/%s"  # This is the only version that's patched (as of 2022/02/19)


LOG4J_HASHES = {
    "2.0-beta9-fixed": {
        "log4j-api": {
            "sha1": "b61eaf2e64d8b0277e188262a8b771bbfa1502b3",
            "size": 107347
        },
        "log4j-core": {
            "sha1": "677991ea2d7426f76309a73739cecf609679492c",
            "size": 677588
        }
    },
    "2.17.1": {
        "log4j-api": {
            "sha1": "d771af8e336e372fb5399c99edabe0919aeaf5b2",
            "size": 301872
        },
        "log4j-core": {
            "sha1": "779f60f3844dadc3ef597976fcb1e5127b1f343d",
            "size": 1790452
        },
        "log4j-slf4j18-impl": {
            "sha1": "ca499d751f4ddd8afb016ef698c30be0da1d09f7",
            "size": 21268
        }
    }
}

def add_or_get_bucket(buckets, lib: Library) -> MetaVersion:
    rule_hash = None
    # if there are custom rules used to exclude arch-specific patches, use a key of "None"
    # to continue treating the library as common between all LWJGL versions
    if lib.rules: # and not lib.arch_rules:
            rule_hash = hash(lib.rules.json())

    if rule_hash in buckets:
        bucket = buckets[rule_hash]
    else:
        bucket = MetaVersion(name="LWJGL", version="undetermined", uid=LWJGL_COMPONENT)
        bucket.type = "release"
        buckets[rule_hash] = bucket
    return bucket


def hash_lwjgl_version(lwjgl: MetaVersion):
    lwjgl_copy = copy.deepcopy(lwjgl)
    lwjgl_copy.release_time = None
    return hashlib.sha1(lwjgl_copy.json().encode("utf-8", "strict")).hexdigest()


def sort_libs_by_name(library):
    return library.name


LWJGLEntry = namedtuple('LWJGLEntry', ('version', 'sha1'))

lwjglVersionVariants = defaultdict(list)


def add_lwjgl_version(variants, lwjgl):
    lwjgl_copy = copy.deepcopy(lwjgl)
    libraries = list(lwjgl_copy.libraries)
    libraries.sort(key=sort_libs_by_name)
    lwjgl_copy.libraries = libraries

    version = lwjgl_copy.version
    current_hash = hash_lwjgl_version(lwjgl_copy)
    found = False
    for variant in variants[version]:
        existing_hash = variant.sha1
        if current_hash == existing_hash:
            found = True
            break
    if not found:
        # print("!!! New variant for LWJGL version %s" % version)
        variants[version].append(LWJGLEntry(version=lwjgl_copy, sha1=current_hash))


def remove_paths_from_lib(lib):
    if lib.downloads.artifact:
        lib.downloads.artifact.path = None
    if lib.downloads.classifiers:
        for key, value in lib.downloads.classifiers.items():
            value.path = None


def adapt_new_style_arguments(arguments):
    foo = []
    # we ignore the jvm arguments entirely.
    # grab the strings, log the complex stuff
    # Added demo mode and width/height checks
    # to reduce console spam
    for arg in arguments.game:
        if isinstance(arg, str):
            if arg == '--clientId':
                continue
            if arg == '${clientid}':
                continue
            if arg == '--xuid':
                continue
            if arg == '${auth_xuid}':
                continue
            foo.append(arg)
        elif isinstance(arg, dict):
            if 'value' in arg:
                if arg['value'] == '--demo':
                    # Just an arg to activate demo mode, ignore
                    continue
                elif isinstance(arg['value'], list):
                    if arg['value'][0] == '--width':
                        # Width/height args, IDK why these are here
                        continue
        else:
            print("!!! Unrecognized structure in Minecraft game arguments:")
            pprint(arg)
    return ' '.join(foo)

def process_single_variant(lwjgl_variant: MetaVersion):
    lwjgl_version = lwjgl_variant.version
    v = copy.deepcopy(lwjgl_variant)

    if lwjgl_version[0] == '2':
        static_filename = os.path.join(STATIC_DIR, LWJGL_COMPONENT, f"{lwjgl_version}.json")
        filename = os.path.join(PMC_DIR, LWJGL_COMPONENT, f"{lwjgl_version}.json")
        if os.path.isfile(static_filename):
            v = MetaVersion.parse_file(static_filename)
            print("LWJGL2 is static:", v.version)

        v.name = 'LWJGL 2'
        v.uid = LWJGL_COMPONENT
        v.conflicts = [Dependency(uid=LWJGL3_COMPONENT)]
    elif lwjgl_version[0] == '3':
        static_filename = os.path.join(STATIC_DIR, LWJGL3_COMPONENT, f"{lwjgl_version}.json")
        filename = os.path.join(PMC_DIR, LWJGL3_COMPONENT, f"{lwjgl_version}.json")
        if os.path.isfile(static_filename):
            v = MetaVersion.parse_file(static_filename)
            print("LWJGL3 is static:", v.version)

        v.name = 'LWJGL 3'
        v.uid = LWJGL3_COMPONENT
        v.conflicts = [Dependency(uid=LWJGL_COMPONENT)]
        # remove jutils and jinput from LWJGL 3
        # this is a dependency that Mojang kept in, but doesn't belong there anymore
        filtered_libraries = list(filter(lambda l: l.name.artifact not in ["jutils", "jinput"], v.libraries))
        v.libraries = filtered_libraries
        if os.path.isfile(static_filename):
            v.write(filename)
            return True
    else:
        raise Exception("LWJGL version not recognized: %s" % v.version)
    v.volatile = True
    v.order = -1
    good = True
    for lib in v.libraries:
        if not lib.natives or lib.arch_rules:
            continue
        searchingFor = lwjgl_version[0:5]
        foundLWJGL_re = '.'.join(re.findall(r'[0-9](?=[\n\-.:]|$)', str(lib.name))[0:3])
        if lwjgl_version[0:5] != '.'.join(re.findall(r'[0-9](?=[\n\-.:]|$)', str(lib.name))[0:3]):
            # print(f"Warning: LWJGL versions searchingFor: {lwjgl_version} and found: {foundLWJGL_re} not the same!")
            continue
        checked_dict = {'linux', 'linux-arm64', 'windows', 'osx', 'osx-arm64'}
        if not checked_dict.issubset(lib.natives.keys()):
            print("Missing system classifier!", v.version, lib.name, lib.natives.keys())
            good = False
            break
        if lib.downloads:
            for entry in checked_dict:
                baked_entry = lib.natives[entry]
                if baked_entry not in lib.downloads.classifiers:
                    print("Missing download for classifier!", v.version, lib.name, baked_entry,
                          lib.downloads.classifiers.keys())
                    good = False
                    break
    if good:
        v.write(filename)
        return True
    else:
        return False


# converts a full library name to a major version name
# for example, "ca.weblite:java-objc-bridge:1.1.0" becomes "ca.weblite:java-objc-bridge:1"
def get_major_name(name: str):
    return re.match(r'.+:\d+', name).group(0)


def add_or_append_arch_rule(lib: Library, action: str, arch: str):
    if lib.arch_rules:
        if arch not in lib.arch_rules[action]:
            lib.arch_rules[action].append(arch)
    else:
        lib.arch_rules = {action: [arch]}



def main():
    # get the local version list
    override_index = LegacyOverrideIndex.parse_file(os.path.join(STATIC_DIR, STATIC_OVERRIDES_FILE))

    found_any_lwjgl3 = False

    lib_patches: Dict[str, Dict[str, List[Library]]] = {}
    # remap patches to a Library indexed by its major version name
    for k, v in get_lib_patches().items():
        d = {}
        for p in v:
            if d.get(get_major_name(p["name"])) == None:
                d[get_major_name(p["name"])] = [Library.parse_obj(p)]
            else:
                d[get_major_name(p["name"])].append(Library.parse_obj(p))
        lib_patches[k] = d

    for filename in os.listdir(os.path.join(UPSTREAM_DIR, VERSIONS_DIR)):
        input_file = os.path.join(UPSTREAM_DIR, VERSIONS_DIR, filename)
        if not input_file.endswith(".json"):
            # skip non JSON files
            continue
        print("Processing", filename)
        mojang_version = MojangVersion.parse_file(input_file)
        v = mojang_version.to_meta_version("Minecraft", MINECRAFT_COMPONENT, mojang_version.id)

        libs_minecraft = []
        is_lwjgl_3 = False
        buckets = {}

        for lib in v.libraries:
            specifier = lib.name
            new_libs: List[Library] = []

            for name, patches in lib_patches.items():
                lib_name = str(lib.name)
                patchlist = patches.get(get_major_name(lib_name))
                if patchlist == None:
                    continue
                for patch in patchlist:
                    if patch.name == lib.name:
                        #print(f"Patching library {lib_name} for {name}")
                        new_lib = copy.deepcopy(patch)
                        add_or_append_arch_rule(new_lib, "allow", name)
                        new_libs.append(new_lib)
                        # Purpose of this if is to remove duplicate disallow rules
                        if lib.arch_rules == None or name not in lib.arch_rules["disallow"]:
                            # print("Adding disallow rule for lib " + str(lib.name) + " and arch " + name)
                            add_or_append_arch_rule(lib, "disallow", name)
                        # New traits system for libs just for the launcher to check if it needs to append the arch in the filename
                        new_lib.add_archdependent_trait()
            
            # generic fixes
            remove_paths_from_lib(lib)

            if specifier.is_lwjgl():
                rules = None
                if lib.rules:
                    rules = lib.rules
                    lib.rules = None
                bucket = add_or_get_bucket(buckets, lib)
                if specifier.group == "org.lwjgl.lwjgl" and specifier.artifact == "lwjgl":
                    bucket.version = specifier.version
                if specifier.group == "org.lwjgl" and specifier.artifact == "lwjgl":
                    is_lwjgl_3 = True
                    found_any_lwjgl3 = True
                    bucket.version = specifier.version
                if not bucket.libraries:
                    bucket.libraries = []
                lib.rules = rules # maaaybe fix? YES IT FIXES IT WOOO HOO YES YESSSSSSSSSSSSSSSSSSSSSSSSS!!!!!!!!!!!!!!! LETS GOOOOOO
                # New traits system for libs just for the launcher to check if it needs to append the arch in the filename
                lib.add_archdependent_trait()
               
                bucket.libraries.append(lib)
                bucket.libraries.extend(new_libs)
                bucket.release_time = v.release_time
                
            # FIXME: workaround for insane log4j nonsense from December 2021. Probably needs adjustment.
            elif lib.name.is_log4j():
                version_override, maven_override = map_log4j_artifact(lib.name.version)

                if version_override not in LOG4J_HASHES:
                    raise Exception("ERROR: unhandled log4j version (overriden) %s!" % version_override)

                if lib.name.artifact not in LOG4J_HASHES[version_override]:
                    raise Exception("ERROR: unhandled log4j artifact %s!" % lib.name.artifact)

                replacement_name = GradleSpecifier("org.apache.logging.log4j", lib.name.artifact, version_override)
                artifact = MojangArtifact(
                    url=maven_override % (replacement_name.path()),
                    sha1=LOG4J_HASHES[version_override][lib.name.artifact]["sha1"],
                    size=LOG4J_HASHES[version_override][lib.name.artifact]["size"]
                )

                libs_minecraft.append(Library(
                    name=replacement_name,
                    downloads=MojangLibraryDownloads(artifact=artifact)
                ))
            else:
                lib.add_archdependent_trait()
                libs_minecraft.append(lib)
                if len(new_libs) > 0:
                    libs_minecraft.extend(new_libs)
        if len(buckets) == 1:
            for key in buckets:
                lwjgl = buckets[key]
                lwjgl.libraries = sorted(lwjgl.libraries, key=attrgetter("name"))
                add_lwjgl_version(lwjglVersionVariants, lwjgl)
                # print("Found only candidate LWJGL", lwjgl.version, key)
        else:
            # multiple buckets for LWJGL. [None] is common to all, other keys are for different sets of rules
            for key in buckets:
                if key is None:
                    continue
                lwjgl = buckets[key]
                if None in buckets:
                    lwjgl.libraries = sorted(lwjgl.libraries + buckets[None].libraries, key=attrgetter("name"))
                else:
                    lwjgl.libraries = sorted(lwjgl.libraries, key=attrgetter('name'))
                add_lwjgl_version(lwjglVersionVariants, lwjgl)
                # print("Found candidate LWJGL", lwjgl.version, key)
            # remove the common bucket...
            if None in buckets:
                del buckets[None]
        v.libraries = libs_minecraft

        if is_lwjgl_3:
            lwjgl_dependency = Dependency(uid=LWJGL3_COMPONENT)
        else:
            lwjgl_dependency = Dependency(uid=LWJGL_COMPONENT)
        if len(buckets) == 1:
            suggested_version = next(iter(buckets.values())).version
            if is_lwjgl_3:
                lwjgl_dependency.suggests = suggested_version
            else:
                lwjgl_dependency.suggests = '2.9.4-nightly-20150209'
        else:
            bad_versions = {'3.1.6', '3.2.1'}
            our_versions = set()

            for lwjgl in iter(buckets.values()):
                our_versions = our_versions.union({lwjgl.version})

            if our_versions == bad_versions:
                print("Found broken 3.1.6/3.2.1 combo, forcing LWJGL to 3.2.1")
                suggested_version = '3.2.1'
                lwjgl_dependency.suggests = suggested_version
            else:
                raise Exception("ERROR: cannot determine single suggested LWJGL version in %s" % mojang_version.id)

        # if it uses LWJGL 3, add the trait that enables starting on first thread on macOS
        if is_lwjgl_3:
            if not v.additional_traits:
                v.additional_traits = []
            v.additional_traits.append("FirstThreadOnMacOS")
        v.requires = [lwjgl_dependency]
        v.order = -2
        # process 1.13 arguments into previous version
        if not mojang_version.minecraft_arguments and mojang_version.arguments:
            v.minecraft_arguments = adapt_new_style_arguments(mojang_version.arguments)
        out_filename = os.path.join(PMC_DIR, MINECRAFT_COMPONENT, f"{v.version}.json")
        if v.version in override_index.versions:
            override = override_index.versions[v.version]
            override.apply_onto_meta_version(v)
        v.write(out_filename)
    print("#"*50)
    for version, variants in lwjglVersionVariants.items():
        variants: List[LWJGLEntry]
        print("%d variant(s) for LWJGL %s:" % (len(variants), version))
        # debugging
        variantVers = []
        for variant in variants:
            variantVers.append(variant.version.version)
        print("which are: " + ', '.join((variantVers)))
        success = False
        # try all variants until one works, starting from newest
        for variant in sorted(variants, key=lambda v: v.version.release_time, reverse=True):
            if process_single_variant(variant.version):
                print("Variant %s accepted." % variant.version.version)
                success = True
                break
        if not success:
            raise Exception(f"No variant passed for version {version}.")

    lwjgl_package = MetaPackage(uid=LWJGL_COMPONENT, name='LWJGL 2')
    lwjgl_package.recommended = ['2.9.4-nightly-20150209']
    lwjgl_package.write(os.path.join(PMC_DIR, LWJGL_COMPONENT, "package.json"))

    if found_any_lwjgl3:
        lwjgl_package = MetaPackage(uid=LWJGL3_COMPONENT, name='LWJGL 3')
        lwjgl_package.recommended = ['3.3.1']
        lwjgl_package.write(os.path.join(PMC_DIR, LWJGL3_COMPONENT, "package.json"))

    mojang_index = MojangIndexWrap(MojangIndex.parse_file(os.path.join(UPSTREAM_DIR, VERSION_MANIFEST_FILE)))

    minecraft_package = MetaPackage(uid=MINECRAFT_COMPONENT, name='Minecraft')
    minecraft_package.recommended = [mojang_index.latest.release]
    minecraft_package.write(os.path.join(PMC_DIR, MINECRAFT_COMPONENT, "package.json"))


if __name__ == '__main__':
    main()
