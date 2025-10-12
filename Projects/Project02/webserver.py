import socket
import os
import mimetypes

def collectData():
    data = ""
    while '\r\n\r\n' not in data:
        data += new_socket.recv(4096).decode("ISO-8859-1")
    return data

def getRequest(data):
    data = data.split('\r\n')
    return data[0]

def getContent(filename):
    try:
        with open(filename, "rb") as fp:
            data = fp.read()   # Read entire file
            return data.decode("ISO-8859-1")
    except:
        return False

def getMIME(url):
    return mimetypes.guess_type(url, strict=True)[0]

port = 33490

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', port))
s.listen()

while True:
    new_conn = s.accept()
    new_socket = new_conn[0]

    # Split up the data to get the file name
    request = getRequest(collectData())
    fullPath = request.split()[1]
    fileName = os.path.split(fullPath)[-1]

    #DEBUGGING
    '''
    print(request)
    print(fullPath)
    print(fileName)
    '''

    # Get content and MIME type for response
    content = getContent(fileName)
    mimeType = getMIME(os.path.splitext(fileName)[1])

    # 404 Error if content isn't found
    if content == False:
        string = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: close\r\nConnection: close\r\n\r\n404 not found"
        response = string.encode("ISO-8859-1")
        new_socket.sendall(response)
        new_socket.close()
        continue

    # Create & Send Response
    string = f"HTTP/1.1 200 OK\r\nContent-Type: {mimeType}\r\nContent-Length: {len(content)}\r\nConnection: close\r\n\r\n{content}"
    response = string.encode("ISO-8859-1")

    new_socket.sendall(response)
    new_socket.close()
