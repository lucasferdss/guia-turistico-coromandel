# start.py
import os, sys, subprocess, platform, threading, time, webbrowser

ROOT = os.path.dirname(os.path.abspath(__file__))
VENV = os.path.join(ROOT, ".venv")
IS_WIN = platform.system() == "Windows"

def venv_py():
    return os.path.join(VENV, "Scripts" if IS_WIN else "bin", "python.exe" if IS_WIN else "python")

def run(cmd, **kw):
    print(">", " ".join(cmd))
    subprocess.check_call(cmd, **kw)

def open_browser_later(url, delay=1.5):
    def _open():
        time.sleep(delay)   # dá um tempinho pro server subir
        try:
            webbrowser.open(url)
        except Exception:
            pass
    t = threading.Thread(target=_open, daemon=True)
    t.start()

def main():
    # cria venv se não existir
    if not os.path.exists(VENV):
        print("🧪 Criando venv…")
        run([sys.executable, "-m", "venv", VENV])

    py = venv_py()

    # pip up
    print("⬆️  Atualizando pip…")
    run([py, "-m", "pip", "install", "--upgrade", "pip"])

    # deps
    req = os.path.join(ROOT, "requirements.txt")
    if os.path.exists(req):
        print("📦 Instalando dependências…")
        run([py, "-m", "pip", "install", "-r", req])
    else:
        print("⚠️  requirements.txt não encontrado (pulando instalação).")

    # envs
    env = os.environ.copy()
    port = env.get("PORT", "5000")
    env.setdefault("PORT", port)
    # env.setdefault("DISABLE_EMAIL", "1")  # descomente se quiser desativar envio local

    # abre o navegador automaticamente
    url = f"http://127.0.0.1:{port}/"
    open_browser_later(url, delay=1.5)

    # roda o server
    print("🚀 Iniciando server…")
    run([py, os.path.join(ROOT, "server.py")], env=env)

if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)
