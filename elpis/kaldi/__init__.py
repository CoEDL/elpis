import os
import shlex
import shutil
import subprocess
from .. import paths

class KaldiError(Exception):
    def __init__(self, message, human_message=None):
        super().__init__(message)
        if human_message == None:
            self.human_message = message
        else:
            self.human_message = human_message

class StepDependencyError(KaldiError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

def step(deps=[]):
    """
    This decorator acts as a management object ensuring that the high-level
    functions (representing a steps in the transcription process) happen in
    the right order.

    `step` has a few properties to keep track of which functions have run:
     * `functions` is a list of registered funtions.
     * `reset()` resets the step progression

    :param deps: List of dependent steps (list of dependent functions).
    """
    def decorator(f):
        # Initalisation
        try:
            _ = step.functions # fails if not initialized
        except AttributeError as e:
            # begin init code
            step.functions = []
            def reset():
                for func in step.functions:
                    func.has_ran = False
            step.reset = reset
            # end init code

        # general code body below
        # TODO error if function already registered?
        def wrapper(*agrs, **kwargs):
            # TODO: This is not thread safe. Relies on the server running in development mode (one thread at a time)
            result = f(*agrs, **kwargs)
            wrapper.has_ran = True
            return result
        wrapper.deps = deps
        wrapper.has_ran = False
        wrapper.__doc__ = f.__doc__
        wrapper.f = f
        step.functions.append(wrapper)
        return wrapper
    return decorator
    # TODO revert function property?

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
        # check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        **kwargs
    )
    log(process.stdout.decode("utf-8"))
    return process

def task(name):
    return run_to_log(f'task {name}')

