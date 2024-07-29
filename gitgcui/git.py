import os
import platform
import subprocess
from pathlib import Path

import structlog

log = structlog.stdlib.get_logger()


def exec(cmd, cwd=None):
    return subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd, text=True
    )


def app_open(url):
    p = platform.system()
    if p == "Linux":
        cmd = ["xdg-open", url]
    else:
        return f"Not supported platform {p}"

    r = exec(cmd)
    return r.stderr


def gc(path: str) -> str:
    p = Path(path)
    dir = p if p.is_dir() else p.parent
    r = exec(["git", "gc"], dir)
    return r.stderr


def root(path: str) -> str:
    """Get root directory of a Git repo."""
    p = Path(path)
    dir = p if p.is_dir() else p.parent
    log.debug("git.root", dir=dir)
    r = exec(["git", "rev-parse", "--show-toplevel"], dir)
    return r.stdout.strip() if r.stdout else ""


def count_files(rootdir: str) -> int:
    file_count = sum(len(files) for _, _, files in os.walk(rootdir))
    return file_count


def list_dirs(root: str) -> list[Path]:
    cwd = Path(root)
    return [entry for entry in cwd.iterdir() if entry.is_dir()]
