from os import urandom
import hashlib

def key():

    key = hashlib.md5(urandom(128)).hexdigest()[:12]
    return key

for i in range(100):
    print(key()[:4], "-", key()[4:8], "-", key()[8:], sep="")