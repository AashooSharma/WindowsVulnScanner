# main.py
from modules import report_generator, system_info, user_accounts, port_scan, updates_check, network_scan
from datetime import datetime
import os

def main():
    print("=== Windows Vulnerability & Network Scanner ===\n")

    # 1️⃣ System Information
    sys_info = system_info.get_system_info()
    print("System Information:")
    for key, value in sys_info.items():
        print(f"{key}: {value}")
    print("\n")

    # 2️⃣ User Accounts
    users = user_accounts.get_user_accounts()
    weak_users = user_accounts.check_weak_passwords(users)
    print("Users Detected:", users)
    print("Potential Weak Users:", weak_users, "\n")

    # 3️⃣ Open Ports (Local system)
    target_ip = sys_info['IP Address']
    open_ports_local = {target_ip: port_scan.scan_ports(target_ip)}
    print(f"Open Ports on {target_ip}:", open_ports_local[target_ip], "\n")

    # 4️⃣ Installed Updates
    updates = updates_check.get_installed_updates()
    print(f"Installed Updates (Total: {len(updates)}):", updates[:5], "...")  # show first 5 updates
    print("\n")

    # 5️⃣ Network Scan (Optional: small range)
    subnet = ".".join(target_ip.split(".")[:3]) + "."
    print(f"Scanning network {subnet}1-10 ...")
    network_devices = network_scan.scan_network(subnet=subnet, start=1, end=10)
    for ip, ports in network_devices.items():
        print(f"{ip} - Open Ports: {ports}")
    print("\n")

    # 6️⃣ Report Generation
    os.makedirs("reports", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"reports/system_report_{timestamp}.csv"
    pdf_filename = f"reports/system_report_{timestamp}.pdf"

    report_generator.generate_csv_report(csv_filename, sys_info, users, weak_users, open_ports_local, network_devices)
    report_generator.generate_pdf_report(pdf_filename, sys_info, users, weak_users, open_ports_local, network_devices)

    print("\nScan Complete! Reports generated in 'reports/' folder.")

if __name__ == "__main__":
    main()
