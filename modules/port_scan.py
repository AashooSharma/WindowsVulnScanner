# port_scan.py
import socket

def scan_ports(target_ip, ports_list=None, timeout=1):
    """
    Scans the given ports on the target IP.
    If ports_list is None, scan common ports.
    """
    if ports_list is None:
        ports_list = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3389]  # common ports

    open_ports = []
    for port in ports_list:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        try:
            result = s.connect_ex((target_ip, port))
            if result == 0:
                open_ports.append(port)
        except Exception as e:
            print(f"Error scanning port {port}:", e)
        finally:
            s.close()

    return open_ports

if __name__ == "__main__":
    target = "127.0.0.1"  # Localhost example
    open_ports = scan_ports(target)
    print(f"Open ports on {target}:", open_ports)
