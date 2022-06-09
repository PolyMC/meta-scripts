# PolyMC Meta

Scripts to generate jsons and jars that PolyMC will access.

## Configuration

1. Clone this repo
2. If you want to override any properties from `config.sh`, create a file `config/config_local.sh` and write them there
3. If deploying, put your SSH key in `config/deploy.key` (should have push access to `meta-upstream` and `meta-polymc`)
4. Pull the meta repos: `bash clone.sh`

## Building

## Release
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

## Debug (DO NOT PUSH TO REMOTE WITH THIS)

You can run the scripts locally if you want to quickly test or debug. To do so, you need to install [poetry](https://github.com/python-poetry/poetry):

```bash
pip install poetry
```

Then, simply run:

```
poetry install
poetry run ./update.sh
```
Again, **DO NOT PUSH TO REMOTE WITH THIS!**
