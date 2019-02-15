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