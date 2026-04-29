# Patch Generators

Generates match overrides for windows-arm64 and osx-arm64, and download overrides for LWJGL 3.3.1+ for linux-arm64, linux-arm32, and linux-riscv64.

These are needed to reduce the tedium of manually updating all the LWJGL3 overrides manually, as LWJGL3 requires platform-specific natives that Mojang themselves sometimes don't provide.

## Generating

You will need `curl` and `jq` in PATH. Update the `versions` and `range` strings in `lwjgl3-linux.sh` and `matches-sh`, then run the scripts:

```sh
cd patches
./lwjgl3-linux.sh
./matches.sh
cd ..
patches/generate.sh
```

Now commit, and your LWJGL overrides are updated.

## `static.json`

The `patches/generated/static.json` file is used for patches that are *not* auto-generated.
