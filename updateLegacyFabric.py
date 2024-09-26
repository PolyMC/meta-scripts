import hashlib
import json
import os
import zipfile
from datetime import datetime

import requests
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache

from meta.common import upstream_path, ensure_upstream_dir, transform_maven_key
from meta.common.fabric import JARS_DIR, INSTALLER_INFO_DIR, META_DIR, DATETIME_FORMAT_HTTP
from meta.model.fabric import FabricJarInfo

UPSTREAM_DIR = upstream_path()

ensure_upstream_dir(JARS_DIR)
ensure_upstream_dir(INSTALLER_INFO_DIR)
ensure_upstream_dir(META_DIR)

forever_cache = FileCache('caches/http_cache', forever=True)
sess = CacheControl(requests.Session(), forever_cache)


def filehash(filename, hashtype, blocksize=65536):
    h = hashtype()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            h.update(block)
    return h.hexdigest()


def get_maven_url(maven_key, server, ext):
    parts = maven_key.split(":", 3)
    maven_ver_url = server + parts[0].replace(".", "/") + "/" + parts[1] + "/" + parts[2] + "/"
    maven_url = maven_ver_url + parts[1] + "-" + parts[2] + ext
    return maven_url


def get_json_file(path, url):
    with open(path, 'w', encoding='utf-8') as f:
        r = sess.get(url)
        r.raise_for_status()
        version_json = r.json()
        json.dump(version_json, f, sort_keys=True, indent=4)
        return version_json


def get_plaintext(url):
    r = sess.get(url)
    r.raise_for_status()
    return r.text


def head_file(url):
    r = sess.head(url)
    r.raise_for_status()
    return r.headers


def get_binary_file(path, url):
    with open(path, 'wb') as f:
        r = sess.get(url)
        r.raise_for_status()
        for chunk in r.iter_content(chunk_size=128):
            f.write(chunk)


def compute_jar_file(path, url):
    # These two approaches should result in the same metadata, except for the timestamp which might be a few minutes
    # off for the fallback method
    try:
        # Let's not download a Jar file if we don't need to.
        headers = head_file(url)
        tstamp = datetime.strptime(headers["Last-Modified"], DATETIME_FORMAT_HTTP)
        sha1 = get_plaintext(url + ".sha1")
        sha256 = get_plaintext(url + ".sha256")
        size = int(headers["Content-Length"])
    except requests.HTTPError:
        # Some older versions don't have a .sha256 file :(
        print(f"Falling back to downloading jar for {url}")

        jar_path = path + ".jar"
        get_binary_file(jar_path, url)
        tstamp = datetime.fromtimestamp(0)
        with zipfile.ZipFile(jar_path) as jar:
            allinfo = jar.infolist()
            for info in allinfo:
                tstamp_new = datetime(*info.date_time)
                if tstamp_new > tstamp:
                    tstamp = tstamp_new

        sha1 = filehash(jar_path, hashlib.sha1)
        sha256 = filehash(jar_path, hashlib.sha256)
        size = os.path.getsize(jar_path)

    data = FabricJarInfo(release_time=tstamp, sha1=sha1, sha256=sha256, size=size)
    data.write(path + ".json")


def main():
    # get the version list for each component we are interested in
    for component in ["intermediary", "loader"]:
        index = get_json_file(os.path.join(UPSTREAM_DIR, META_DIR, f"{component}.json"),
                              "https://meta.legacyfabric.net/v2/versions/" + component)
        for it in index:
            print(f"Processing {component} {it['version']} ")
            jar_maven_url = get_maven_url(it["maven"], "https://maven.legacyfabric.net/", ".jar")
            compute_jar_file(os.path.join(UPSTREAM_DIR, JARS_DIR, transform_maven_key(it["maven"])), jar_maven_url)

    # for each loader, download installer JSON file from maven
    with open(os.path.join(UPSTREAM_DIR, META_DIR, "loader.json"), 'r', encoding='utf-8') as loaderVersionIndexFile:
        loader_version_index = json.load(loaderVersionIndexFile)
        for it in loader_version_index:
            print(f"Downloading installer info for loader {it['version']} ")
            maven_url = get_maven_url(it["maven"], "https://maven.legacyfabric.net/", ".json")
            get_json_file(os.path.join(UPSTREAM_DIR, INSTALLER_INFO_DIR, f"{it['version']}.json"), maven_url)


if __name__ == '__main__':
    main()
