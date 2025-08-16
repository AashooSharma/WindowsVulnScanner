# report_generator.py
import csv
from datetime import datetime
# Optional PDF export
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

def generate_csv_report(filename, system_info, users, weak_users, open_ports, network_devices):
    """
    Generates a CSV report.
    """
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Section", "Details"])
        # System Info
        for key, value in system_info.items():
            writer.writerow([key, value])
        writer.writerow([])
        # Users
        writer.writerow(["Users", ", ".join(users)])
        writer.writerow(["Potential Weak Users", ", ".join(weak_users)])
        writer.writerow([])
        # Open Ports
        for ip, ports in open_ports.items():
            writer.writerow([f"Open Ports for {ip}", ", ".join(map(str, ports))])
        writer.writerow([])
        # Network Devices
        for ip, ports in network_devices.items():
            writer.writerow([f"Device {ip}", ", ".join(map(str, ports))])

    print(f"CSV report generated: {filename}")

def generate_pdf_report(filename, system_info, users, weak_users, open_ports, network_devices):
    """
    Optional: Generates PDF report using reportlab
    """
    if not PDF_AVAILABLE:
        print("PDF report generation not available. Install reportlab first.")
        return

    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    y = height - 50

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Windows Vulnerability & Network Scan Report")
    y -= 30
    c.setFont("Helvetica", 12)

    # System Info
    c.drawString(50, y, "System Info:")
    y -= 20
    for key, value in system_info.items():
        c.drawString(60, y, f"{key}: {value}")
        y -= 15

    # Users
    y -= 10
    c.drawString(50, y, "Users:")
    y -= 15
    c.drawString(60, y, ", ".join(users))
    y -= 15
    c.drawString(60, y, "Potential Weak Users: " + ", ".join(weak_users))

    # Open Ports
    y -= 20
    for ip, ports in open_ports.items():
        c.drawString(50, y, f"Open Ports for {ip}: {', '.join(map(str, ports))}")
        y -= 15

    # Network Devices
    y -= 10
    for ip, ports in network_devices.items():
        c.drawString(50, y, f"Device {ip}: {', '.join(map(str, ports))}")
        y -= 15

    c.save()
    print(f"PDF report generated: {filename}")

if __name__ == "__main__":
    # Sample data for demo
    system_info = {"Hostname": "DESKTOP-A", "OS": "Windows 10 Pro", "IP": "192.168.1.5"}
    users = ["Admin", "Guest"]
    weak_users = ["Guest"]
    open_ports = {"192.168.1.5": [21, 80, 3389]}
    network_devices = {"192.168.1.10": [22, 80]}
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    generate_csv_report(f"reports/system_report_{timestamp}.csv", system_info, users, weak_users, open_ports, network_devices)
    generate_pdf_report(f"reports/system_report_{timestamp}.pdf", system_info, users, weak_users, open_ports, network_devices)
