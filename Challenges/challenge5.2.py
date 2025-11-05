def ipv4_to_value(ipv4_addr):
    ip_nums = ipv4_addr.split('.')
    ip_nums = [int(num) for num in ip_nums]
    hex_str = (ip_nums[0] << 24) | (ip_nums[1] << 16) | (ip_nums[2] << 8) | ip_nums[3]
    return int(hex_str)

def value_to_ipv4(addr):
    ip = []
    ip.append(str((addr >> 24) & 0xff))
    ip.append(str((addr >> 16) & 0xff))
    ip.append(str((addr >> 8)  & 0xff))
    ip.append(str((addr >> 0)  & 0xff))
    return (".").join(ip)

def get_subnet_mask_value(slash):
    index = slash.find('/') + 1
    slash_num = int(slash[index:])
    mask = str((1 << slash_num)-1)
    mask = int(mask) << (32 - slash_num)
    return mask

def get_network(ip_value, netmask):
    return ip_value & netmask

def get_network_ip(ip, slash):
    return value_to_ipv4(get_network(ipv4_to_value(ip), get_subnet_mask_value(slash)))

print(get_network_ip("192.168.107.101", "/19"))
