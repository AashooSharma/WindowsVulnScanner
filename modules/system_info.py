# system_info.py
import platform
import socket
import psutil

def get_system_info():
    system_info = {}
    system_info['Hostname'] = socket.gethostname()
    system_info['IP Address'] = socket.gethostbyname(socket.gethostname())
    system_info['OS'] = platform.system() + " " + platform.release()
    system_info['Architecture'] = platform.architecture()[0]
    system_info['CPU Cores'] = psutil.cpu_count(logical=True)
    system_info['RAM (GB)'] = round(psutil.virtual_memory().total / (1024 ** 3), 2)
    return system_info

if __name__ == "__main__":
    info = get_system_info()
    for key, value in info.items():
        print(f"{key}: {value}")
