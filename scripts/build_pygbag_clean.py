import os
import shutil
import stat
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STAGING_DIR = ROOT / "build" / "pygbag_app"

FILES_TO_COPY = [
    "main.py",
    "requirements.txt",
    "abertura.png",
]

DIRS_TO_COPY = [
    "assets",
    "src",
]


def ignore_generated(_folder: str, names: list[str]) -> set[str]:
    return {
        name
        for name in names
        if name == "__pycache__" or name.endswith((".pyc", ".pyo"))
    }


def remove_tree(path: Path):
    def onexc(func, item, _excinfo):
        os.chmod(item, stat.S_IWRITE)
        func(item)

    for attempt in range(3):
        try:
            shutil.rmtree(path, onexc=onexc)
            return
        except PermissionError:
            if attempt == 2:
                raise
            time.sleep(0.4)


def main() -> int:
    if STAGING_DIR.exists():
        remove_tree(STAGING_DIR)
    STAGING_DIR.mkdir(parents=True)

    for filename in FILES_TO_COPY:
        shutil.copy2(ROOT / filename, STAGING_DIR / filename)

    for dirname in DIRS_TO_COPY:
        shutil.copytree(ROOT / dirname, STAGING_DIR / dirname, ignore=ignore_generated)

    command = [sys.executable, "-m", "pygbag", "--build", str(STAGING_DIR)]
    result = subprocess.run(command, cwd=ROOT)
    if result.returncode == 0:
        print("Build Pygbag limpo gerado em:")
        print(STAGING_DIR / "build" / "web")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
