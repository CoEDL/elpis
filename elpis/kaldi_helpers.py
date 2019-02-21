import subprocess


def run_settings_task_demo():
    # l = subprocess.run(["ls", "-la"])
    # l = subprocess.run(["cd", ".."])
    # l = subprocess.run(["cd", "kaldi-helpers"])
    # l = subprocess.run(["task", "tmp-makedir"])
    # subprocess.run(["touch", "touch-file3"])
    proc = subprocess.Popen(["ls"], stdout=subprocess.PIPE)
    std_out, std_err = proc.communicate()
    print(std_out, std_err)
    print('hi')    


if __name__ == "__main__":
    run_settings_task_demo()
