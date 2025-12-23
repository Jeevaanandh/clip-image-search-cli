import sys
import hashlib

path= sys.argv[1]

sha256= hashlib.sha256()

with open(path, "rb") as f:
    while True:
        data= f.read(8192)
        if(not data):
            break

        sha256.update(data)

print(sha256.hexdigest())

