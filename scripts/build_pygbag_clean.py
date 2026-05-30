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

READY_TOUCH_PATCH = """\
        # Mobile Safari/iOS can keep the loader canvas from giving Pygbag the
        # first media engagement tap. Let the page receive that tap, then restore
        # canvas interaction before the game starts.
        platform.window.canvas.style.pointerEvents = "none"
        while not platform.window.MM.UME:
            await asyncio.sleep(.1)
        platform.window.canvas.style.pointerEvents = "auto"
"""

READY_TOUCH_TARGET = """\
        while not platform.window.MM.UME:
            await asyncio.sleep(.1)
"""

READY_PROMPT_MARKER = "Ready to start !"


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


def patch_mobile_ready_prompt(index_path: Path) -> bool:
    try:
        html = index_path.read_text(encoding="utf-8")
    except OSError:
        return False

    if "platform.window.canvas.style.pointerEvents = \"none\"" in html:
        print("Patch mobile do Ready to start ja estava aplicado.")
        return True

    if READY_PROMPT_MARKER not in html:
        print("Bloqueio Ready to start desativado no build Pygbag.")
        return True

    if READY_TOUCH_TARGET not in html:
        print("Nao foi possivel encontrar o bloco Ready to start para patch mobile.")
        return False

    html = html.replace(READY_TOUCH_TARGET, READY_TOUCH_PATCH, 1)

    try:
        index_path.write_text(html, encoding="utf-8")
    except OSError:
        return False

    print("Patch mobile aplicado ao Ready to start do Pygbag.")
    return True


def main() -> int:
    if STAGING_DIR.exists():
        remove_tree(STAGING_DIR)
    STAGING_DIR.mkdir(parents=True)

    for filename in FILES_TO_COPY:
        shutil.copy2(ROOT / filename, STAGING_DIR / filename)

    for dirname in DIRS_TO_COPY:
        shutil.copytree(ROOT / dirname, STAGING_DIR / dirname, ignore=ignore_generated)

    command = [
        sys.executable,
        "-m",
        "pygbag",
        "--ume_block=0",
        "--build",
        str(STAGING_DIR),
    ]
    result = subprocess.run(command, cwd=ROOT)
    if result.returncode == 0:
        index_path = STAGING_DIR / "build" / "web" / "index.html"
        if not patch_mobile_ready_prompt(index_path):
            return 1
        print("Build Pygbag limpo gerado em:")
        print(STAGING_DIR / "build" / "web")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
