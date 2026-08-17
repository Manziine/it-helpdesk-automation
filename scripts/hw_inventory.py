#!/usr/bin/env python3
"""
Hardware Inventory Reporter
============================
Generates a comprehensive hardware inventory report:
CPU, RAM, disk, and network interface information.

Usage:
    python hw_inventory.py
    python hw_inventory.py --output inventory.csv
    python hw_inventory.py --format json
"""

import argparse
import csv
import json
import platform
import socket
import uuid
from datetime import datetime


def get_system_info() -> dict:
    """Collect full system hardware information."""
    info = {
        "hostname": socket.gethostname(),
        "ip_address": socket.gethostbyname(socket.gethostname()),
        "mac_address": ":".join(f"{(uuid.getnode() >> ele) & 0xff:02x}" for ele in range(0, 48, 8)[::-1]),
        "os": platform.system(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
        "timestamp": datetime.now().isoformat(),
    }
    
    try:
        import psutil
        # CPU
        info["cpu_model"] = platform.processor() or "Unknown"
        info["cpu_physical_cores"] = psutil.cpu_count(logical=False)
        info["cpu_logical_cores"] = psutil.cpu_count(logical=True)
        info["cpu_freq_mhz"] = round(psutil.cpu_freq().current, 2) if psutil.cpu_freq() else "N/A"
        info["cpu_usage_percent"] = psutil.cpu_percent(interval=1)
        
        # RAM
        ram = psutil.virtual_memory()
        info["ram_total_gb"] = round(ram.total / (1024**3), 2)
        info["ram_used_gb"] = round(ram.used / (1024**3), 2)
        info["ram_available_gb"] = round(ram.available / (1024**3), 2)
        info["ram_percent_used"] = ram.percent
        
        # Disk
        disks = []
        for partition in psutil.disk_partitions(all=False):
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disks.append({
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "fstype": partition.fstype,
                    "total_gb": round(usage.total / (1024**3), 2),
                    "used_gb": round(usage.used / (1024**3), 2),
                    "free_gb": round(usage.free / (1024**3), 2),
                    "percent_used": usage.percent,
                })
            except PermissionError:
                continue
        info["disks"] = disks
        
        # Network interfaces
        interfaces = []
        for name, addresses in psutil.net_if_addrs().items():
            for addr in addresses:
                if hasattr(addr, "address") and ":" not in addr.address:
                    interfaces.append({
                        "interface": name,
                        "ip": addr.address,
                        "netmask": addr.netmask,
                    })
        info["network_interfaces"] = interfaces
        
    except ImportError:
        info["cpu_model"] = platform.processor() or "Unknown"
        info["note"] = "Install psutil for detailed hardware info: pip install psutil"
    
    return info


def export_csv(info: dict, output_path: str) -> None:
    """Export inventory as CSV (flat fields only)."""
    flat = {k: v for k, v in info.items() if not isinstance(v, list)}
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=flat.keys())
        writer.writeheader()
        writer.writerow(flat)
    print(f"📄 CSV saved: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Hardware Inventory Reporter")
    parser.add_argument("--output", type=str, help="Output file path")
    parser.add_argument("--format", choices=["json", "csv", "text"], default="text",
                        help="Output format (default: text)")
    args = parser.parse_args()
    
    print("🔍 Collecting hardware inventory...")
    info = get_system_info()
    
    if args.format == "json":
        output = json.dumps(info, indent=2)
        if args.output:
            with open(args.output, "w") as f:
                f.write(output)
            print(f"📄 JSON saved: {args.output}")
        else:
            print(output)
    
    elif args.format == "csv":
        path = args.output or f"inventory_{info['hostname']}_{datetime.now().strftime('%Y%m%d')}.csv"
        export_csv(info, path)
    
    else:
        print(f"\n{'='*50}")
        print(f" HARDWARE INVENTORY — {info['hostname']}")
        print(f"{'='*50}")
        print(f"  OS            : {info['os']} {info.get('os_version', '')}")
        print(f"  Architecture  : {info['architecture']}")
        print(f"  IP Address    : {info['ip_address']}")
        print(f"  MAC Address   : {info['mac_address']}")
        print(f"\n  CPU           : {info.get('cpu_model', 'N/A')}")
        print(f"  Cores         : {info.get('cpu_physical_cores', 'N/A')} physical / {info.get('cpu_logical_cores', 'N/A')} logical")
        print(f"  Frequency     : {info.get('cpu_freq_mhz', 'N/A')} MHz")
        print(f"  CPU Usage     : {info.get('cpu_usage_percent', 'N/A')}%")
        print(f"\n  RAM Total     : {info.get('ram_total_gb', 'N/A')} GB")
        print(f"  RAM Used      : {info.get('ram_used_gb', 'N/A')} GB ({info.get('ram_percent_used', 'N/A')}%)")
        
        if info.get("disks"):
            print(f"\n  DISKS:")
            for d in info["disks"]:
                print(f"    {d['device']:20} {d['total_gb']:>8} GB total, {d['free_gb']:>8} GB free ({d['percent_used']}% used)")
        
        if info.get("network_interfaces"):
            print(f"\n  NETWORK INTERFACES:")
            for i in info["network_interfaces"]:
                print(f"    {i['interface']:20} {i['ip']}")
        
        print(f"\n  Generated: {info['timestamp']}")
        
        if args.output:
            export_csv(info, args.output)


if __name__ == "__main__":
    main()
