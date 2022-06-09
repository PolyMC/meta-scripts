def get_lib_patches():
    return {
        "osx-arm64": [
            {
                "downloads": {
                    "artifact": {
                        "sha1": "f378f889797edd7df8d32272c06ca80a1b6b0f58",
                        "size": 13164,
                        "url": "https://libraries.minecraft.net/com/mojang/text2speech/1.11.3/text2speech-1.11.3.jar",
                    }
                },
                "name": "com.mojang:text2speech:1.11.3",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "369a83621e3c65496348491e533cb97fe5f2f37d",
                        "size": 91947,
                        "url": "https://github.com/MinecraftMachina/Java-Objective-C-Bridge/releases/download/1.1.0-mmachina.1/java-objc-bridge-1.1.jar",
                    }
                },
                "name": "ca.weblite:java-objc-bridge:1.1.0",
            },
            {
                "downloads": {
                    "classifiers": {
                        "natives-osx": {
                            "sha1": "53f9c919f34d2ca9de8c51fc4e1e8282029a9232",
                            "size": 12186,
                            "url": "https://libraries.minecraft.net/net/java/jinput/jinput-platform/2.0.5/jinput-platform-2.0.5-natives-osx.jar",
                        }
                    }
                },
                "extract": {"exclude": ["META-INF/"]},
                "name": "net.java.jinput:jinput-platform:2.0.5",
                "natives": {"osx": "natives-osx"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "39c7796b469a600f72380316f6b1f11db6c2c7c4",
                        "size": 208338,
                        "url": "https://libraries.minecraft.net/net/java/jinput/jinput/2.0.5/jinput-2.0.5.jar",
                    }
                },
                "name": "net.java.jinput:jinput:2.0.5",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "e12fe1fda814bd348c1579329c86943d2cd3c6a6",
                        "size": 7508,
                        "url": "https://libraries.minecraft.net/net/java/jutils/jutils/1.0.0/jutils-1.0.0.jar",
                    }
                },
                "name": "net.java.jutils:jutils:1.0.0",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "b04f3ee8f5e43fa3b162981b50bb72fe1acabb33",
                        "size": 22,
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl-platform/2.9.4-nightly-20150209/lwjgl-platform-2.9.4-nightly-20150209.jar",
                    },
                    "classifiers": {
                        "natives-osx": {
                            "sha1": "eff546c0b319d6ffc7a835652124c18089c67f36",
                            "size": 488316,
                            "url": "https://github.com/MinecraftMachina/lwjgl/releases/download/2.9.4-20150209-mmachina.2/lwjgl-platform-2.9.4-nightly-20150209-natives-osx.jar",
                        }
                    },
                },
                "extract": {"exclude": ["META-INF/"]},
                "name": "org.lwjgl.lwjgl:lwjgl-platform:2.9.4-nightly-20150209",
                "natives": {"osx": "natives-osx"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "697517568c68e78ae0b4544145af031c81082dfe",
                        "size": 1047168,
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl/2.9.4-nightly-20150209/lwjgl-2.9.4-nightly-20150209.jar",
                    }
                },
                "name": "org.lwjgl.lwjgl:lwjgl:2.9.4-nightly-20150209",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "d51a7c040a721d13efdfbd34f8b257b2df882ad0",
                        "size": 173887,
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl_util/2.9.4-nightly-20150209/lwjgl_util-2.9.4-nightly-20150209.jar",
                    }
                },
                "name": "org.lwjgl.lwjgl:lwjgl_util:2.9.4-nightly-20150209",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "b04f3ee8f5e43fa3b162981b50bb72fe1acabb33",
                        "size": 22,
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl-platform/2.9.4-nightly-20150209/lwjgl-platform-2.9.4-nightly-20150209.jar",
                    },
                    "classifiers": {
                        "natives-osx": {
                            "sha1": "eff546c0b319d6ffc7a835652124c18089c67f36",
                            "size": 488316,
                            "url": "https://github.com/MinecraftMachina/lwjgl/releases/download/2.9.4-20150209-mmachina.2/lwjgl-platform-2.9.4-nightly-20150209-natives-osx.jar",
                        }
                    },
                },
                "extract": {"exclude": ["META-INF/"]},
                "name": "org.lwjgl.lwjgl:lwjgl-platform:2.9.1-nightly-20131017",
                "natives": {"osx": "natives-osx"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "697517568c68e78ae0b4544145af031c81082dfe",
                        "size": 1047168,
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl/2.9.4-nightly-20150209/lwjgl-2.9.4-nightly-20150209.jar",
                    }
                },
                "name": "org.lwjgl.lwjgl:lwjgl:2.9.1-nightly-20131017",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "d51a7c040a721d13efdfbd34f8b257b2df882ad0",
                        "size": 173887,
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl_util/2.9.4-nightly-20150209/lwjgl_util-2.9.4-nightly-20150209.jar",
                    }
                },
                "name": "org.lwjgl.lwjgl:lwjgl_util:2.9.1-nightly-20131017",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "b04f3ee8f5e43fa3b162981b50bb72fe1acabb33",
                        "size": 22,
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl-platform/2.9.4-nightly-20150209/lwjgl-platform-2.9.4-nightly-20150209.jar",
                    },
                    "classifiers": {
                        "natives-osx": {
                            "sha1": "eff546c0b319d6ffc7a835652124c18089c67f36",
                            "size": 488316,
                            "url": "https://github.com/MinecraftMachina/lwjgl/releases/download/2.9.4-20150209-mmachina.2/lwjgl-platform-2.9.4-nightly-20150209-natives-osx.jar",
                        }
                    },
                },
                "extract": {"exclude": ["META-INF/"]},
                "name": "org.lwjgl.lwjgl:lwjgl-platform:2.9.1",
                "natives": {"osx": "natives-osx"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "697517568c68e78ae0b4544145af031c81082dfe",
                        "size": 1047168,
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl/2.9.4-nightly-20150209/lwjgl-2.9.4-nightly-20150209.jar",
                    }
                },
                "name": "org.lwjgl.lwjgl:lwjgl:2.9.1",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "d51a7c040a721d13efdfbd34f8b257b2df882ad0",
                        "size": 173887,
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl_util/2.9.4-nightly-20150209/lwjgl_util-2.9.4-nightly-20150209.jar",
                    }
                },
                "name": "org.lwjgl.lwjgl:lwjgl_util:2.9.1",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "b04f3ee8f5e43fa3b162981b50bb72fe1acabb33",
                        "size": 22,
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl-platform/2.9.4-nightly-20150209/lwjgl-platform-2.9.4-nightly-20150209.jar",
                    },
                    "classifiers": {
                        "natives-osx": {
                            "sha1": "eff546c0b319d6ffc7a835652124c18089c67f36",
                            "size": 488316,
                            "url": "https://github.com/MinecraftMachina/lwjgl/releases/download/2.9.4-20150209-mmachina.2/lwjgl-platform-2.9.4-nightly-20150209-natives-osx.jar",
                        }
                    },
                },
                "extract": {"exclude": ["META-INF/"]},
                "name": "org.lwjgl.lwjgl:lwjgl-platform:2.9.1-nightly-20130708-debug3",
                "natives": {"osx": "natives-osx"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "697517568c68e78ae0b4544145af031c81082dfe",
                        "size": 1047168,
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl/2.9.4-nightly-20150209/lwjgl-2.9.4-nightly-20150209.jar",
                    }
                },
                "name": "org.lwjgl.lwjgl:lwjgl:2.9.1-nightly-20130708-debug3",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "d51a7c040a721d13efdfbd34f8b257b2df882ad0",
                        "size": 173887,
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl_util/2.9.4-nightly-20150209/lwjgl_util-2.9.4-nightly-20150209.jar",
                    }
                },
                "name": "org.lwjgl.lwjgl:lwjgl_util:2.9.1-nightly-20130708-debug3",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "b04f3ee8f5e43fa3b162981b50bb72fe1acabb33",
                        "size": 22,
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl-platform/2.9.4-nightly-20150209/lwjgl-platform-2.9.4-nightly-20150209.jar",
                    },
                    "classifiers": {
                        "natives-osx": {
                            "sha1": "eff546c0b319d6ffc7a835652124c18089c67f36",
                            "size": 488316,
                            "url": "https://github.com/MinecraftMachina/lwjgl/releases/download/2.9.4-20150209-mmachina.2/lwjgl-platform-2.9.4-nightly-20150209-natives-osx.jar",
                        }
                    },
                },
                "extract": {"exclude": ["META-INF/"]},
                "name": "org.lwjgl.lwjgl:lwjgl-platform:2.9.2-nightly-20140822",
                "natives": {"osx": "natives-osx"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "697517568c68e78ae0b4544145af031c81082dfe",
                        "size": 1047168,
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl/2.9.4-nightly-20150209/lwjgl-2.9.4-nightly-20150209.jar",
                    }
                },
                "name": "org.lwjgl.lwjgl:lwjgl:2.9.2-nightly-20140822",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "d51a7c040a721d13efdfbd34f8b257b2df882ad0",
                        "size": 173887,
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl_util/2.9.4-nightly-20150209/lwjgl_util-2.9.4-nightly-20150209.jar",
                    }
                },
                "name": "org.lwjgl.lwjgl:lwjgl_util:2.9.2-nightly-20140822",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "b04f3ee8f5e43fa3b162981b50bb72fe1acabb33",
                        "size": 22,
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl-platform/2.9.4-nightly-20150209/lwjgl-platform-2.9.4-nightly-20150209.jar",
                    },
                    "classifiers": {
                        "natives-osx": {
                            "sha1": "eff546c0b319d6ffc7a835652124c18089c67f36",
                            "size": 488316,
                            "url": "https://github.com/MinecraftMachina/lwjgl/releases/download/2.9.4-20150209-mmachina.2/lwjgl-platform-2.9.4-nightly-20150209-natives-osx.jar",
                        }
                    },
                },
                "extract": {"exclude": ["META-INF/"]},
                "name": "org.lwjgl.lwjgl:lwjgl-platform:2.9.1-nightly-20131120",
                "natives": {"osx": "natives-osx"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "697517568c68e78ae0b4544145af031c81082dfe",
                        "size": 1047168,
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl/2.9.4-nightly-20150209/lwjgl-2.9.4-nightly-20150209.jar",
                    }
                },
                "name": "org.lwjgl.lwjgl:lwjgl:2.9.1-nightly-20131120",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "d51a7c040a721d13efdfbd34f8b257b2df882ad0",
                        "size": 173887,
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl_util/2.9.4-nightly-20150209/lwjgl_util-2.9.4-nightly-20150209.jar",
                    }
                },
                "name": "org.lwjgl.lwjgl:lwjgl_util:2.9.1-nightly-20131120",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "e9a101bca4fa30d26b21b526ff28e7c2d8927f1b",
                        "size": 130128,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-glfw.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl-glfw:3.3.1",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "e9a101bca4fa30d26b21b526ff28e7c2d8927f1b",
                        "size": 130128,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-glfw.jar",
                    },
                    "classifiers": {
                        "natives-macos": {
                            "sha1": "71d793d0a5a42e3dfe78eb882abc2523a2c6b496",
                            "size": 129076,
                            "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-glfw-natives-macos-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl-glfw:3.3.1",
                "natives": {"osx": "natives-macos"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "4fb94224378d3588d52d2beb172f2eeafea2d546",
                        "size": 36976,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-jemalloc.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl-jemalloc:3.3.1",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "4fb94224378d3588d52d2beb172f2eeafea2d546",
                        "size": 36976,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-jemalloc.jar",
                    },
                    "classifiers": {
                        "natives-macos": {
                            "sha1": "b0be721188d2e7195798780b1c5fe7eafe8091c1",
                            "size": 103478,
                            "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-jemalloc-natives-macos-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl-jemalloc:3.3.1",
                "natives": {"osx": "natives-macos"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "d48e753d85916fc8a200ccddc709b36e3865cc4e",
                        "size": 88880,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-openal.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl-openal:3.3.1",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "d48e753d85916fc8a200ccddc709b36e3865cc4e",
                        "size": 88880,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-openal.jar",
                    },
                    "classifiers": {
                        "natives-macos": {
                            "sha1": "6b80fc0b982a0723b141e88859c42d6f71bd723f",
                            "size": 346131,
                            "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-openal-natives-macos-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl-openal:3.3.1",
                "natives": {"osx": "natives-macos"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "962c2a8d2a8cdd3b89de3d78d766ab5e2133c2f4",
                        "size": 929233,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-opengl.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl-opengl:3.3.1",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "962c2a8d2a8cdd3b89de3d78d766ab5e2133c2f4",
                        "size": 929233,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-opengl.jar",
                    },
                    "classifiers": {
                        "natives-macos": {
                            "sha1": "bb575058e0372f515587b5d2d04ff7db185f3ffe",
                            "size": 41667,
                            "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-opengl-natives-macos-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl-opengl:3.3.1",
                "natives": {"osx": "natives-macos"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "703e4b533e2542560e9f94d6d8bd148be1c1d572",
                        "size": 113273,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-stb.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl-stb:3.3.1",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "703e4b533e2542560e9f94d6d8bd148be1c1d572",
                        "size": 113273,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-stb.jar",
                    },
                    "classifiers": {
                        "natives-macos": {
                            "sha1": "98f0ad956c754723ef354d50057cc30417ef376a",
                            "size": 178409,
                            "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-stb-natives-macos-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl-stb:3.3.1",
                "natives": {"osx": "natives-macos"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "1203660b3131cbb8681b17ce6437412545be95e0",
                        "size": 6802,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-tinyfd.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl-tinyfd:3.3.1",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "1203660b3131cbb8681b17ce6437412545be95e0",
                        "size": 6802,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-tinyfd.jar",
                    },
                    "classifiers": {
                        "natives-macos": {
                            "sha1": "015b931a2daba8f0c317d84c9d14e8e98ae56e0c",
                            "size": 41384,
                            "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-tinyfd-natives-macos-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl-tinyfd:3.3.1",
                "natives": {"osx": "natives-macos"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "8e664dd69ad7bbcf2053da23efc7848e39e498db",
                        "size": 719038,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl:3.3.1",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "8e664dd69ad7bbcf2053da23efc7848e39e498db",
                        "size": 719038,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl.jar",
                    },
                    "classifiers": {
                        "natives-macos": {
                            "sha1": "984df31fadaab86838877b112e5b4e4f68a00ccf",
                            "size": 42693,
                            "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-natives-macos-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl:3.3.1",
                "natives": {"osx": "natives-macos"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "e9a101bca4fa30d26b21b526ff28e7c2d8927f1b",
                        "size": 130128,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-glfw.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl-glfw:3.2.2",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "e9a101bca4fa30d26b21b526ff28e7c2d8927f1b",
                        "size": 130128,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-glfw.jar",
                    },
                    "classifiers": {
                        "natives-macos": {
                            "sha1": "71d793d0a5a42e3dfe78eb882abc2523a2c6b496",
                            "size": 129076,
                            "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-glfw-natives-macos-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl-glfw:3.2.2",
                "natives": {"osx": "natives-macos"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "4fb94224378d3588d52d2beb172f2eeafea2d546",
                        "size": 36976,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-jemalloc.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl-jemalloc:3.2.2",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "4fb94224378d3588d52d2beb172f2eeafea2d546",
                        "size": 36976,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-jemalloc.jar",
                    },
                    "classifiers": {
                        "natives-macos": {
                            "sha1": "b0be721188d2e7195798780b1c5fe7eafe8091c1",
                            "size": 103478,
                            "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-jemalloc-natives-macos-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl-jemalloc:3.2.2",
                "natives": {"osx": "natives-macos"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "d48e753d85916fc8a200ccddc709b36e3865cc4e",
                        "size": 88880,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-openal.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl-openal:3.2.2",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "d48e753d85916fc8a200ccddc709b36e3865cc4e",
                        "size": 88880,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-openal.jar",
                    },
                    "classifiers": {
                        "natives-macos": {
                            "sha1": "6b80fc0b982a0723b141e88859c42d6f71bd723f",
                            "size": 346131,
                            "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-openal-natives-macos-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl-openal:3.2.2",
                "natives": {"osx": "natives-macos"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "962c2a8d2a8cdd3b89de3d78d766ab5e2133c2f4",
                        "size": 929233,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-opengl.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl-opengl:3.2.2",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "962c2a8d2a8cdd3b89de3d78d766ab5e2133c2f4",
                        "size": 929233,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-opengl.jar",
                    },
                    "classifiers": {
                        "natives-macos": {
                            "sha1": "bb575058e0372f515587b5d2d04ff7db185f3ffe",
                            "size": 41667,
                            "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-opengl-natives-macos-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl-opengl:3.2.2",
                "natives": {"osx": "natives-macos"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "703e4b533e2542560e9f94d6d8bd148be1c1d572",
                        "size": 113273,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-stb.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl-stb:3.2.2",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "703e4b533e2542560e9f94d6d8bd148be1c1d572",
                        "size": 113273,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-stb.jar",
                    },
                    "classifiers": {
                        "natives-macos": {
                            "sha1": "98f0ad956c754723ef354d50057cc30417ef376a",
                            "size": 178409,
                            "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-stb-natives-macos-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl-stb:3.2.2",
                "natives": {"osx": "natives-macos"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "1203660b3131cbb8681b17ce6437412545be95e0",
                        "size": 6802,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-tinyfd.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl-tinyfd:3.2.2",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "1203660b3131cbb8681b17ce6437412545be95e0",
                        "size": 6802,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-tinyfd.jar",
                    },
                    "classifiers": {
                        "natives-macos": {
                            "sha1": "015b931a2daba8f0c317d84c9d14e8e98ae56e0c",
                            "size": 41384,
                            "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-tinyfd-natives-macos-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl-tinyfd:3.2.2",
                "natives": {"osx": "natives-macos"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "8e664dd69ad7bbcf2053da23efc7848e39e498db",
                        "size": 719038,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl:3.2.2",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "8e664dd69ad7bbcf2053da23efc7848e39e498db",
                        "size": 719038,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl.jar",
                    },
                    "classifiers": {
                        "natives-macos": {
                            "sha1": "984df31fadaab86838877b112e5b4e4f68a00ccf",
                            "size": 42693,
                            "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-natives-macos-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl:3.2.2",
                "natives": {"osx": "natives-macos"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "e9a101bca4fa30d26b21b526ff28e7c2d8927f1b",
                        "size": 130128,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-glfw.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl-glfw:3.2.1",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "e9a101bca4fa30d26b21b526ff28e7c2d8927f1b",
                        "size": 130128,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-glfw.jar",
                    },
                    "classifiers": {
                        "natives-macos": {
                            "sha1": "71d793d0a5a42e3dfe78eb882abc2523a2c6b496",
                            "size": 129076,
                            "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-glfw-natives-macos-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl-glfw:3.2.1",
                "natives": {"osx": "natives-macos"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "4fb94224378d3588d52d2beb172f2eeafea2d546",
                        "size": 36976,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-jemalloc.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl-jemalloc:3.2.1",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "4fb94224378d3588d52d2beb172f2eeafea2d546",
                        "size": 36976,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-jemalloc.jar",
                    },
                    "classifiers": {
                        "natives-macos": {
                            "sha1": "b0be721188d2e7195798780b1c5fe7eafe8091c1",
                            "size": 103478,
                            "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-jemalloc-natives-macos-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl-jemalloc:3.2.1",
                "natives": {"osx": "natives-macos"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "d48e753d85916fc8a200ccddc709b36e3865cc4e",
                        "size": 88880,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-openal.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl-openal:3.2.1",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "d48e753d85916fc8a200ccddc709b36e3865cc4e",
                        "size": 88880,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-openal.jar",
                    },
                    "classifiers": {
                        "natives-macos": {
                            "sha1": "6b80fc0b982a0723b141e88859c42d6f71bd723f",
                            "size": 346131,
                            "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-openal-natives-macos-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl-openal:3.2.1",
                "natives": {"osx": "natives-macos"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "962c2a8d2a8cdd3b89de3d78d766ab5e2133c2f4",
                        "size": 929233,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-opengl.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl-opengl:3.2.1",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "962c2a8d2a8cdd3b89de3d78d766ab5e2133c2f4",
                        "size": 929233,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-opengl.jar",
                    },
                    "classifiers": {
                        "natives-macos": {
                            "sha1": "bb575058e0372f515587b5d2d04ff7db185f3ffe",
                            "size": 41667,
                            "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-opengl-natives-macos-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl-opengl:3.2.1",
                "natives": {"osx": "natives-macos"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "703e4b533e2542560e9f94d6d8bd148be1c1d572",
                        "size": 113273,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-stb.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl-stb:3.2.1",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "703e4b533e2542560e9f94d6d8bd148be1c1d572",
                        "size": 113273,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-stb.jar",
                    },
                    "classifiers": {
                        "natives-macos": {
                            "sha1": "98f0ad956c754723ef354d50057cc30417ef376a",
                            "size": 178409,
                            "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-stb-natives-macos-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl-stb:3.2.1",
                "natives": {"osx": "natives-macos"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "1203660b3131cbb8681b17ce6437412545be95e0",
                        "size": 6802,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-tinyfd.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl-tinyfd:3.2.1",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "1203660b3131cbb8681b17ce6437412545be95e0",
                        "size": 6802,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-tinyfd.jar",
                    },
                    "classifiers": {
                        "natives-macos": {
                            "sha1": "015b931a2daba8f0c317d84c9d14e8e98ae56e0c",
                            "size": 41384,
                            "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-tinyfd-natives-macos-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl-tinyfd:3.2.1",
                "natives": {"osx": "natives-macos"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "8e664dd69ad7bbcf2053da23efc7848e39e498db",
                        "size": 719038,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl:3.2.1",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "8e664dd69ad7bbcf2053da23efc7848e39e498db",
                        "size": 719038,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl.jar",
                    },
                    "classifiers": {
                        "natives-macos": {
                            "sha1": "984df31fadaab86838877b112e5b4e4f68a00ccf",
                            "size": 42693,
                            "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-natives-macos-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl:3.2.1",
                "natives": {"osx": "natives-macos"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "e9a101bca4fa30d26b21b526ff28e7c2d8927f1b",
                        "size": 130128,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-glfw.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl-glfw:3.1.6",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "e9a101bca4fa30d26b21b526ff28e7c2d8927f1b",
                        "size": 130128,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-glfw.jar",
                    },
                    "classifiers": {
                        "natives-macos": {
                            "sha1": "71d793d0a5a42e3dfe78eb882abc2523a2c6b496",
                            "size": 129076,
                            "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-glfw-natives-macos-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl-glfw:3.1.6",
                "natives": {"osx": "natives-macos"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "4fb94224378d3588d52d2beb172f2eeafea2d546",
                        "size": 36976,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-jemalloc.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl-jemalloc:3.1.6",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "4fb94224378d3588d52d2beb172f2eeafea2d546",
                        "size": 36976,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-jemalloc.jar",
                    },
                    "classifiers": {
                        "natives-macos": {
                            "sha1": "b0be721188d2e7195798780b1c5fe7eafe8091c1",
                            "size": 103478,
                            "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-jemalloc-natives-macos-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl-jemalloc:3.1.6",
                "natives": {"osx": "natives-macos"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "d48e753d85916fc8a200ccddc709b36e3865cc4e",
                        "size": 88880,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-openal.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl-openal:3.1.6",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "d48e753d85916fc8a200ccddc709b36e3865cc4e",
                        "size": 88880,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-openal.jar",
                    },
                    "classifiers": {
                        "natives-macos": {
                            "sha1": "6b80fc0b982a0723b141e88859c42d6f71bd723f",
                            "size": 346131,
                            "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-openal-natives-macos-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl-openal:3.1.6",
                "natives": {"osx": "natives-macos"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "962c2a8d2a8cdd3b89de3d78d766ab5e2133c2f4",
                        "size": 929233,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-opengl.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl-opengl:3.1.6",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "962c2a8d2a8cdd3b89de3d78d766ab5e2133c2f4",
                        "size": 929233,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-opengl.jar",
                    },
                    "classifiers": {
                        "natives-macos": {
                            "sha1": "bb575058e0372f515587b5d2d04ff7db185f3ffe",
                            "size": 41667,
                            "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-opengl-natives-macos-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl-opengl:3.1.6",
                "natives": {"osx": "natives-macos"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "703e4b533e2542560e9f94d6d8bd148be1c1d572",
                        "size": 113273,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-stb.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl-stb:3.1.6",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "703e4b533e2542560e9f94d6d8bd148be1c1d572",
                        "size": 113273,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-stb.jar",
                    },
                    "classifiers": {
                        "natives-macos": {
                            "sha1": "98f0ad956c754723ef354d50057cc30417ef376a",
                            "size": 178409,
                            "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-stb-natives-macos-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl-stb:3.1.6",
                "natives": {"osx": "natives-macos"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "1203660b3131cbb8681b17ce6437412545be95e0",
                        "size": 6802,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-tinyfd.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl-tinyfd:3.1.6",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "1203660b3131cbb8681b17ce6437412545be95e0",
                        "size": 6802,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-tinyfd.jar",
                    },
                    "classifiers": {
                        "natives-macos": {
                            "sha1": "015b931a2daba8f0c317d84c9d14e8e98ae56e0c",
                            "size": 41384,
                            "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-tinyfd-natives-macos-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl-tinyfd:3.1.6",
                "natives": {"osx": "natives-macos"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "8e664dd69ad7bbcf2053da23efc7848e39e498db",
                        "size": 719038,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl:3.1.6",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "8e664dd69ad7bbcf2053da23efc7848e39e498db",
                        "size": 719038,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl.jar",
                    },
                    "classifiers": {
                        "natives-macos": {
                            "sha1": "984df31fadaab86838877b112e5b4e4f68a00ccf",
                            "size": 42693,
                            "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-natives-macos-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl:3.1.6",
                "natives": {"osx": "natives-macos"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "e9a101bca4fa30d26b21b526ff28e7c2d8927f1b",
                        "size": 130128,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-glfw.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl-glfw:3.1.2",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "e9a101bca4fa30d26b21b526ff28e7c2d8927f1b",
                        "size": 130128,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-glfw.jar",
                    },
                    "classifiers": {
                        "natives-macos": {
                            "sha1": "71d793d0a5a42e3dfe78eb882abc2523a2c6b496",
                            "size": 129076,
                            "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-glfw-natives-macos-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl-glfw:3.1.2",
                "natives": {"osx": "natives-macos"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "4fb94224378d3588d52d2beb172f2eeafea2d546",
                        "size": 36976,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-jemalloc.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl-jemalloc:3.1.2",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "4fb94224378d3588d52d2beb172f2eeafea2d546",
                        "size": 36976,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-jemalloc.jar",
                    },
                    "classifiers": {
                        "natives-macos": {
                            "sha1": "b0be721188d2e7195798780b1c5fe7eafe8091c1",
                            "size": 103478,
                            "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-jemalloc-natives-macos-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl-jemalloc:3.1.2",
                "natives": {"osx": "natives-macos"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "d48e753d85916fc8a200ccddc709b36e3865cc4e",
                        "size": 88880,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-openal.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl-openal:3.1.2",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "d48e753d85916fc8a200ccddc709b36e3865cc4e",
                        "size": 88880,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-openal.jar",
                    },
                    "classifiers": {
                        "natives-macos": {
                            "sha1": "6b80fc0b982a0723b141e88859c42d6f71bd723f",
                            "size": 346131,
                            "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-openal-natives-macos-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl-openal:3.1.2",
                "natives": {"osx": "natives-macos"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "962c2a8d2a8cdd3b89de3d78d766ab5e2133c2f4",
                        "size": 929233,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-opengl.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl-opengl:3.1.2",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "962c2a8d2a8cdd3b89de3d78d766ab5e2133c2f4",
                        "size": 929233,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-opengl.jar",
                    },
                    "classifiers": {
                        "natives-macos": {
                            "sha1": "bb575058e0372f515587b5d2d04ff7db185f3ffe",
                            "size": 41667,
                            "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-opengl-natives-macos-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl-opengl:3.1.2",
                "natives": {"osx": "natives-macos"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "703e4b533e2542560e9f94d6d8bd148be1c1d572",
                        "size": 113273,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-stb.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl-stb:3.1.2",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "703e4b533e2542560e9f94d6d8bd148be1c1d572",
                        "size": 113273,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-stb.jar",
                    },
                    "classifiers": {
                        "natives-macos": {
                            "sha1": "98f0ad956c754723ef354d50057cc30417ef376a",
                            "size": 178409,
                            "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-stb-natives-macos-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl-stb:3.1.2",
                "natives": {"osx": "natives-macos"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "1203660b3131cbb8681b17ce6437412545be95e0",
                        "size": 6802,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-tinyfd.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl-tinyfd:3.1.2",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "1203660b3131cbb8681b17ce6437412545be95e0",
                        "size": 6802,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-tinyfd.jar",
                    },
                    "classifiers": {
                        "natives-macos": {
                            "sha1": "015b931a2daba8f0c317d84c9d14e8e98ae56e0c",
                            "size": 41384,
                            "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-tinyfd-natives-macos-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl-tinyfd:3.1.2",
                "natives": {"osx": "natives-macos"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "8e664dd69ad7bbcf2053da23efc7848e39e498db",
                        "size": 719038,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl:3.1.2",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "8e664dd69ad7bbcf2053da23efc7848e39e498db",
                        "size": 719038,
                        "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl.jar",
                    },
                    "classifiers": {
                        "natives-macos": {
                            "sha1": "984df31fadaab86838877b112e5b4e4f68a00ccf",
                            "size": 42693,
                            "url": "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/lwjgl-natives-macos-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl:3.1.2",
                "natives": {"osx": "natives-macos"},
            },
        ],
        "linux-arm64": [
            {
                "downloads": {
                    "artifact": {
                        "sha1": "f378f889797edd7df8d32272c06ca80a1b6b0f58",
                        "size": 13164,
                        "url": "https://libraries.minecraft.net/com/mojang/text2speech/1.11.3/text2speech-1.11.3.jar",
                    }
                },
                "name": "com.mojang:text2speech:1.11.3",
            },
            {
                "downloads": {
                    "classifiers": {
                        "natives-linux": {
                            "sha1": "7ff832a6eb9ab6a767f1ade2b548092d0fa64795",
                            "size": 10362,
                            "url": "https://libraries.minecraft.net/net/java/jinput/jinput-platform/2.0.5/jinput-platform-2.0.5-natives-linux.jar",
                        }
                    }
                },
                "extract": {"exclude": ["META-INF/"]},
                "name": "net.java.jinput:jinput-platform:2.0.5",
                "natives": {"linux": "natives-linux"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "39c7796b469a600f72380316f6b1f11db6c2c7c4",
                        "size": 208338,
                        "url": "https://libraries.minecraft.net/net/java/jinput/jinput/2.0.5/jinput-2.0.5.jar",
                    }
                },
                "name": "net.java.jinput:jinput:2.0.5",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "e12fe1fda814bd348c1579329c86943d2cd3c6a6",
                        "size": 7508,
                        "url": "https://libraries.minecraft.net/net/java/jutils/jutils/1.0.0/jutils-1.0.0.jar",
                    }
                },
                "name": "net.java.jutils:jutils:1.0.0",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "b04f3ee8f5e43fa3b162981b50bb72fe1acabb33",
                        "size": 22,
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl-platform/2.9.4-nightly-20150209/lwjgl-platform-2.9.4-nightly-20150209.jar",
                    },
                    "classifiers": {
                        "natives-linux": {
                            "sha1": "ba120169db0180f4188ddf4b240668a41f11d35f",
                            "size": 480907,
                            "url": "https://github.com/r58Playz/lwjgl2-m1/raw/linux-aarch64-built/lwjgl-platform-2.9.4-nightly-20150209-natives-linux.jar",
                        }
                    },
                },
                "extract": {"exclude": ["META-INF/"]},
                "name": "org.lwjgl.lwjgl:lwjgl-platform:2.9.4-nightly-20150209",
                "natives": {"linux": "natives-linux"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "697517568c68e78ae0b4544145af031c81082dfe",
                        "size": 1047168,
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl/2.9.4-nightly-20150209/lwjgl-2.9.4-nightly-20150209.jar",
                    }
                },
                "name": "org.lwjgl.lwjgl:lwjgl:2.9.4-nightly-20150209",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "d51a7c040a721d13efdfbd34f8b257b2df882ad0",
                        "size": 173887,
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl_util/2.9.4-nightly-20150209/lwjgl_util-2.9.4-nightly-20150209.jar",
                    }
                },
                "name": "org.lwjgl.lwjgl:lwjgl_util:2.9.4-nightly-20150209",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "b04f3ee8f5e43fa3b162981b50bb72fe1acabb33",
                        "size": 22,
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl-platform/2.9.4-nightly-20150209/lwjgl-platform-2.9.4-nightly-20150209.jar",
                    },
                    "classifiers": {
                        "natives-linux": {
                            "sha1": "ba120169db0180f4188ddf4b240668a41f11d35f",
                            "size": 480907,
                            "url": "https://github.com/r58Playz/lwjgl2-m1/raw/linux-aarch64-built/lwjgl-platform-2.9.4-nightly-20150209-natives-linux.jar",
                        }
                    },
                },
                "extract": {"exclude": ["META-INF/"]},
                "name": "org.lwjgl.lwjgl:lwjgl-platform:2.9.1-nightly-20131017",
                "natives": {"linux": "natives-linux"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "697517568c68e78ae0b4544145af031c81082dfe",
                        "size": 1047168,
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl/2.9.4-nightly-20150209/lwjgl-2.9.4-nightly-20150209.jar",
                    }
                },
                "name": "org.lwjgl.lwjgl:lwjgl:2.9.1-nightly-20131017",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "d51a7c040a721d13efdfbd34f8b257b2df882ad0",
                        "size": 173887,
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl_util/2.9.4-nightly-20150209/lwjgl_util-2.9.4-nightly-20150209.jar",
                    }
                },
                "name": "org.lwjgl.lwjgl:lwjgl_util:2.9.1-nightly-20131017",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "b04f3ee8f5e43fa3b162981b50bb72fe1acabb33",
                        "size": 22,
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl-platform/2.9.4-nightly-20150209/lwjgl-platform-2.9.4-nightly-20150209.jar",
                    },
                    "classifiers": {
                        "natives-linux": {
                            "sha1": "ba120169db0180f4188ddf4b240668a41f11d35f",
                            "size": 480907,
                            "url": "https://github.com/r58Playz/lwjgl2-m1/raw/linux-aarch64-built/lwjgl-platform-2.9.4-nightly-20150209-natives-linux.jar",
                        }
                    },
                },
                "extract": {"exclude": ["META-INF/"]},
                "name": "org.lwjgl.lwjgl:lwjgl-platform:2.9.1",
                "natives": {"linux": "natives-linux"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "697517568c68e78ae0b4544145af031c81082dfe",
                        "size": 1047168,
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl/2.9.4-nightly-20150209/lwjgl-2.9.4-nightly-20150209.jar",
                    }
                },
                "name": "org.lwjgl.lwjgl:lwjgl:2.9.1",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "d51a7c040a721d13efdfbd34f8b257b2df882ad0",
                        "size": 173887,
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl_util/2.9.4-nightly-20150209/lwjgl_util-2.9.4-nightly-20150209.jar",
                    }
                },
                "name": "org.lwjgl.lwjgl:lwjgl_util:2.9.1",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "b04f3ee8f5e43fa3b162981b50bb72fe1acabb33",
                        "size": 22,
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl-platform/2.9.4-nightly-20150209/lwjgl-platform-2.9.4-nightly-20150209.jar",
                    },
                    "classifiers": {
                        "natives-linux": {
                            "sha1": "ba120169db0180f4188ddf4b240668a41f11d35f",
                            "size": 480907,
                            "url": "https://github.com/r58Playz/lwjgl2-m1/raw/linux-aarch64-built/lwjgl-platform-2.9.4-nightly-20150209-natives-linux.jar",
                        }
                    },
                },
                "extract": {"exclude": ["META-INF/"]},
                "name": "org.lwjgl.lwjgl:lwjgl-platform:2.9.1-nightly-20130708-debug3",
                "natives": {"linux": "natives-linux"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "697517568c68e78ae0b4544145af031c81082dfe",
                        "size": 1047168,
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl/2.9.4-nightly-20150209/lwjgl-2.9.4-nightly-20150209.jar",
                    }
                },
                "name": "org.lwjgl.lwjgl:lwjgl:2.9.1-nightly-20130708-debug3",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "d51a7c040a721d13efdfbd34f8b257b2df882ad0",
                        "size": 173887,
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl_util/2.9.4-nightly-20150209/lwjgl_util-2.9.4-nightly-20150209.jar",
                    }
                },
                "name": "org.lwjgl.lwjgl:lwjgl_util:2.9.1-nightly-20130708-debug3",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "b04f3ee8f5e43fa3b162981b50bb72fe1acabb33",
                        "size": 22,
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl-platform/2.9.4-nightly-20150209/lwjgl-platform-2.9.4-nightly-20150209.jar",
                    },
                    "classifiers": {
                        "natives-linux": {
                            "sha1": "ba120169db0180f4188ddf4b240668a41f11d35f",
                            "size": 480907,
                            "url": "https://github.com/r58Playz/lwjgl2-m1/raw/linux-aarch64-built/lwjgl-platform-2.9.4-nightly-20150209-natives-linux.jar",
                        }
                    },
                },
                "extract": {"exclude": ["META-INF/"]},
                "name": "org.lwjgl.lwjgl:lwjgl-platform:2.9.2-nightly-20140822",
                "natives": {"linux": "natives-linux"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "697517568c68e78ae0b4544145af031c81082dfe",
                        "size": 1047168,
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl/2.9.4-nightly-20150209/lwjgl-2.9.4-nightly-20150209.jar",
                    }
                },
                "name": "org.lwjgl.lwjgl:lwjgl:2.9.2-nightly-20140822",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "d51a7c040a721d13efdfbd34f8b257b2df882ad0",
                        "size": 173887,
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl_util/2.9.4-nightly-20150209/lwjgl_util-2.9.4-nightly-20150209.jar",
                    }
                },
                "name": "org.lwjgl.lwjgl:lwjgl_util:2.9.2-nightly-20140822",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "b04f3ee8f5e43fa3b162981b50bb72fe1acabb33",
                        "size": 22,
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl-platform/2.9.4-nightly-20150209/lwjgl-platform-2.9.4-nightly-20150209.jar",
                    },
                    "classifiers": {
                        "natives-linux": {
                            "sha1": "ba120169db0180f4188ddf4b240668a41f11d35f",
                            "size": 480907,
                            "url": "https://github.com/r58Playz/lwjgl2-m1/raw/linux-aarch64-built/lwjgl-platform-2.9.4-nightly-20150209-natives-linux.jar",
                        }
                    },
                },
                "extract": {"exclude": ["META-INF/"]},
                "name": "org.lwjgl.lwjgl:lwjgl-platform:2.9.1-nightly-20131120",
                "natives": {"linux": "natives-linux"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "697517568c68e78ae0b4544145af031c81082dfe",
                        "size": 1047168,
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl/2.9.4-nightly-20150209/lwjgl-2.9.4-nightly-20150209.jar",
                    }
                },
                "name": "org.lwjgl.lwjgl:lwjgl:2.9.1-nightly-20131120",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "d51a7c040a721d13efdfbd34f8b257b2df882ad0",
                        "size": 173887,
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl_util/2.9.4-nightly-20150209/lwjgl_util-2.9.4-nightly-20150209.jar",
                    }
                },
                "name": "org.lwjgl.lwjgl:lwjgl_util:2.9.1-nightly-20131120",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "cbac1b8d30cb4795149c1ef540f912671a8616d0",
                        "size": 128801,
                        "url": "https://build.lwjgl.org/release/3.3.1/bin/lwjgl-glfw/lwjgl-glfw.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl-glfw:3.3.1",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "cbac1b8d30cb4795149c1ef540f912671a8616d0",
                        "size": 128801,
                        "url": "https://build.lwjgl.org/release/3.3.1/bin/lwjgl-glfw/lwjgl-glfw.jar",
                    },
                    "classifiers": {
                        "natives-linux": {
                            "sha1": "513eb39b866d0fe131a18d5c517087805433b029",
                            "size": 112350,
                            "url": "https://build.lwjgl.org/release/3.3.1/bin/lwjgl-glfw/lwjgl-glfw-natives-linux-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl-glfw:3.3.1",
                "natives": {"linux": "natives-linux"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "a817bcf213db49f710603677457567c37d53e103",
                        "size": 36601,
                        "url": "https://build.lwjgl.org/release/3.3.1/bin/lwjgl-jemalloc/lwjgl-jemalloc.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl-jemalloc:3.3.1",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "a817bcf213db49f710603677457567c37d53e103",
                        "size": 36601,
                        "url": "https://build.lwjgl.org/release/3.3.1/bin/lwjgl-jemalloc/lwjgl-jemalloc.jar",
                    },
                    "classifiers": {
                        "natives-linux": {
                            "sha1": "c6606e57db075ad218a2e78d2416c159a53b6a0c",
                            "size": 157996,
                            "url": "https://build.lwjgl.org/release/3.3.1/bin/lwjgl-jemalloc/lwjgl-jemalloc-natives-linux-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl-jemalloc:3.3.1",
                "natives": {"linux": "natives-linux"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "2623a6b8ae1dfcd880738656a9f0243d2e6840bd",
                        "size": 88237,
                        "url": "https://build.lwjgl.org/release/3.3.1/bin/lwjgl-openal/lwjgl-openal.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl-openal:3.3.1",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "2623a6b8ae1dfcd880738656a9f0243d2e6840bd",
                        "size": 88237,
                        "url": "https://build.lwjgl.org/release/3.3.1/bin/lwjgl-openal/lwjgl-openal.jar",
                    },
                    "classifiers": {
                        "natives-linux": {
                            "sha1": "cf4e303257e82981b8b2e31bba3d7f8f7b8f42b2",
                            "size": 470743,
                            "url": "https://build.lwjgl.org/release/3.3.1/bin/lwjgl-openal/lwjgl-openal-natives-linux-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl-openal:3.3.1",
                "natives": {"linux": "natives-linux"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "831a5533a21a5f4f81bbc51bb13e9899319b5411",
                        "size": 921563,
                        "url": "https://build.lwjgl.org/release/3.3.1/bin/lwjgl-opengl/lwjgl-opengl.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl-opengl:3.3.1",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "831a5533a21a5f4f81bbc51bb13e9899319b5411",
                        "size": 921563,
                        "url": "https://build.lwjgl.org/release/3.3.1/bin/lwjgl-opengl/lwjgl-opengl.jar",
                    },
                    "classifiers": {
                        "natives-linux": {
                            "sha1": "1c528fb258a6e63e8fceb4482d8db0f3af10a634",
                            "size": 57908,
                            "url": "https://build.lwjgl.org/release/3.3.1/bin/lwjgl-opengl/lwjgl-opengl-natives-linux-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl-opengl:3.3.1",
                "natives": {"linux": "natives-linux"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "b119297cf8ed01f247abe8685857f8e7fcf5980f",
                        "size": 112380,
                        "url": "https://build.lwjgl.org/release/3.3.1/bin/lwjgl-stb/lwjgl-stb.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl-stb:3.3.1",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "b119297cf8ed01f247abe8685857f8e7fcf5980f",
                        "size": 112380,
                        "url": "https://build.lwjgl.org/release/3.3.1/bin/lwjgl-stb/lwjgl-stb.jar",
                    },
                    "classifiers": {
                        "natives-linux": {
                            "sha1": "8e8348a1813aad7f30aaf75ea197151ebb7beba9",
                            "size": 205491,
                            "url": "https://build.lwjgl.org/release/3.3.1/bin/lwjgl-stb/lwjgl-stb-natives-linux-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl-stb:3.3.1",
                "natives": {"linux": "natives-linux"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "0ff1914111ef2e3e0110ef2dabc8d8cdaad82347",
                        "size": 6767,
                        "url": "https://build.lwjgl.org/release/3.3.1/bin/lwjgl-tinyfd/lwjgl-tinyfd.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl-tinyfd:3.3.1",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "0ff1914111ef2e3e0110ef2dabc8d8cdaad82347",
                        "size": 6767,
                        "url": "https://build.lwjgl.org/release/3.3.1/bin/lwjgl-tinyfd/lwjgl-tinyfd.jar",
                    },
                    "classifiers": {
                        "natives-linux": {
                            "sha1": "964f628b7a82fd909def086c0dd9a4b84bb259ae",
                            "size": 42654,
                            "url": "https://build.lwjgl.org/release/3.3.1/bin/lwjgl-tinyfd/lwjgl-tinyfd-natives-linux-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl-tinyfd:3.3.1",
                "natives": {"linux": "natives-linux"},
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "ae58664f88e18a9bb2c77b063833ca7aaec484cb",
                        "size": 724243,
                        "url": "https://build.lwjgl.org/release/3.3.1/bin/lwjgl/lwjgl.jar",
                    }
                },
                "name": "org.lwjgl:lwjgl:3.3.1",
            },
            {
                "downloads": {
                    "artifact": {
                        "sha1": "ae58664f88e18a9bb2c77b063833ca7aaec484cb",
                        "size": 724243,
                        "url": "https://build.lwjgl.org/release/3.3.1/bin/lwjgl/lwjgl.jar",
                    },
                    "classifiers": {
                        "natives-linux": {
                            "sha1": "b597401014acb7196c76d97e15a6288f54f1f692",
                            "size": 86308,
                            "url": "https://build.lwjgl.org/release/3.3.1/bin/lwjgl/lwjgl-natives-linux-arm64.jar",
                        }
                    },
                },
                "name": "org.lwjgl:lwjgl:3.3.1",
                "natives": {"linux": "natives-linux"},
            },
        ]
    }
