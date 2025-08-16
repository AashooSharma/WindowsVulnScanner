# user_accounts.py
import subprocess

def get_user_accounts():
    """
    Returns a clean list of Windows user accounts
    """
    try:
        output = subprocess.check_output("net user", shell=True, text=True, stderr=subprocess.DEVNULL)
        users = []

        # Parse 'net user' output
        capture = False
        for line in output.splitlines():
            line = line.strip()
            if not line:
                continue

            # Start capturing after dashes
            if "----" in line:
                capture = not capture
                continue

            if capture:
                # Skip footer line
                if "The command completed successfully" in line:
                    continue

                # Split by spaces and filter blanks
                users.extend([u for u in line.split() if u])

        return users

    except Exception as e:
        print("Error fetching users:", e)
        return []

def check_weak_passwords(users_list):
    """
    Placeholder function: Just flags common accounts as 'check password manually'
    """
    weak_users = []
    common_users = ["Guest", "Admin", "Administrator"]
    for user in users_list:
        if user in common_users:
            weak_users.append(user)
    return weak_users

if __name__ == "__main__":
    users = get_user_accounts()
    print("Detected Users:", users)
    weak_users = check_weak_passwords(users)
    print("Potential Weak/Default Users:", weak_users)
