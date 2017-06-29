from os import urandom
import hashlib

def key():

    key = hashlib.md5(urandom(128)).hexdigest()[:7]
    return key

for i in range(100):
    print(key())