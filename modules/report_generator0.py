import csv
from datetime import datetime
import os

# Optional PDF export
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from reportlab.lib import colors
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False


def generate_csv_report(filename, system_info, users, weak_users, open_ports, network_devices):
    """
    Generates a more professional CSV report.
    """
    with open(filename, mode='w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(["=== Windows Vulnerability & Network Scan Report ==="])
        writer.writerow([])

        # System Info
        writer.writerow(["System Information"])
        for key, value in system_info.items():
            writer.writerow([key, value])
        writer.writerow([])

        # Users
        writer.writerow(["User Accounts"])
        writer.writerow(["Detected Users", ", ".join(users)])
        writer.writerow(["Potential Weak/Default Users", ", ".join(weak_users) if weak_users else "None"])
        writer.writerow([])

        # Open Ports
        writer.writerow(["Open Ports & Services"])
        for ip, ports in open_ports.items():
            if ports:
                writer.writerow([f"{ip}", ", ".join(map(str, ports))])
            else:
                writer.writerow([f"{ip}", "No open ports found"])
        writer.writerow([])

        # Network Devices
        writer.writerow(["Network Devices Detected"])
        for ip, ports in network_devices.items():
            writer.writerow([f"{ip}", ", ".join(map(str, ports)) if ports else "No open ports"])
        writer.writerow([])

        # Security Findings Section
        writer.writerow(["Security Findings & Recommendations"])
        if "Administrator" in users or "Guest" in users:
            writer.writerow(["Default Accounts Enabled", "Disable or rename Administrator/Guest accounts"])
        if any("445" in str(p) for p in open_ports.values()):
            writer.writerow(["SMB Port Open (445)", "Restrict or firewall SMB, patch system"])
        if any("80" in str(p) for p in open_ports.values()):
            writer.writerow(["HTTP Detected", "Use HTTPS (TLS 1.2/1.3) instead of HTTP"])

    print(f"✅ CSV report generated: {filename}")


def generate_pdf_report(filename, system_info, users, weak_users, open_ports, network_devices):
    """
    Generates a professional PDF report using reportlab.
    """
    if not PDF_AVAILABLE:
        print("⚠️ PDF report generation not available. Install reportlab first.")
        return

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
    for key, value in system_info.items():
        c.drawString(60, y, f"{key}: {value}")
        y -= 15
    y -= 10

    # Users
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "👤 User Accounts")
    y -= 20
    c.setFont("Helvetica", 11)
    c.drawString(60, y, f"Detected Users: {', '.join(users)}")
    y -= 15
    c.drawString(60, y, f"Weak/Default Users: {', '.join(weak_users) if weak_users else 'None'}")
    y -= 20

    # Open Ports
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "🌐 Open Ports & Services")
    y -= 20
    c.setFont("Helvetica", 11)
    for ip, ports in open_ports.items():
        if ports:
            c.drawString(60, y, f"{ip}: {', '.join(map(str, ports))}")
        else:
            c.drawString(60, y, f"{ip}: No open ports found")
        y -= 15
    y -= 20

    # Network Devices
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "🖧 Network Devices")
    y -= 20
    c.setFont("Helvetica", 11)
    for ip, ports in network_devices.items():
        c.drawString(60, y, f"{ip}: {', '.join(map(str, ports)) if ports else 'No open ports'}")
        y -= 15
    y -= 20

    # Security Findings
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(colors.red)
    c.drawString(50, y, "🚨 Security Findings & Recommendations")
    y -= 20
    c.setFont("Helvetica", 11)
    c.setFillColor(colors.black)

    if "Administrator" in users or "Guest" in users:
        c.drawString(60, y, "- Default accounts enabled → Disable/rename Administrator & Guest")
        y -= 15
    if any("445" in str(p) for p in open_ports.values()):
        c.drawString(60, y, "- SMB Port 445 open → Patch system & restrict via firewall")
        y -= 15
    if any("80" in str(p) for p in open_ports.values()):
        c.drawString(60, y, "- HTTP service detected → Switch to HTTPS (TLS 1.2/1.3)")
        y -= 15

    c.save()
    print(f"✅ PDF report generated: {filename}")


if __name__ == "__main__":
    # Sample test
    system_info = {
        "Hostname": "DESKTOP-A",
        "OS": "Windows 10 Pro",
        "IP": "192.168.1.5",
        "CPU": "8 cores",
        "RAM": "16 GB"
    }
    users = ["Admin", "Guest", "Aashoo"]
    weak_users = ["Admin", "Guest"]
    open_ports = {"192.168.1.5": [21, 80, 445]}
    network_devices = {"192.168.1.10": [22, 80], "192.168.1.15": []}

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("reports", exist_ok=True)

    generate_csv_report(f"reports/system_report_{timestamp}.csv",
                        system_info, users, weak_users, open_ports, network_devices)
    generate_pdf_report(f"reports/system_report_{timestamp}.pdf",
                        system_info, users, weak_users, open_ports, network_devices)
