import asyncio
import os
import shutil
import subprocess
import time
import traceback
from concurrent.futures import ProcessPoolExecutor
from datetime import date
from functools import partial
from pathlib import Path

from . import fabric, forge, index, liteloader, mojang, neoforge
from .common import PMC, UPSTREAM, client, log

BRANCH = os.environ.get("BRANCH", "develop")
PUSH = os.environ.get("DEPLOY_TO_GIT") == "true"
DEPLOY_FOLDER = os.environ.get("DEPLOY_FOLDER")
INTERVAL = int(os.environ.get("INTERVAL", "0"))
REPOS = {
    UPSTREAM: os.environ.get("UPSTREAM_REPO", "git@github.com:PolyMC/meta-upstream.git"),
    PMC: os.environ.get("PMC_REPO", "git@github.com:PolyMC/meta-polymc.git"),
}


def git(repo: Path, *args: str):
    subprocess.run(["git", "-C", str(repo), *args], check=True)


def prepare():
    for repo, url in REPOS.items():
        if not repo.exists():
            subprocess.run(["git", "clone", url, str(repo)], check=True)
        git(repo, "reset", "--hard", "HEAD")
        git(repo, "checkout", BRANCH)


def publish(repo: Path):
    if not PUSH:
        return
    git(repo, "add", "-A", "--", "*.json")
    if subprocess.run(["git", "-C", str(repo), "diff", "--cached", "--quiet"]).returncode:
        git(repo, "commit", "-m", f"Update {date.today().isoformat()}")
        git(repo, "push")


async def pipeline(pool: ProcessPoolExecutor):
    loop = asyncio.get_running_loop()
    cpu = partial(loop.run_in_executor, pool)

    async def then(deps, fn, *args):
        await asyncio.gather(*deps)
        return await fn(*args)

    async with client() as http, asyncio.TaskGroup() as tg:
        up = {name: tg.create_task(coro) for name, coro in {
            "mojang": mojang.update(http),
            "forge": forge.update(http),
            "neoforge": neoforge.update(http),
            "fabric": fabric.update(http, "fabric"),
            "quilt": fabric.update(http, "quilt"),
            "liteloader": liteloader.update(http),
        }.items()}
        minecraft = tg.create_task(then([up["mojang"]], cpu, mojang.generate))
        tg.create_task(then([up["forge"], minecraft], cpu, forge.generate))
        tg.create_task(then([up["neoforge"], minecraft], cpu, neoforge.generate))
        tg.create_task(then([up["fabric"]], cpu, fabric.generate, "fabric"))
        tg.create_task(then([up["quilt"]], cpu, fabric.generate, "quilt"))
        tg.create_task(then([up["liteloader"]], cpu, liteloader.generate))
        tg.create_task(then(up.values(), asyncio.to_thread, publish, UPSTREAM))

    await cpu(index.generate)
    await asyncio.to_thread(publish, PMC)
    if DEPLOY_FOLDER:
        await asyncio.to_thread(shutil.copytree, PMC, DEPLOY_FOLDER, ignore=shutil.ignore_patterns(".git"),
                                dirs_exist_ok=True)


def run():
    prepare()
    try:
        with ProcessPoolExecutor() as pool:
            asyncio.run(pipeline(pool))
    except BaseException:
        for repo in REPOS:
            git(repo, "reset", "--hard", "HEAD")
        raise


if __name__ == "__main__":
    if not INTERVAL:
        run()
    while INTERVAL:
        started = time.monotonic()
        try:
            run()
        except Exception:
            traceback.print_exc()
        log(f"Run finished in {time.monotonic() - started:.0f}s")
        time.sleep(max(0.0, INTERVAL - (time.monotonic() - started)))
