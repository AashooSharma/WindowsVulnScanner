from flask import Flask, render_template, jsonify
from modules import system_info, user_accounts, port_scan, updates_check, network_scan, report_generator
from datetime import datetime
import os
import threading
import time

app = Flask(__name__)

# Global variable to store scan status
scan_status = {
    "progress": 0,
    "status": "Idle",
    "result": None
}

def run_full_scan():
    global scan_status
    # 1️⃣ System Info
    scan_status["progress"] = 10
    scan_status["status"] = "Getting system info..."
    sys_info = system_info.get_system_info()
    time.sleep(1)

    # 2️⃣ User Accounts
    scan_status["progress"] = 25
    scan_status["status"] = "Checking users..."
    users = user_accounts.get_user_accounts()
    weak_users = user_accounts.check_weak_passwords(users)
    time.sleep(1)

    # 3️⃣ Open Ports
    scan_status["progress"] = 40
    scan_status["status"] = "Scanning local ports..."
    target_ip = sys_info['IP Address']
    open_ports_local = {target_ip: port_scan.scan_ports(target_ip)}
    time.sleep(1)

    # 4️⃣ Installed Updates
    scan_status["progress"] = 55
    scan_status["status"] = "Checking installed updates..."
    updates = updates_check.get_installed_updates()
    time.sleep(1)

    # 5️⃣ Network Scan
    scan_status["progress"] = 70
    scan_status["status"] = "Scanning network devices..."
    subnet = ".".join(target_ip.split(".")[:3]) + "."
    network_devices = network_scan.scan_network(subnet=subnet, start=1, end=10)
    time.sleep(1)

    # 6️⃣ Generate Reports
    scan_status["progress"] = 90
    scan_status["status"] = "Generating reports..."
    os.makedirs("reports", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"reports/system_report_{timestamp}.csv"
    pdf_filename = f"reports/system_report_{timestamp}.pdf"
    report_generator.generate_csv_report(csv_filename, sys_info, users, weak_users, open_ports_local, network_devices)
    report_generator.generate_pdf_report(pdf_filename, sys_info, users, weak_users, open_ports_local, network_devices)

    scan_status["progress"] = 100
    scan_status["status"] = "Scan complete!"
    scan_status["result"] = {
        "sys_info": sys_info,
        "users": users,
        "weak_users": weak_users,
        "open_ports": open_ports_local,
        "updates": updates[:5],
        "network_devices": network_devices,
        "report_csv": csv_filename,
        "report_pdf": pdf_filename
    }

@app.route("/")
def dashboard():
    return render_template("index.html")

@app.route("/start_scan")
def start_scan():
    # Run scan in a separate thread
    threading.Thread(target=run_full_scan).start()
    return render_template("scan_progress.html")

@app.route("/scan_status")
def get_scan_status():
    return jsonify(scan_status)

@app.route("/show_results")
def show_results():
    if scan_status["result"]:
        r = scan_status["result"]
        return render_template(
            "scan.html",
            sys_info=r["sys_info"],
            users=r["users"],
            weak_users=r["weak_users"],
            open_ports=r["open_ports"],
            updates=r["updates"],
            network_devices=r["network_devices"],
            report_csv=r["report_csv"],
            report_pdf=r["report_pdf"]
        )
    else:
        return "Scan not finished yet. Please wait..."

if __name__ == "__main__":
    app.run(debug=True)
