#.\venv\Scripts\activate
#pyinstaller --onefile --icon=vscode+.ico start_vscode_with_docker.py

import subprocess, time, os, shutil, ctypes, sys

def run_cmd(cmd, timeout=8):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, shell=False)
        return p.returncode, p.stdout.strip()
    except Exception as e:
        return 1, str(e)

def is_proc(name):
    rc, out = run_cmd(['tasklist'])
    return rc == 0 and name.lower() in out.lower()

def is_rancher_running():
    return is_proc('rancher desktop')

def kubernetes_ready():
    if not shutil.which('kubectl'): return False
    rc, out = run_cmd(['kubectl','get','--raw','/readyz?verbose'], timeout=6)
    if rc == 0 and 'ok' in out.lower(): return True
    rc, _ = run_cmd(['kubectl','cluster-info'], timeout=6)
    if rc != 0: return False
    rc, nodes = run_cmd(['kubectl','get','nodes','--no-headers'], timeout=6)
    if rc != 0 or not nodes.strip(): return False
    for l in nodes.splitlines():
        if 'ready' not in l.lower(): return False
    return True

def container_runtime_available():
    if shutil.which('docker') and run_cmd(['docker','info'], timeout=6)[0] == 0: return True
    if shutil.which('nerdctl') and run_cmd(['nerdctl','info'], timeout=6)[0] == 0: return True
    return False

rancher_path = r"C:\Program Files\Rancher Desktop\Rancher Desktop.exe"
code_exe = r"C:\Users\sasch\AppData\Local\Programs\Microsoft VS Code\Code.exe"

if not is_rancher_running():
    if shutil.which('rdctl'):
        subprocess.Popen(['rdctl','start'])
    elif os.path.exists(rancher_path):
        os.startfile(rancher_path)
    else:
        print("Rancher Desktop nicht gefunden"); raise SystemExit(1)

start = time.time(); timeout = 180
while time.time()-start < timeout:
    if kubernetes_ready() and container_runtime_available():
        print("K8s + container runtime ready"); break
    print("warte auf k8s/container..."); time.sleep(2)
else:
    print("Timeout beim Starten"); raise SystemExit(1)

if os.path.exists(code_exe):
    os.startfile(code_exe)
else:
    subprocess.Popen([r"C:\Users\sasch\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd"])

vscode_name = "code.exe"
start = time.time()
while time.time()-start < 30:
    if is_proc(vscode_name):
        print("VSCode läuft")
        sys.exit(0); break
    time.sleep(1)
else:
    print("VSCode startet nicht schnell genug")

hwnd = ctypes.windll.kernel32.GetConsoleWindow()
if hwnd:
    ctypes.windll.user32.ShowWindow(hwnd, 0)

stopfile = os.path.join(os.path.dirname(__file__), "stop_monitor.txt")
try:
    while True:
        if os.path.exists(stopfile):
            print("stopfile gefunden, beende Monitor"); break
        time.sleep(60)
except KeyboardInterrupt:
    if hwnd:
        ctypes.windll.user32.ShowWindow(hwnd, 5)
