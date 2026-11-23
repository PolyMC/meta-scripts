"""Shared constants for the lwjgl3ify and Cleanroom profiles.

Ported from https://github.com/AngelicIndustries/multi3ify (commit 2cb12f4).
"""
from os.path import join

BASE_DIR = "multi3ify"
LWJGL3IFY_DIR = join(BASE_DIR, "lwjgl3ify")
CLEANROOM_DIR = join(BASE_DIR, "cleanroom")

# lwjgl3ify (Minecraft 1.7.10)
LWJGL3IFY_UID = "io.github.jackofnonetrades.lwjgl3ify"
LWJGL3IFY_MC_VERSION = "1.7.10-lwjgl3ify"
LWJGL3IFY_GAME_VERSION = "1.7.10"
LWJGL3IFY_RELEASES_API = "https://api.github.com/repos/GTNewHorizons/lwjgl3ify/releases"
LWJGL3IFY_MINIMUM = "3.0.0"
LWJGL3IFY_PATCH_UIDS = {"net.minecraft", "net.minecraftforge", "org.lwjgl3",
                        "me.eigenraven.lwjgl3ify.forgepatches", "me.eigenraven.lwjgl3ify.launchargs"}

# The helper installs the selected lwjgl3ify mod into mods/ before handing off
# to RetroFuturaBootstrap. Its source is static/multi3ify/Bootstrap.java.
BOOTSTRAP_CLASS = "io.github.jackofnonetrades.multi3ify.Bootstrap"
BOOTSTRAP_VERSION = "010cd78fa19cce95"
BOOTSTRAP_GROUP_PATH = "io/github/jackofnonetrades/multi3ify-bootstrap"
BOOTSTRAP_MAVEN_DIR = "maven"

# Cleanroom (Minecraft 1.12.2)
CLEANROOM_UID = "io.github.jackofnonetrades.cleanroom"
CLEANROOM_MC_VERSION = "1.12.2-cleanroom"
CLEANROOM_GAME_VERSION = "1.12.2"
CLEANROOM_BRIDGE_VERSION = "1.12.2-cleanroom-latest"
CLEANROOM_MAIN_CLASS = "top.outlands.foundation.boot.Foundation"
CLEANROOM_RELEASES_API = "https://api.github.com/repos/CleanroomMC/Cleanroom/releases"
CLEANROOM_MINIMUM = "0.6.13-alpha"
CLEANROOM_JAVA_NAMES = {25: "java-runtime-epsilon"}
CLEANROOM_LWJGL2_LIBRARIES = {
    "net.java.jinput:jinput", "net.java.jinput:jinput-platform", "net.java.jutils:jutils",
    "org.lwjgl.lwjgl:lwjgl", "org.lwjgl.lwjgl:lwjgl-platform", "org.lwjgl.lwjgl:lwjgl_util",
}

PATCH_FIELDS = {
    "formatVersion", "uid", "version", "name", "order", "releaseTime", "type", "volatile",
    "requires", "conflicts", "libraries", "+jvmArgs", "+tweakers", "+traits", "mainClass",
    "compatibleJavaMajors", "compatibleJavaName", "mainJar", "minecraftArguments", "assetIndex",
}
