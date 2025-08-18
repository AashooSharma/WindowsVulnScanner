# network_scan.py
import os
from .port_scan import scan_ports
from concurrent.futures import ThreadPoolExecutor

# Common ports to check
COMMON_PORTS = [22, 80, 135, 139, 443, 445, 3389,5000,5500]

def ping_device(ip):
    """Pings a device to check if it's active (Windows)."""
    response = os.system(f"ping -n 1 -w 500 {ip} >nul")
    return response == 0

def scan_ip(ip, ports=None):
    """Scan a single IP and return open ports."""
    if ping_device(ip):
        open_ports = scan_ports(ip, ports)
        return (ip, open_ports)
    return (ip, [])

def scan_network(subnet="192.168.1.", start=1, end=254, ports=COMMON_PORTS, max_threads=50):
    """Scan a range of IPs in the subnet for open ports (multi-threaded)."""
    ips = [f"{subnet}{i}" for i in range(start, end + 1)]
    active_devices = {}

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        results = executor.map(lambda ip: scan_ip(ip, ports), ips)

    for ip, open_ports in results:
        if open_ports:  # Only include IPs with open ports
            active_devices[ip] = open_ports

    return active_devices

if __name__ == "__main__":
    print("Scanning local network 192.168.1.1-10 ...")
    devices = scan_network(subnet="192.168.1.", start=1, end=10)
    for ip, ports in devices.items():
        print(f"{ip} - Open Ports: {ports}")
