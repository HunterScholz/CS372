# Example usage:
#
# python chat_server.py 3490

import sys
import socket
import select
import json

def run_server(port):
    listen_socket = socket.socket()
    listen_socket.bind(('127.0.0.1', port))
    listen_socket.listen()
    read_set = {listen_socket}
    nicks = {}

    while read_set:
        ready_to_read, _, _ = select.select(read_set, {}, {})

        for s in ready_to_read:
            if s is listen_socket: # Accept new clients
                new_s, _ = s.accept()
                read_set.add(new_s)

            else: # Check for new messages
                try:
                    data = s.recv(4096)
                    payload = json.loads(data.decode())
                except:
                    read_set.remove(s)
                    send_to_clients(read_set, listen_socket, {"type": "leave","nick": nicks[s]})
                    ready_to_read.remove(s)
                    del nicks[s]
                    continue

                match payload["type"]:
                    case "hello":
                        nicks[s] = payload["nick"]
                        send_to_clients(read_set, listen_socket, {"type": "join","nick": nicks[s]})
                    case "chat":
                        send_to_clients(read_set, listen_socket, {"type": "chat", "nick": nicks[s], "message": payload["message"]})
    pass

def send_to_clients(client_set, ls, payload):
    for s in client_set:
        if s is not ls:
            json_string = json.dumps(payload)
            s.sendall(json_string.encode())
    pass

# def client_quits(s):
#     print(f"***someone has left the chat")
#     read_set.remove(s)

#--------------------------------#
# Do not modify below this line! #
#--------------------------------#

def usage():
    print("usage: select_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
