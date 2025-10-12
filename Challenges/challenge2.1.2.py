import os
import mimetypes

def getExt(url):
    return os.path.splitext(url)[1]

print(getExt("/bar.txt"))

def getMIME(url):
    return mimetypes.guess_type(url, strict=True)[0]

print(getMIME("/bar.txt"))
