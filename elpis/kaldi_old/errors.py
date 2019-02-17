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