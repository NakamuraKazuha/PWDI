import subprocess

processes = []

try:
    processes.append(subprocess.Popen(["python", "server.py"]))
    processes.append(subprocess.Popen(["python", "app.py"]))
    processes.append(subprocess.Popen(["python", "web.py"]))

    # Keep the processes running
    for p in processes:
        p.wait()
except KeyboardInterrupt:
    print("\nStopping all scripts...")
    for p in processes:
        p.terminate()
