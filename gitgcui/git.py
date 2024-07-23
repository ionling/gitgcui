import os
import subprocess
from pathlib import Path

import structlog

log = structlog.stdlib.get_logger()


def exec(cmd, cwd=None):
    return subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd, text=True
    )


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
