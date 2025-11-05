import sys
import json
import math  # If you want to use math.inf for infinity

def dijkstras_shortest_path(routers, src_ip, dest_ip):
    """
    This function takes a dictionary representing the network, a source
    IP, and a destination IP, and returns a list with all the routers
    along the shortest path.

    The source and destination IPs are **not** included in this path.

    Note that the source IP and destination IP will probably not be
    routers! They will be on the same subnet as the router. You'll have
    to search the routers to find the one on the same subnet as the
    source IP. Same for the destination IP. [Hint: make use of your
    find_router_for_ip() function from the last project!]

    The dictionary keys are router IPs, and the values are dictionaries
    with a bunch of information, including the routers that are directly
    connected to the key.

    This partial example shows that router `10.31.98.1` is connected to
    three other routers: `10.34.166.1`, `10.34.194.1`, and `10.34.46.1`:

    {
        "10.34.98.1": {
            "connections": {
                "10.34.166.1": {
                    "netmask": "/24",
                    "interface": "en0",
                    "ad": 70
                },
                "10.34.194.1": {
                    "netmask": "/24",
                    "interface": "en1",
                    "ad": 93
                },
                "10.34.46.1": {
                    "netmask": "/24",
                    "interface": "en2",
                    "ad": 64
                }
            },
            "netmask": "/24",
            "if_count": 3,
            "if_prefix": "en"
        },
        ...

    The "ad" (Administrative Distance) field is the edge weight for that
    connection.

    **Strong recommendation**: make functions to do subtasks within this
    function. Having it all built as a single wall of code is a recipe
    for madness.
    """
    
    to_visit = []
    distance = {}
    parent = {}
    for ip in routers:
        distance[ip] = math.inf
        parent[ip] = None

    # Encode Source and Destination IPs into Router IPs
    src_ip = find_router_for_ip(routers, src_ip)
    dest_ip = find_router_for_ip(routers, dest_ip)

    distance[src_ip] = 0
    to_visit.append(src_ip)

    while to_visit:
        current_ip = min(to_visit, key=lambda k: distance[k]) # The evil line of code
        to_visit.remove(current_ip)

        # Check if the destination IP is reached
        if current_ip == dest_ip:
            path = []
            if src_ip == dest_ip:
                return path 
            temp_ip = current_ip
            while temp_ip is not None:
                path.insert(0, temp_ip)
                temp_ip = parent[temp_ip]
            return path

        # Check the neighbor paths of the current IP
        for neighbor_ip, neighbor_ip_info in routers[current_ip]["connections"].items():
            alt_dist = distance[current_ip] + neighbor_ip_info["ad"]
            if alt_dist < distance[neighbor_ip]:
                distance[neighbor_ip] = alt_dist
                parent[neighbor_ip] = current_ip
                to_visit.append(neighbor_ip)
    return

#-----------------
# HELPER FUNCTIONS
#-----------------
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
    ip1_subnet = ipv4_to_value(ip1) & get_subnet_mask_value(slash)
    ip2_subnet = ipv4_to_value(ip2) & get_subnet_mask_value(slash)
    return ip1_subnet == ip2_subnet

def find_router_for_ip(routers, ip):
    for route_ip, netmask in routers.items():
        if ips_same_subnet(route_ip, ip, netmask["netmask"]):
            return route_ip
    return None
#------------------------------
# DO NOT MODIFY BELOW THIS LINE
#------------------------------
def read_routers(file_name):
    with open(file_name) as fp:
        data = fp.read()

    return json.loads(data)

def find_routes(routers, src_dest_pairs):
    for src_ip, dest_ip in src_dest_pairs:
        path = dijkstras_shortest_path(routers, src_ip, dest_ip)
        print(f"{src_ip:>15s} -> {dest_ip:<15s}  {repr(path)}")

def usage():
    print("usage: dijkstra.py infile.json", file=sys.stderr)

def main(argv):
    try:
        router_file_name = argv[1]
    except:
        usage()
        return 1

    json_data = read_routers(router_file_name)

    routers = json_data["routers"]
    routes = json_data["src-dest"]

    find_routes(routers, routes)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
    
