# network_scan.py
import os
import socket
from .port_scan import scan_ports  # Import from our previous module

def ping_device(ip):
    """
    Pings a device to check if it's active.
    Returns True if ping is successful, else False.
    """
    response = os.system(f"ping -n 1 -w 1000 {ip} >nul")
    return response == 0

def scan_network(subnet="192.168.1.", start=1, end=254, ports=None):
    """
    Scans the local network for active devices and their open ports.
    subnet: e.g., '192.168.1.'
    start, end: IP range
    ports: list of ports to scan
    Returns a dictionary {IP: [open ports]}
    """
    active_devices = {}
    for i in range(start, end + 1):
        ip = f"{subnet}{i}"
        if ping_device(ip):
            open_ports = scan_ports(ip, ports)
            active_devices[ip] = open_ports
    return active_devices

if __name__ == "__main__":
    print("Scanning local network 192.168.1.1-10 ...")
    devices = scan_network(subnet="192.168.1.", start=1, end=10)
    for ip, ports in devices.items():
        print(f"{ip} - Open Ports: {ports}")
