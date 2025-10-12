from urllib.parse import urlparse

def getURL(url):
    return urlparse(url).path

print(getURL("https://example.com/"))
print(getURL("https://example.com/foo"))
print(getURL("https://example.com/bar.txt"))
print(getURL("https://example.com/baz/foo/bar.git"))

