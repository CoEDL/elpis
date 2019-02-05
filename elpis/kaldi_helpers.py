import subprocess

def run_task_demo():
    l = subprocess.run(["ls", "-la"])
    # l = subprocess.run(["cd", ".."])
    # l = subprocess.run(["cd", "kaldi-helpers"])
    # l = subprocess.run(["task", "tmp-makedir"])
    

