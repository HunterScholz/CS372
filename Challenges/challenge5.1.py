ip_1 = "192.168.1.2"
ip_2 = "10.20.30.40"
ip_3 = "127.0.0.1"

dec_1 = 3325256824
dec_2 = 3405803976
dec_3 = 3221225987

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
    
print(ip_to_dec(ip_1))
print(ip_to_dec(ip_2))
print(ip_to_dec(ip_3))
print(dec_to_ip(dec_1))
print(dec_to_ip(dec_2))
print(dec_to_ip(dec_3))

# Prints Out:
# 3232235778
# 169090600
# 2130706433
# 198.51.100.120
# 203.0.113.200
# 192.0.2.3