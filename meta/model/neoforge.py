from typing import Optional, List, Dict, Any

from pydantic import Field

from . import MetaBase, MojangLibrary, GradleSpecifier
from .forge import DataSpec, ProcessorSpec


class NeoForgeEntry(MetaBase):
    version: str
    mc_version: str
    latest: bool
    installer_sha1: Optional[str]
    installer_size: Optional[int]

    @staticmethod
    def from_obj(obj: Dict):
        return NeoForgeEntry(
            version=obj["version"],
            mc_version=obj["mc_version"],
            latest=obj["latest"],
            installer_sha1=obj["installer_sha1"],
            installer_size=obj["installer_size"]
        )

    def sane_version(self):
        return self.version.split('-')[1] if self.mc_version == "1.20.1" else self.version

    def installer_filename(self):
        return f"{"forge" if self.mc_version == "1.20.1" else "neoforge"}-{self.version}-installer.jar"

    def installer_url(self):
        name = "forge" if self.mc_version == "1.20.1" else "neoforge"
        return f"https://maven.neoforged.net/releases/net/neoforged/{name}/{self.version}/{self.installer_filename()}"


class NeoForgeInstallerProfile(MetaBase):
    _comment: Optional[List[str]]
    spec: Optional[int]
    profile: Optional[str]
    version: Optional[str]
    icon: Optional[str]
    json_data: Optional[str] = Field(alias="json")
    path: Optional[GradleSpecifier]
    logo: Optional[str]
    minecraft: Optional[str]
    welcome: Optional[str]
    data: Optional[Dict[str, DataSpec]]
    processors: Optional[List[ProcessorSpec]]
    libraries: Optional[List[MojangLibrary]]
    mirror_list: Optional[str] = Field(alias="mirrorList")
    server_jar_path: Optional[str] = Field(alias="serverJarPath")
