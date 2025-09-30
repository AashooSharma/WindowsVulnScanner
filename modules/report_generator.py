# modules/report_generator.py
import csv
from datetime import datetime
import os

# Optional PDF export
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from reportlab.lib import colors
    PDF_AVAILABLE = True

    # Patch for ReportLab md5 issue (Python 3.8+ / OpenSSL 3)
    import reportlab.pdfbase.pdfdoc as pdfdoc
    import hashlib
    pdfdoc.md5 = lambda *args, **kwargs: hashlib.md5()

except ImportError:
    PDF_AVAILABLE = False

# Service name mapping (keep in sync with your port_scan COMMON_PORTS)
COMMON_PORTS = {
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
    3000: "Node/React (dev) / Next.js / Express",
    3001: "Node alternate",
    3002: "React alternate",
    3003: "React alternate",
    4000: "Generic dev server",
    4200: "Angular (ng serve)",
    5000: "Flask (default)",
    5173: "Vite (dev)",
    5500: "Live Server (VSCode)",
    8000: "Django dev / HTTP",
    9000: "Dev server / static host",
    9229: "Node Inspector (debug)",
    1234: "Parcel dev",
    35729: "LiveReload"
}


def _normalize_open_ports(open_ports):
    """
    Normalize open_ports to dict[ip] = [(port, service_name), ...]
    Supports input where open_ports values are either:
      - list of ints [80, 443], or
      - list of tuples [(80, "HTTP"), ...] (as produced by updated port_scan)
    """
    normalized = {}
    for ip, ports in (open_ports or {}).items():
        normalized[ip] = []
        if not ports:
            continue
        # detect element type
        first = ports[0]
        if isinstance(first, tuple) and len(first) >= 1:
            # already tuple list: ensure service present
            for entry in ports:
                if entry is None:
                    continue
                if isinstance(entry, (list, tuple)) and len(entry) >= 1:
                    p = int(entry[0])
                    svc = entry[1] if len(entry) > 1 and entry[1] else COMMON_PORTS.get(p, "Unknown/Custom")
                    normalized[ip].append((p, svc))
        else:
            # assume list of ints
            for p in ports:
                try:
                    port_num = int(p)
                except Exception:
                    continue
                svc = COMMON_PORTS.get(port_num, "Unknown/Custom")
                normalized[ip].append((port_num, svc))
    return normalized


def _format_ports_for_csv(ports_tuples):
    """Return comma separated 'port (service)' strings for CSV row."""
    return ", ".join([f"{p} ({svc})" for p, svc in ports_tuples]) if ports_tuples else "None"


