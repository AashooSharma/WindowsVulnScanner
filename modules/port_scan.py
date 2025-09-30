# port_scan.py
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Iterable, List, Tuple, Optional

COMMON_PORTS = {
    # Standard ports
    20: "FTP Data",
    21: "FTP Control",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    67: "DHCP Server",
    68: "DHCP Client",
    69: "TFTP",
    80: "HTTP",
    110: "POP3",
    123: "NTP",
    135: "MS RPC",
    137: "NetBIOS Name Service",
    138: "NetBIOS Datagram Service",
    139: "NetBIOS Session Service",
    143: "IMAP",
    161: "SNMP",
    162: "SNMP Trap",
    389: "LDAP",
    443: "HTTPS",
    445: "SMB",
    465: "SMTPS",
    514: "Syslog",
    587: "SMTP (Submission)",
    631: "IPP (Printing)",
    993: "IMAPS",
    995: "POP3S",
    1433: "MSSQL",
    1521: "Oracle DB",
    2049: "NFS",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    5900: "VNC",
    6379: "Redis",
    8080: "HTTP Alternate",
    8443: "HTTPS Alternate",

    # Common dev/web framework ports
    3000: "Node/React (dev) / Next.js / Express",
    3001: "Node alternate",
    3002: "React alternate",
    3003: "React alternate",
    4000: "Generic dev server",
    4200: "Angular (ng serve)",
    5000: "Flask (default)",
    5173: "Vite (React/Vue/Svelte dev)",
    5500: "Live Server (VSCode)",
    8000: "Django dev / HTTP",
    9000: "Dev server / static host",
    9229: "Node Inspector (debug)",
    1234: "Parcel dev",
    35729: "LiveReload"
}


def scan_port(target_ip: str, port: int, timeout: float = 1.0) -> Optional[Tuple[int, str]]:
    """Scan a single port. Return (port, service) if open, otherwise None."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((target_ip, port))
            if result == 0:
                service = COMMON_PORTS.get(port, "Unknown/Custom")
                return (port, service)
    except Exception:
        return None
    return None


def scan_ports(target_ip: str,
               ports_list: Optional[Iterable[int]] = None,
               timeout: float = 1.0,
               max_threads: int = 200) -> List[Tuple[int, str]]:
    """
    Scan multiple ports fast using multithreading.
    If ports_list is None, scan all ports present in COMMON_PORTS.
    Returns a sorted list of tuples (port, service).
    """
    # If no ports specified, scan all keys from COMMON_PORTS
    if ports_list is None:
        ports_list = sorted(COMMON_PORTS.keys())

    # Convert to list (allow range() etc.)
    ports = list(ports_list)

    open_ports: List[Tuple[int, str]] = []
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_to_port = {executor.submit(scan_port, target_ip, port, timeout): port for port in ports}
        for future in as_completed(future_to_port):
            try:
                result = future.result()
                if result:
                    open_ports.append(result)
            except Exception:
                # ignore individual worker errors
                continue

    return sorted(open_ports, key=lambda x: x[0])


# Quick test (only run when this file executed directly)
if __name__ == "__main__":
    target = "127.0.0.1"  # replace with your target IP
    print(f"Scanning {target} on selected ports...")
    open_ports = scan_ports(target, timeout=0.8, max_threads=300)

    if open_ports:
        print(f"\nOpen ports detected on {target}:")
        for port, service in open_ports:
            print(f"Port {port} ({service})")
    else:
        print(f"No open ports detected on {target}.")
        print("Hints: 1) run services that you expect to be open, 2) check firewall, 3) try scanning from another machine in the network.")
