import subprocess
import time


def is_docker_running():
    tasks = subprocess.check_output("tasklist", shell=True).decode()
    return "Docker Desktop.exe" in tasks


if not is_docker_running():
    subprocess.Popen(r"C:/Program Files/Docker/Docker/Docker Desktop.exe")
    time.sleep(5)

subprocess.Popen(r"C:/Users/sasch/AppData/Local/Programs/Microsoft VS Code/Code.exe")
