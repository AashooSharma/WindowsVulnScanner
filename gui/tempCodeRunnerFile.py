import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import sys
import os
import glob
import subprocess
import webbrowser

# Add root project path to sys.path (so main.py is importable)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import main as scanner_main


def run_scan():
    """
    Run the scanner in a separate thread to avoid freezing GUI
    """
    def scan_thread():
        output_text.delete(1.0, tk.END)
        try:
            # Redirect print output to GUI
            class Redirect:
                def write(self, s):
                    output_text.insert(tk.END, s)
                    output_text.see(tk.END)
                def flush(self): 
                    pass

            sys.stdout = Redirect()
            scanner_main.main()   # Run the main.py scan
            sys.stdout = sys.__stdout__

            messagebox.showinfo("Scan Complete", "✅ Scan finished! Reports saved in 'reports/' folder.")
        except Exception as e:
            sys.stdout = sys.__stdout__
            messagebox.showerror("Error", str(e))

    threading.Thread(target=scan_thread, daemon=True).start()


def open_latest_report():
    """
    Open the latest CSV, PDF or MD report from 'reports/' folder
    """
    reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
    if not os.path.exists(reports_dir):
        messagebox.showerror("Error", "Reports folder not found.")
        return

    files = glob.glob(os.path.join(reports_dir, "system_report_*.*"))
    if not files:
        messagebox.showwarning("No Report", "No reports found. Please run a scan first.")
        return

    latest_file = max(files, key=os.path.getctime)
    try:
        if latest_file.endswith(".md"):
            # Open markdown file in default browser
            webbrowser.open_new_tab(f"file://{os.path.abspath(latest_file)}")
        elif sys.platform.startswith("win"):
            os.startfile(latest_file)  # Windows
        elif sys.platform == "darwin":
            subprocess.call(["open", latest_file])  # macOS
        else:
            subprocess.call(["xdg-open", latest_file])  # Linux
    except Exception as e:
        messagebox.showerror("Error", f"Could not open report: {e}")


# === GUI Setup ===
root = tk.Tk()
root.title("🔐 Windows Vulnerability & Network Scanner")
root.geometry("800x620")
root.config(bg="#f4f4f4")

# Header label
header = tk.Label(root, text="Windows Vulnerability & Network Scanner", 
                  font=("Arial", 16, "bold"), bg="#f4f4f4", fg="black")
header.pack(pady=10)

# Run Scan button
scan_button = tk.Button(root, text="▶ Run Full Scan", font=("Arial", 14), 
                        bg="green", fg="white", width=20, command=run_scan)
scan_button.pack(pady=8)

# Open Report button
report_button = tk.Button(root, text="📂 Open Latest Report", font=("Arial", 14), 
                          bg="blue", fg="white", width=20, command=open_latest_report)
report_button.pack(pady=5)

# Output area
output_frame = tk.LabelFrame(root, text=" Scan Output ", font=("Arial", 12, "bold"), 
                             bg="#f4f4f4", fg="black", padx=5, pady=5)
output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

output_text = scrolledtext.ScrolledText(output_frame, width=90, height=25, font=("Consolas", 10))
output_text.pack(fill=tk.BOTH, expand=True)

# Run GUI loop
root.mainloop()
