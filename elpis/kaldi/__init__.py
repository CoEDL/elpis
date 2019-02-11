class KaldiError(Exception):
    def __init__(self, message, human_message):
        super().__init__(message)
        self.human_message = human_message

class Bridge(object):
    """
    Hide code under the hood of the kaldi interface here.
    """
    @classmethod
    def sync_model(cls):
        pass

def step(deps=[]):
    """
    This decorator acts as a management object ensuring that the high-level
    functions (representing a steps in the transcription process) happen in
    the right order.

    `step` has a few properties to keep track of which functions have run:
     * `functions` is a list of registered funtions.
     * `reset()` resets the step progression
     * `running_step` is the funtion (step) that is running

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
                    func.has_run = False
            step.reset = reset
            step.running_step = None
            # end init code

        # general code body below
        # TODO error if function already registered?
        def wrapper(*agrs, **kwargs):
            # TODO: This is not thread safe. Relies on the server running in development mode (one thread at a time)
            if step.running_step is not None:
                raise KaldiError(f'The {step.running_step} step is still running', 'Another step is still running')
            step.running_step = wrapper
            result = f(*agrs, **kwargs)
            wrapper.has_run = True
            step.running_step = None
            return result
        wrapper.deps = deps
        wrapper.has_run = False
        step.functions.append(wrapper)
        return wrapper
    return decorator
    # TODO revert function property?

