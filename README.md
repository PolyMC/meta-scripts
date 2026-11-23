# PolyMC Meta
Scripts to generate jsons and jars that PolyMC will access.

## Deployment
It is recommended to use Docker to deploy the environment.

- Clone this repo to a server
- Make sure it's writable by the container later: `chown -R 1337:1337 .`
- Configure `config/config_local.sh`
  - The defaults should be fine (apart from committer email and name perhaps)
- Put your SSH key (which has push access to meta-upstream and meta-polymc) at `config/deploy.key`
- Pull meta- repos: `bash clone.sh`
- Customize docker-compose.yaml
- Run `docker-compose up -d --build`
- Observe Cron logs using `docker-compose logs -f` (Runs hourly by default)
- (Optional) Run once to fill caches: `docker-compose run meta update`

For local development you can also use `docker-compose.local.yaml`. By default it uses `UID=1000` and `GID=1000`.
Make sure it's the same as your host instance.

## lwjgl3ify and Cleanroom profiles
`updateMulti3ify.py` and `generateMulti3ify.py` port [multi3ify](https://github.com/AngelicIndustries/multi3ify).
They publish two extra Minecraft versions:

- `1.7.10-lwjgl3ify`: Forge 1.7.10 with [lwjgl3ify](https://github.com/GTNewHorizons/lwjgl3ify). Users add [UniMixins](https://github.com/LegacyModdingMC/UniMixins/releases) to `mods` themselves.
- `1.12.2-cleanroom`: [Cleanroom](https://github.com/CleanroomMC/Cleanroom). Users add Fugue and Scalar Legacy for conventional Forge packs.

Pick either version with **Mod Loader -> None**. The `lwjgl3ify` and `Cleanroom` components offer `latest` plus pinned releases.

The lwjgl3ify profiles need `META_BASE_URL` in `config/config_local.sh`, set to the public URL of the deployed `v1` folder.
They are skipped without it. Their helper jar (`static/multi3ify/`) is served from `maven/` under that URL.
Set `GITHUB_TOKEN` to raise the GitHub API rate limit.
