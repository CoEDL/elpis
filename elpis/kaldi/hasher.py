from hashlib import md5
from time import time


def new():
    # Meant to give a unique hash. TODO: fix to ensure it does.
    return md5(bytes(str(time()), 'utf-8')).hexdigest()
