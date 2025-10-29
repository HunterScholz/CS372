import sys
import json

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

def ips_same_subnet(ip1, ip2, slash):
    ip1_subnet = get_network(ipv4_to_value(ip1), get_subnet_mask_value(slash))
    ip2_subnet = get_network(ipv4_to_value(ip2), get_subnet_mask_value(slash))
    return ip1_subnet == ip2_subnet

def get_network(ip_value, netmask):
    return ip_value & netmask

def find_router_for_ip(routers, ip):
    for route_ip, netmask in routers.items():
        if ips_same_subnet(route_ip, ip, netmask["netmask"]):
            return route_ip
    return None

# Uncomment this code to have it run instead of the real main.
# Be sure to comment it back out before you submit!

"""
def my_tests():
    print("-------------------------------------")
    print("This is the result of my custom tests")
    print("-------------------------------------")

    print("IP to Value Tests")
    print(ipv4_to_value("255.255.0.0") == 4294901760)
    print(ipv4_to_value("1.2.3.4") == 16909060)

    print("Value to IP Tests")
    print(value_to_ipv4(0xffff0000) == "255.255.0.0")
    print(value_to_ipv4(0b00000001000000100000001100000100) == "1.2.3.4")
    print(value_to_ipv4(16909060) == "1.2.3.4")

    print("Subnet Mask Value")
    print(get_subnet_mask_value("/16") == 4294901760)
    print(get_subnet_mask_value("10.20.30.40/23") == 0xfffffe00)

    print("Compare Subnets")
    print(ips_same_subnet("10.23.121.17", "10.23.121.225", "/23") == True)
    print(ips_same_subnet("10.23.230.22", "10.24.121.225", "/16") == False)

    print("Get Network Test")
    print(get_network(0x01020304, 0xffffff00) == 0x01020300)

    print("Test Routers")
    print(find_router_for_ip({"1.2.3.1": {"netmask": "/24"},"1.2.4.1": {"netmask": "/24"}}, "1.2.3.5") == "1.2.3.1")
    print(find_router_for_ip({"1.2.3.1": {"netmask": "/24"},"1.2.4.1": {"netmask": "/24"}}, "1.2.5.6") == None)
"""
    
## -------------------------------------------
## Do not modify below this line
##
## But do read it so you know what it's doing!
## -------------------------------------------

def usage():
    print("usage: netfuncs.py infile.json", file=sys.stderr)

def read_routers(file_name):
    with open(file_name) as fp:
        json_data = fp.read()
        
    return json.loads(json_data)

def print_routers(routers):
    print("Routers:")

    routers_list = sorted(routers.keys())

    for router_ip in routers_list:

        # Get the netmask
        slash_mask = routers[router_ip]["netmask"]
        netmask_value = get_subnet_mask_value(slash_mask)
        netmask = value_to_ipv4(netmask_value)

        # Get the network number
        router_ip_value = ipv4_to_value(router_ip)
        network_value = get_network(router_ip_value, netmask_value)
        network_ip = value_to_ipv4(network_value)

        print(f" {router_ip:>15s}: netmask {netmask}: " \
            f"network {network_ip}")

def print_same_subnets(src_dest_pairs):
    print("IP Pairs:")

    src_dest_pairs_list = sorted(src_dest_pairs)

    for src_ip, dest_ip in src_dest_pairs_list:
        print(f" {src_ip:>15s} {dest_ip:>15s}: ", end="")

        if ips_same_subnet(src_ip, dest_ip, "/24"):
            print("same subnet")
        else:
            print("different subnets")

def print_ip_routers(routers, src_dest_pairs):
    print("Routers and corresponding IPs:")

    all_ips = sorted(set([i for pair in src_dest_pairs for i in pair]))

    router_host_map = {}

    for ip in all_ips:
        router = str(find_router_for_ip(routers, ip))
        
        if router not in router_host_map:
            router_host_map[router] = []

        router_host_map[router].append(ip)

    for router_ip in sorted(router_host_map.keys()):
        print(f" {router_ip:>15s}: {router_host_map[router_ip]}")

def main(argv):
    if "my_tests" in globals() and callable(my_tests):
        my_tests()
        return 0

    try:
        router_file_name = argv[1]
    except:
        usage()
        return 1

    json_data = read_routers(router_file_name)

    routers = json_data["routers"]
    src_dest_pairs = json_data["src-dest"]

    print_routers(routers)
    print()
    print_same_subnets(src_dest_pairs)
    print()
    print_ip_routers(routers, src_dest_pairs)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
    
