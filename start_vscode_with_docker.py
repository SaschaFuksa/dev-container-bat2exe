import subprocess
import time
import os

#.\venv\Scripts\activate
#pyinstaller --onefile --noconsole --icon=vscode+.ico start_vscode_with_docker.py

def run_command(command):
    try:
        output = subprocess.check_output(command, shell=True)
        return output.decode("utf-8").strip()
    except Exception as e:
        print(f"Error: {e}")
        return None

def is_rancher_running():
    return "Rancher Desktop" in run_command("tasklist")

rancher_running = is_rancher_running()

if not rancher_running:
    rancher_path = r"C:\Program Files\Rancher Desktop\Rancher Desktop.exe"
    if not os.path.exists(rancher_path):
        print("❌ Rancher Desktop.exe not found!")
    else:
        subprocess.Popen(['cmd', '/c', 'start', '', rancher_path], shell=False)
        print("🚀 Starting Rancher Desktop...")
        start_time = time.time()

        while not is_rancher_running():
            if time.time() - start_time > 30:
                print("⚠️ Timeout: Rancher Desktop did not start in time.")
                break
            print("⏳ Waiting for Rancher Desktop...")
            time.sleep(2)

if is_rancher_running():
    time.sleep(2)
    vscode_path = r"C:\Users\sasch\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd"
    subprocess.run([vscode_path], shell=True)
else:
    print("⚠️ Rancher Desktop could not be started.")
