def pack_ip(ip):
    byte_string = b''
    ip_nums = ip.split('.')
    for num in ip_nums:
        byte_string += int(num).to_bytes(1, 'big')
    return byte_string

test_data = (
    ("0.0.0.0", b'\x00\x00\x00\x00'),
    ("127.0.0.1", b'\x7f\x00\x00\x01'),
    ("255.0.255.0", b'\xff\x00\xff\x00'),
    ("127.1.127.1", b'\x7f\x01\x7f\x01'),
    ("16.16.16.16", b'\x10\x10\x10\x10'),
    ("1.1.1.1", b'\x01\x01\x01\x01'),
    ("1.2.3.4", b'\x01\x02\x03\x04'),
)

for ip, packed_ip in test_data:
    output = f"testing: {ip} -> {packed_ip}"
    print(f"{output:<45}", end="")
    print('OK' if pack_ip(ip) == packed_ip else 'FAIL')
