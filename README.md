# IT Helpdesk Automation Toolkit

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![Bash](https://img.shields.io/badge/Bash-Scripting-4EAA25?style=flat-square&logo=gnubash&logoColor=white)
![PowerShell](https://img.shields.io/badge/PowerShell-Windows-2CA5E0?style=flat-square&logo=powershell&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-Ubuntu-FCC624?style=flat-square&logo=linux&logoColor=black)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey?style=flat-square)

**Real, production-tested automation scripts for IT helpdesk and systems administration** — born from hands-on experience at BICT (Kigali) and COPE Solutions Canada.

</div>

---

## 🎯 Why This Exists

Every IT technician spends hours on repetitive tasks: checking disk space, onboarding users, diagnosing network issues, parsing error logs. This toolkit automates all of it — freeing you to focus on what actually requires human judgment.

> "The best IT support engineer automates themselves out of the repetitive work."

## 🧰 Toolkit Contents

### 1. 📊 Disk Usage Monitor (`scripts/disk_monitor.py`)
Automatically checks disk usage across all mounted volumes. Sends an email alert when usage exceeds a configurable threshold.

```bash
python scripts/disk_monitor.py --threshold 80 --email admin@company.com
```

**Features:**
- Checks all mounted drives/volumes
- Configurable alert threshold (default: 80%)
- Email notification with detailed breakdown
- CSV report generation
- Works on Linux, macOS, and Windows

---

### 2. 👤 User Onboarding Script (`scripts/user_onboard.sh`)
Automates new employee setup on Linux servers.

```bash
sudo bash scripts/user_onboard.sh --username jdoe --fullname "Jane Doe" --group developers
```

**Features:**
- Creates user account with secure random password
- Assigns to specified groups
- Sets up SSH key directory
- Creates home directory structure
- Sends welcome email with credentials

---

### 3. 🌐 Network Diagnostics (`scripts/network_diag.py`)
Comprehensive network health checker — ping sweep, port scan, DNS resolution, and latency reporting.

```bash
python scripts/network_diag.py --subnet 192.168.1.0/24 --ports 22,80,443,3389
```

**Features:**
- ICMP ping sweep across subnet
- TCP port availability check
- DNS resolution test
- Latency statistics (min/avg/max)
- Exports results as JSON or HTML report

---

### 4. 📋 Hardware Inventory Report (`scripts/hw_inventory.py`)
Generates a full hardware inventory report — CPU, RAM, disk, network adapters.

```bash
python scripts/hw_inventory.py --output inventory_report.csv
```

**Features:**
- CPU model, core count, frequency
- RAM total and available
- Disk partitions, sizes, filesystems
- Network interfaces and MAC addresses
- Exports to CSV, JSON, or HTML

---

### 5. 🔍 Log Parser & Error Analyzer (`scripts/log_parser.py`)
Parses server logs (Nginx, Apache, syslog, application logs) and extracts patterns, errors, and anomalies.

```bash
python scripts/log_parser.py --file /var/log/nginx/error.log --last 24h --format html
```

**Features:**
- Parses Nginx, Apache, syslog, and custom formats
- Time-range filtering
- Groups similar errors with occurrence counts
- Identifies top error sources by IP
- Generates HTML or JSON report

---

## 📁 Project Structure

```
it-helpdesk-automation/
├── scripts/
│   ├── disk_monitor.py      # Disk usage alerting
│   ├── user_onboard.sh      # Linux user onboarding
│   ├── user_offboard.sh     # Linux user removal (revokes access)
│   ├── network_diag.py      # Network diagnostics
│   ├── hw_inventory.py      # Hardware inventory reporter
│   ├── log_parser.py        # Server log analyzer
│   └── port_scanner.py      # TCP port scanner
├── docs/
│   ├── USAGE.md             # Detailed usage guide
│   └── SCREENSHOTS.md       # Example output screenshots
├── tests/
│   └── test_scripts.py      # Unit tests for Python scripts
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 Quick Start

```bash
# 1. Clone
git clone https://github.com/Manziine/it-helpdesk-automation.git
cd it-helpdesk-automation

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Run any script
python scripts/disk_monitor.py --threshold 80
python scripts/network_diag.py --subnet 192.168.1.0/24
python scripts/hw_inventory.py
```

## 💡 Real-World Context

These scripts were developed and refined through:
- **ICT Support Technician** work at BICT, Kigali — managing local networks, server infrastructure, and hardware diagnostics
- **Customer Service Representative** at COPE Solutions Canada — high-volume technical issue resolution
- **AI Software Engineer** at Verlet Robotics — automating data pipeline verification and system monitoring

## 🛠️ Built By

**Arnaud Ineza Manzi** — Backend Engineer & IT Systems Professional  
📍 Ottawa, Canada | 📧 ainezamanzi@gmail.com | 🔗 [LinkedIn](https://linkedin.com/in/arnaud-ineza-manzi-471221272)

---

*MIT License — use freely in production.*
