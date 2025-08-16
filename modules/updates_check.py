# updates_check.py
import subprocess

def get_installed_updates():
    """
    Returns a list of installed Windows updates (KB numbers) using WMIC.
    """
    try:
        # Run WMIC command to fetch installed hotfixes
        output = subprocess.check_output(
            "wmic qfe get HotFixID, InstalledOn /format:table",
            shell=True,
            stderr=subprocess.DEVNULL
        )
        output = output.decode(errors="ignore").splitlines()

        updates = []
        for line in output:
            line = line.strip()
            if line.startswith("KB"):  # Only take lines starting with KB
                parts = line.split()
                kb = parts[0]
                updates.append(kb)

        return updates

    except Exception as e:
        print("Error fetching updates:", e)
        return []


if __name__ == "__main__":
    updates = get_installed_updates()
    if updates:
        print("✅ Installed Windows Updates (KB):")
        for kb in updates:
            print(" -", kb)
    else:
        print("⚠️ No updates found or unable to fetch.")
