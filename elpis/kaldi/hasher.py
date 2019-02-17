from hashlib import md5
from time import time

def new():
    return md5(bytes(str(time()), 'utf-8')).hexdigest()