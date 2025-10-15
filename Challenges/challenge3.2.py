def packet_complete(data):
    byte_length = int.from_bytes(data[:2], "big")
    if len(data) >= byte_length+2:
        return True
    return False

def packet_extract(data):
    byte_length = int.from_bytes(data[:2], "big")
    return data[:byte_length+2], data[byte_length+2:]

test_data = (
    (b'\x00\x05hello', (True, (b'\x00\x05hello', b''))),
    (b'\x00\x05hello\x00\x03', (True, (b'\x00\x05hello', b'\x00\x03'))),
    (b'\x00\x05hello\x00\x03and\x00\x09bb', (True, (b'\x00\x05hello', b'\x00\x03and\x00\x09bb'))),
    (b'\x00\x00', (True, (b'\x00\x00',b''))),
    (b'\x00\x05hell', (False, None)),
    (b'\x00\x05', (False, None)),
    (b'\x00', (False, None)),
    (b'', (False, None)),
)

for data, (expected_complete, expected_result) in test_data:
    print(f"{'='*40}\nData: {data}\n{'-'*40}")

    complete = packet_complete(data)
    print(f"Expected: {expected_complete}")
    print(f"     Got: {complete}")
    assert(complete == expected_complete)

    if complete:
        result = packet_extract(data)
        print(f"Expected: {expected_result}")
        print(f"     Got: {result}")
        assert(result == expected_result)