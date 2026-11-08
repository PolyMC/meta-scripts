# PolyMC Meta

Generates the version metadata that PolyMC downloads.

Each run fetches raw data from Mojang, Forge, NeoForge, Fabric, Quilt and LiteLoader into `upstream/`. It converts that data into PolyMC's format in `polymc/` and writes an `index.json`. If configured, it commits and pushes both repos and copies `polymc/` to a web folder. Every source is fetched and converted concurrently. Forge and NeoForge wait only for the Minecraft output they depend on.

## Deployment

1. Clone this repo and `cp config/meta.env.example config/meta.env`, then edit it.
2. Put an SSH key with push access to meta-upstream and meta-polymc at `config/deploy.key`.
3. `docker compose up -d --build` runs an update every `INTERVAL` seconds (default 3600). The data repos are cloned on the first run.

To run a single update: `docker compose run --rm -e INTERVAL=0 meta`.

Containers run as UID/GID 1337 by default. To match your host user, set `UID` and `GID` when building.

## Configuration

| Variable | Default | Meaning |
|---|---|---|
| `BRANCH` | `develop` | Branch checked out in both data repos |
| `DEPLOY_TO_GIT` | `false` | Commit and push the data repos |
| `DEPLOY_FOLDER` | unset | Copy `polymc/` here after a run |
| `INTERVAL` | `0` | Seconds between runs; `0` runs once |
| `UPSTREAM_DIR`, `PMC_DIR`, `STATIC_DIR` | `upstream`, `polymc`, `static` | Data directories |
| `UPSTREAM_REPO`, `PMC_REPO` | PolyMC GitHub repos | Clone URLs |

## Local development

```sh
pip install -r requirements.txt
python -m meta
```

LWJGL override generators live in `patches/` (see its README).
