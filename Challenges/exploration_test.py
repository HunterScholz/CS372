def ip_to_dec(ip):
    hex_str = b''
    ip_nums = ip.split('.')
    for num in ip_nums:
        hex_str += int(num).to_bytes()
    return int.from_bytes(hex_str)

def dec_to_ip(dec):
    ip = []
    ip.append(str((dec >> 24) & 0xff))
    ip.append(str((dec >> 16) & 0xff))
    ip.append(str((dec >> 8)  & 0xff))
    ip.append(str((dec >> 0)  & 0xff))
    return (".").join(ip)


    
print(hex(ip_to_dec("192.0.2.37")))
print(dec_to_ip(3405804026))