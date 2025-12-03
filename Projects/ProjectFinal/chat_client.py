# Example usage:
#
# python chat_client.py chris localhost 3490

import sys
import socket
import json
import threading
from chatui import init_windows, read_command, print_message, end_windows


def usage():
    print("usage: select_client.py nickname host port", file=sys.stderr)

def main(argv):
    try:
        nickname = argv[1]
        host = argv[2]
        port = int(argv[3])
    except:
        usage()
        return 1

    # Initiate UI
    init_windows()

    # Make the client socket and connect
    s = socket.socket()
    s.connect((host, port))

    # Create recieving thread
    stop_event = threading.Event()
    t = threading.Thread(target=recieve_data, args=(s, stop_event))
    t.start()

    # Join Message
    connection = json.dumps({
        "type": "hello",
        "nick": nickname
    })
    json_connect_bytes = connection.encode()
    s.send(json_connect_bytes)

    # Loop forever sending data
    while True:
        message = read_command(f"{nickname}> ")

        # Client leaves chat
        if message == "/q":
            stop_event.set()
            s.shutdown(socket.SHUT_RDWR)  # tells recv() to exit immediately
            s.close()
            t.join()
            end_windows()
            break

        # Send Message
        payload = json.dumps({
            "type": "chat",
            "message": message
        })
        json_bytes = payload.encode()
        s.send(json_bytes)

# Recieve Thread
def recieve_data(s, stop_event):
    try:
        while not stop_event.is_set():
            data = s.recv(4096)
            if not data:
                break

            payload = json.loads(data.decode())
            match payload["type"]:
                case "join":
                    print_message(f"***{payload['nick']} has joined the chat")
                case "leave":
                    print_message(f"***{payload['nick']} has left the chat")
                case "chat":
                    print_message(f"{payload['nick']}: {payload['message']}")
    except OSError:
        pass

if __name__ == "__main__":
    sys.exit(main(sys.argv))
