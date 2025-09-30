# updates_check.py
import subprocess
from typing import List, Tuple

def get_installed_updates(limit: int = 50) -> List[Tuple[str, str]]:
    """
    Returns installed Windows updates (KB + InstalledOn date) using PowerShell.
    Works on modern Windows versions.
    :param limit: Maximum number of updates to return
    :return: List of tuples [(KB, InstalledOn), ...]
    """
    try:
        # PowerShell command to get installed updates
        ps_cmd = "Get-HotFix | Select-Object HotFixID, InstalledOn | Format-Table -AutoSize"
        output = subprocess.check_output(["powershell", "-Command", ps_cmd], stderr=subprocess.DEVNULL)
        lines = output.decode(errors="ignore").splitlines()

        updates = []
        for line in lines:
            line = line.strip()
            # Skip header and empty lines
            if not line or line.lower().startswith("hotfixid"):
                continue

            parts = line.split()
            if len(parts) >= 2:
                kb = parts[0]
                installed_on = parts[1]
                updates.append((kb, installed_on))
            elif len(parts) == 1:
                updates.append((parts[0], "Unknown"))

        return updates[:limit]

    except Exception as e:
        print("⚠️ Error fetching updates:", e)
        return []


if __name__ == "__main__":
    updates = get_installed_updates()
    if updates:
        print("✅ Installed Windows Updates (KB + InstalledOn):")
        for kb, date in updates:
            print(f" - {kb} ({date})")
    else:
        print("⚠️ No updates found or unable to fetch.")
