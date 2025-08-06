import subprocess
import time


def run_command(command):
    try:
        output = subprocess.check_output(command, shell=True)
        return output.decode("utf-8").strip()
    except Exception as e:
        print(f"Error: {e}")
        return None


rancher_running = False

if "Rancher Desktop" in run_command("tasklist"):
    rancher_running = True
else:
    subprocess.run(["start", ""], check=False, shell=True)

    time.sleep(5)

    while not rancher_running:
        if "Rancher Desktop" in run_command("tasklist"):
            rancher_running = True
        else:
            print("Waiting for Rancher Desktop to start...")
            time.sleep(2)

if rancher_running:
    subprocess.run(["code"], check=False)
else:
    print("Rancher Desktop couldn't start.")