def generate_csv_report(filename, system_info, users, weak_users, open_ports, network_devices):
    """
    Generates a professional CSV report.
    open_ports: dict { ip: [port-int | (port,service), ...] }
    """
    normalized_ports = _normalize_open_ports(open_ports)

    with open(filename, mode='w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(["=== Windows Vulnerability & Network Scan Report ==="])
        writer.writerow([])

        # System Info
        writer.writerow(["System Information"])
        for key, value in (system_info or {}).items():
            writer.writerow([key, value])
        writer.writerow([])

        # Users
        writer.writerow(["User Accounts"])
        writer.writerow(["Detected Users", ", ".join(users) if users else "None"])
        writer.writerow(["Potential Weak/Default Users", ", ".join(weak_users) if weak_users else "None"])
        writer.writerow([])

        # Open Ports
        writer.writerow(["Open Ports & Services (Local)"])
        for ip, ports in normalized_ports.items():
            writer.writerow([f"{ip}", _format_ports_for_csv(ports)])
        writer.writerow([])

        # Network Devices
        writer.writerow(["Network Devices Detected"])
        if network_devices:
            for ip, ports in (network_devices or {}).items():
                # network_devices may be dict[ip] = [int,..] or [ (port,svc), ... ]
                # reuse normalization on-the-fly
                nd = _normalize_open_ports({ip: ports})
                writer.writerow([f"{ip}", _format_ports_for_csv(nd.get(ip, []))])
        else:
            writer.writerow(["None"])
        writer.writerow([])

        # Installed updates summary placeholder (callers may pass list)
        writer.writerow(["Installed Updates (first 10)"])
        writer.writerow([])

        # Security Findings Section
        writer.writerow(["Security Findings & Recommendations"])
        if users and ("Administrator" in users or "Guest" in users):
            writer.writerow(["Default Accounts Enabled", "Disable or rename Administrator/Guest accounts"])
        # check through normalized ports for important findings
        all_ports_flat = [p for ports in normalized_ports.values() for p, s in ports]
        if any(p == 445 for p in all_ports_flat):
            writer.writerow(["SMB Port Open (445)", "Restrict or firewall SMB, patch system"])
        if any(p == 80 for p in all_ports_flat) or any(p == 8080 for p in all_ports_flat):
            writer.writerow(["HTTP Detected", "Use HTTPS (TLS 1.2/1.3) instead of HTTP"])
        if any(p in (3000, 5000, 5173, 4200) for p in all_ports_flat):
            writer.writerow(["Development Server Detected", "Check if a dev server is intentionally exposed"])

    print(f"✅ CSV report generated: {filename}")


def generate_pdf_report(filename, system_info, users, weak_users, open_ports, network_devices):
    """
    Generates a professional PDF report using reportlab.
    """
    if not PDF_AVAILABLE:
        print("⚠️ PDF report generation not available. Install reportlab first.")
        return

    normalized_ports = _normalize_open_ports(open_ports)

    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    y = height - 50

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.darkblue)
    c.drawString(50, y, "🔐 Windows Vulnerability & Network Scan Report")
    y -= 40

    c.setFillColor(colors.black)
    c.setFont("Helvetica", 12)

    # System Info
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "📌 System Information")
    y -= 20
    c.setFont("Helvetica", 11)
    for key, value in (system_info or {}).items():
        c.drawString(60, y, f"{key}: {value}")
        y -= 15
        if y < 80:
            c.showPage()
            y = height - 50

    y -= 10

    # Users
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "👤 User Accounts")
    y -= 20
    c.setFont("Helvetica", 11)
    c.drawString(60, y, f"Detected Users: {', '.join(users) if users else 'None'}")
    y -= 15
    c.drawString(60, y, f"Weak/Default Users: {', '.join(weak_users) if weak_users else 'None'}")
    y -= 20

    # Open Ports
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "🌐 Open Ports & Services (Local)")
    y -= 20
    c.setFont("Helvetica", 11)
    for ip, ports in normalized_ports.items():
        c.drawString(60, y, f"{ip}: {_format_ports_for_csv(ports)}")
        y -= 15
        if y < 80:
            c.showPage()
            y = height - 50

    y -= 20

    # Network Devices
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "🖧 Network Devices")
    y -= 20
    c.setFont("Helvetica", 11)
    if network_devices:
        for ip, ports in (network_devices or {}).items():
            nd = _normalize_open_ports({ip: ports})
            c.drawString(60, y, f"{ip}: {_format_ports_for_csv(nd.get(ip, []))}")
            y -= 15
            if y < 80:
                c.showPage()
                y = height - 50
    else:
        c.drawString(60, y, "None")
        y -= 15

    y -= 20

    # Security Findings
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(colors.red)
    c.drawString(50, y, "🚨 Security Findings & Recommendations")
    y -= 20
    c.setFont("Helvetica", 11)
    c.setFillColor(colors.black)

    all_ports_flat = [p for ports in normalized_ports.values() for p, s in ports]
    if users and ("Administrator" in users or "Guest" in users):
        c.drawString(60, y, "- Default accounts enabled → Disable/rename Administrator & Guest")
        y -= 15
    if any(p == 445 for p in all_ports_flat):
        c.drawString(60, y, "- SMB Port 445 open → Patch system & restrict via firewall")
        y -= 15
    if any(p == 80 for p in all_ports_flat) or any(p == 8080 for p in all_ports_flat):
        c.drawString(60, y, "- HTTP service detected → Switch to HTTPS (TLS 1.2/1.3)")
        y -= 15
    if any(p in (3000, 5000, 5173, 4200) for p in all_ports_flat):
        c.drawString(60, y, "- Development server detected → ensure it's not publicly exposed")
        y -= 15

    c.save()
    print(f"✅ PDF report generated: {filename}")
