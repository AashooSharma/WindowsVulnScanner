# user_accounts.py
import subprocess

def get_user_accounts():
    """
    Returns a list of Windows user accounts
    """
    try:
        output = subprocess.check_output("net user", shell=True, stderr=subprocess.DEVNULL)
        output = output.decode().splitlines()
        users = []

        # Windows 'net user' output parsing
        capture = False
        for line in output:
            if "----" in line:
                capture = not capture
                continue
            if capture:
                # Split line by spaces and filter empty strings
                users += [u for u in line.split(" ") if u]

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
