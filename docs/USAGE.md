# Usage Guide — IT Helpdesk Automation Toolkit

## Prerequisites

```bash
pip install -r requirements.txt
```

## Scripts

### disk_monitor.py
```bash
# Basic usage — check all drives
python scripts/disk_monitor.py

# Alert if any drive > 80% full
python scripts/disk_monitor.py --threshold 80

# Generate CSV report
python scripts/disk_monitor.py --output disk_report.csv

# Send email alert
python scripts/disk_monitor.py --threshold 80 --email admin@company.com
```

### network_diag.py
```bash
# Scan a full subnet
python scripts/network_diag.py --subnet 192.168.1.0/24

# Check specific host and ports
python scripts/network_diag.py --host google.com --ports 80,443

# Generate HTML report
python scripts/network_diag.py --subnet 192.168.1.0/24 --output report.html

# JSON output
python scripts/network_diag.py --subnet 10.0.0.0/24 --json
```

### hw_inventory.py
```bash
# Print hardware summary
python scripts/hw_inventory.py

# Export as CSV
python scripts/hw_inventory.py --output inventory.csv

# Export as JSON
python scripts/hw_inventory.py --format json
```

### log_parser.py
```bash
# Analyze last 24 hours
python scripts/log_parser.py --file /var/log/nginx/error.log

# Analyze last 48 hours, JSON output
python scripts/log_parser.py --file /var/log/syslog --last 48 --format json
```

### user_onboard.sh
```bash
# Create a new user
sudo bash scripts/user_onboard.sh --username jdoe --fullname "Jane Doe" --group developers

# Create with custom group
sudo bash scripts/user_onboard.sh --username bsmith --fullname "Bob Smith" --group admins
```

## Windows (PowerShell) Equivalents

Most Python scripts work cross-platform. For PowerShell-specific variants, see the `scripts/windows/` directory (coming soon).