# updates_check.py
import subprocess

def get_installed_updates():
    """
    Returns a list of installed Windows updates (KB numbers)
    """
    try:
        output = subprocess.check_output("wmic qfe list brief", shell=True, stderr=subprocess.DEVNULL)
        output = output.decode().splitlines()
        updates = []

        # Skip header lines and parse KB numbers
        for line in output[1:]:
            parts = line.split()
            if len(parts) > 0:
                kb = parts[0]  # First column usually KB number
                updates.append(kb)
        return updates
    except Exception as e:
        print("Error fetching updates:", e)
        return []

if __name__ == "__main__":
    updates = get_installed_updates()
    print("Installed Windows Updates (KB):")
    for kb in updates:
        print(kb)
