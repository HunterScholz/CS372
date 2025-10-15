def encode_data(message, value):
    encodedMsg = message.encode('utf-8')
    encodedVal = value.to_bytes(4, "big")
    length = (len(encodedVal) + len(encodedMsg)).to_bytes(2, "big")
    return length + encodedMsg + encodedVal


def decode_data(data):
    message = data[2:-4].decode('utf-8')
    value = int.from_bytes(data[-4:], "big")
    return message, value

data = encode_data("Hello", 100)
print(data)
print(decode_data(data))