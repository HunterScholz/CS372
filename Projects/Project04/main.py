def IP_to_bytes(ip):
    byte_string = b''
    bytes = ip.split('.')
    for byte in bytes:
        byte_string += int(byte).to_bytes(1)
    return byte_string

def get_pseudoheader(source_ip, dest_ip):
    header = b''
    header += IP_to_bytes(source_ip) + IP_to_bytes (dest_ip)
    header += (0).to_bytes(1) + (6).to_bytes(1)
    return header

def calc_checksum(pseudoheader, tcp_cksum):
    data = pseudoheader + tcp_cksum
    offset = 0
    total = 0
    while offset < len(data):
        word = int.from_bytes(data[offset:offset + 2], "big")
        offset += 2   # Go to the next 2-byte value

        total += word
        total = (total & 0xffff) + (total >> 16)
    return (~total) & 0xffff

def get_checksums(data, addrs):
    # TCP Data
    with open(data, "rb") as fp:
        tcp_data = fp.read()
        tcp_length = len(tcp_data)

    # Address Data
    with open(addrs) as addrs:
        addrs_data = addrs.read()
        source, dest = addrs_data.split()
        
    # Get Checksums
    pseudoheader = get_pseudoheader(source, dest) + tcp_length.to_bytes(2)
    tcp_cksum = int.from_bytes(tcp_data[16:18])

    tcp_zero_cksum = tcp_data[:16] + b'\x00\x00' + tcp_data[18:]
    if len(tcp_zero_cksum) % 2 == 1:
        tcp_zero_cksum += b'\x00'

    addrs_cksum = calc_checksum(pseudoheader, tcp_zero_cksum)

    return tcp_cksum, addrs_cksum

def compare_checksums(check1, check2):
    if check1 == check2:
        print("PASS")
        return
    print("FAIL")

# -------------------------
# Compare all the Checksums
for i in range(10):
    data = "tcp_data/tcp_data_"+ str(i) + ".dat"
    addrs = "tcp_data/tcp_addrs_"+ str(i) + ".txt"
    tcp_cksum, addrs_cksum = get_checksums(data, addrs)
    compare_checksums(tcp_cksum, addrs_cksum)
