import subprocess


def run(cmdline: str) -> subprocess.CompletedProcess:
    """
    Run a command in the bash shell.
    
    :cmdline: command string to run in bash.
    :return: the subprocess created from the string.
    """
    args = ['bash', '-c', cmdline]
    process = subprocess.run(
        args,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    return process
