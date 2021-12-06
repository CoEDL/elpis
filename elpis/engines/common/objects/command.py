import subprocess


def run(cmdline: str, cwd: str = None) -> subprocess.CompletedProcess:
    """
    Run a command in the bash shell.
    
    :cmdline: command string to run in bash.
    :cwd: optionallly, set the current working dir for the command.
    :return: the subprocess created from the string.
    """
    args = ['bash', '-c', cmdline]
    process = subprocess.run(
        args,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        cwd=cwd
    )
    return process
