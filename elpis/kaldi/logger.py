class Logger(object):
    def __init__(self, path):
        self.hash = 0
    def write(self, line):
        pass

class EmptyLogger(object):
    def __init__(self, path):
        self.hash = None
    def write(self, line):
        pass