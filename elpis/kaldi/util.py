import os
import shlex
import subprocess
from .. import paths

def log(content: str):
    log_path = os.path.join(paths.ELPIS_ROOT_DIR, 'log.txt')
    with open(log_path, 'a') as fout:
        fout.write(content)

def run_to_log(cmd: str, **kwargs) -> str:
    """Captures stdout/stderr and writes it to a log file, then returns the
    CompleteProcess result object"""
    args = shlex.split(cmd)
    if 'cwd' not in kwargs:
        kwargs['cwd'] = '/kaldi-helpers'
    process = subprocess.run(
        args,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        **kwargs
    )
    log(process.stdout.decode("utf-8"))
    return process

def task(name):
    return run_to_log(f'task {name}')