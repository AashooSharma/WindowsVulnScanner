# full_port_scan.py
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

# Common ports and their services
COMMON_PORTS = {
    20: "FTP Data",
    21: "FTP Control",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3389: "RDP",
}

def scan_port(target_ip, port, timeout=1):
    """Scan a single port. Return (port, service) if open."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            if s.connect_ex((target_ip, port)) == 0:
                service = COMMON_PORTS.get(port, "Unknown")
                return (port, service)
    except:
        return None
    return None

def scan_ports(target_ip, ports_list=None, timeout=1, max_threads=500):
    """
    Scan multiple ports fast using multithreading.
    Returns a list of tuples (port, service).
    """
    if ports_list is None:
        ports_list = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3389]  # common ports
        
        #ports_list = range(1, 65536)  # All TCP ports

    open_ports = []
    with ThreadPoolExecutor(max_threads) as executor:
        future_to_port = {executor.submit(scan_port, target_ip, port, timeout): port for port in ports_list}
        for future in as_completed(future_to_port):
            result = future.result()
            if result:
                open_ports.append(result)

    return sorted(open_ports, key=lambda x: x[0])

if __name__ == "__main__":
    target = "127.0.0.1"  # Replace with target IP
    print(f"Scanning {target} on all TCP ports...")
    open_ports = scan_ports(target, timeout=0.5, max_threads=500)  # timeout can be smaller for faster scan

    if open_ports:
        print(f"\nOpen ports detected on {target}:")
        for port, service in open_ports:
            print(f"Port {port} ({service})")
    else:
        print(f"No open ports detected on {target}")
