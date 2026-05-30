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

LOADING_STYLE = """\

        html, body {
            background: #76c9d4;
            overflow: hidden;
            overscroll-behavior: none;
            touch-action: manipulation;
            -webkit-user-select: none;
            user-select: none;
        }

        #caminhos-loading {
            position: fixed;
            inset: 0;
            z-index: 20;
            display: flex;
            align-items: center;
            justify-content: center;
            box-sizing: border-box;
            padding: 24px;
            background: #76c9d4;
            color: #202428;
            font-family: Arial, sans-serif;
            text-align: center;
            pointer-events: none;
            opacity: 1;
            transition: opacity 280ms ease;
        }

        #caminhos-loading.is-hidden {
            opacity: 0;
        }

        #caminhos-loading .panel {
            width: min(84vw, 430px);
            box-sizing: border-box;
            padding: 22px 20px 20px;
            background: rgba(248, 238, 190, 0.94);
            border: 2px solid #202428;
            border-radius: 8px;
            box-shadow: 0 12px 28px rgba(32, 36, 40, 0.22);
        }

        #caminhos-loading .title {
            margin: 0 0 8px;
            font-size: 26px;
            font-weight: 700;
        }

        #caminhos-loading .message {
            margin: 0;
            font-size: 16px;
            line-height: 1.35;
        }

        #caminhos-loading .hint {
            margin: 8px 0 0;
            font-size: 13px;
            line-height: 1.35;
        }

        #caminhos-loading .bar {
            position: relative;
            height: 10px;
            margin: 18px auto 0;
            overflow: hidden;
            border: 2px solid #202428;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.55);
        }

        #caminhos-loading .bar::after {
            content: "";
            position: absolute;
            top: 0;
            bottom: 0;
            left: -38%;
            width: 38%;
            background: #2fb36f;
            animation: caminhos-loading-bar 1.25s ease-in-out infinite;
        }

        @keyframes caminhos-loading-bar {
            0% {
                left: -38%;
            }
            100% {
                left: 100%;
            }
        }
"""

LOADING_MARKUP = """\
    <div id="caminhos-loading" aria-live="polite">
        <div class="panel">
            <p class="title">Caminhos do Brasil</p>
            <p class="message" id="caminhos-loading-message">Carregando arquivos do jogo...</p>
            <div class="bar" aria-hidden="true"></div>
            <p class="hint">Primeira abertura pode levar alguns segundos. Se demorar, toque para continuar.</p>
        </div>
    </div>

    <script>
    (function () {
        var messages = [
            "Carregando arquivos do jogo...",
            "Preparando Mig e a linha do tempo...",
            "Quase pronto. Use o celular deitado."
        ];
        var index = 0;
        var hidden = false;
        var messageTimer = window.setInterval(function () {
            var label = document.getElementById("caminhos-loading-message");
            if (!label) {
                return;
            }
            index = (index + 1) % messages.length;
            label.textContent = messages[index];
        }, 2400);
        function hideLoading() {
            if (hidden) {
                return;
            }
            var loading = document.getElementById("caminhos-loading");
            if (!loading) {
                return;
            }
            hidden = true;
            window.clearInterval(messageTimer);
            loading.classList.add("is-hidden");
            window.setTimeout(function () {
                loading.style.display = "none";
            }, 320);
        }
        window.caminhosHideLoading = hideLoading;
        window.setTimeout(hideLoading, 8500);
        window.addEventListener("pointerdown", hideLoading, { passive: true });
        window.addEventListener("touchstart", hideLoading, { passive: true });
        window.addEventListener("click", hideLoading);
    })();
    </script>
"""


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


def patch_loading_experience(index_path: Path) -> bool:
    try:
        html = index_path.read_text(encoding="utf-8")
    except OSError:
        return False

    if "id=\"caminhos-loading\"" in html:
        print("Tela de carregamento mobile ja estava aplicada.")
        return True

    if "</style>" not in html or "<body>" not in html:
        print("Nao foi possivel encontrar pontos para inserir a tela de carregamento.")
        return False

    html = html.replace("</style>", f"{LOADING_STYLE}\n    </style>", 1)
    html = html.replace("<body>", f"<body>\n{LOADING_MARKUP}", 1)

    try:
        index_path.write_text(html, encoding="utf-8")
    except OSError:
        return False

    print("Tela de carregamento mobile aplicada ao index.html.")
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
        if not patch_loading_experience(index_path):
            return 1
        print("Build Pygbag limpo gerado em:")
        print(STAGING_DIR / "build" / "web")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
