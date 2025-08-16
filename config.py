# config.py

# Default network scan options
SCAN_TYPE = "full"       # fast, full, vuln
TIMEOUT = 2              # seconds

# Ports to scan (common)
COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 3306, 3389]

# Report settings
REPORT_FORMAT = "json"   # options: json, csv, html
REPORT_PATH = "reports/"

# Logging
LOG_LEVEL = "INFO"       # DEBUG, INFO, WARNING, ERROR

# Vulnerability DB (local JSON or API)
VULN_DB_PATH = "data/vuln_signatures.json"

# Banner grabbing options
BANNER_GRAB = True
BANNER_MAX_BYTES = 1024
