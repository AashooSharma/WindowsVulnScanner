# dashboard.py
import tkinter as tk
from tkinter import messagebox, scrolledtext
from modules import main as scanner_main
import threading

def run_scan():
    """
    Run the scanner in a separate thread to avoid freezing GUI
    """
    def scan_thread():
        output_text.delete(1.0, tk.END)
        try:
            # Redirect print to GUI
            import sys
            class Redirect:
                def write(self, s):
                    output_text.insert(tk.END, s)
                    output_text.see(tk.END)
                def flush(self): pass
            sys.stdout = Redirect()
            scanner_main.main()
            sys.stdout = sys.__stdout__
            messagebox.showinfo("Scan Complete", "Scan finished! Reports saved in 'reports/' folder.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    threading.Thread(target=scan_thread).start()

# Create main window
root = tk.Tk()
root.title("Windows Vulnerability & Network Scanner")
root.geometry("700x500")

# Header label
header = tk.Label(root, text="Windows Vulnerability & Network Scanner", font=("Arial", 16, "bold"))
header.pack(pady=10)

# Run Scan button
scan_button = tk.Button(root, text="Run Full Scan", font=("Arial", 14), bg="green", fg="white", command=run_scan)
scan_button.pack(pady=10)

# Output area
output_text = scrolledtext.ScrolledText(root, width=80, height=20, font=("Consolas", 10))
output_text.pack(pady=10)

# Run GUI
root.mainloop()
