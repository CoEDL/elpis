import shlex
import subprocess

def run(cmdline):
    args = ['bash', '-c', cmdline]
    process = subprocess.run(
        args,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return process
