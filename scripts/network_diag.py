#!/usr/bin/env python3
"""
Network Diagnostics Tool
========================
Comprehensive network health checker: ping sweep, port scan,
DNS resolution, and latency reporting.

Usage:
    python network_diag.py --subnet 192.168.1.0/24
    python network_diag.py --host google.com --ports 80,443
    python network_diag.py --subnet 10.0.0.0/24 --ports 22,80,443 --output report.html
"""

import argparse
import ipaddress
import json
import socket
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Optional


def ping_host(host: str, count: int = 3) -> dict:
    """Ping a host and return latency statistics."""
    param = "-n" if sys.platform == "win32" else "-c"
    try:
        start = time.time()
        result = subprocess.run(
            ["ping", param, str(count), "-W", "1", str(host)],
            capture_output=True, text=True, timeout=10
        )
        duration = time.time() - start
        is_alive = result.returncode == 0
        return {
            "host": str(host),
            "alive": is_alive,
            "avg_ms": round((duration / count) * 1000, 2) if is_alive else None,
        }
    except (subprocess.TimeoutExpired, Exception):
        return {"host": str(host), "alive": False, "avg_ms": None}


def check_port(host: str, port: int, timeout: float = 1.0) -> dict:
    """Check if a TCP port is open."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return {"port": port, "open": True}
    except (socket.timeout, ConnectionRefusedError, OSError):
        return {"port": port, "open": False}


def resolve_dns(hostname: str) -> Optional[str]:
    """Resolve hostname to IP address."""
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None


def scan_subnet(subnet: str, ports: list[int], max_workers: int = 50) -> list[dict]:
    """Scan all hosts in a subnet."""
    network = ipaddress.ip_network(subnet, strict=False)
    hosts = list(network.hosts())
    
    print(f"🌐 Scanning {len(hosts)} hosts in {subnet}...")
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        ping_futures = {executor.submit(ping_host, str(h)): str(h) for h in hosts}
        
        for future in as_completed(ping_futures):
            ping_result = future.result()
            if ping_result["alive"] and ports:
                # Scan ports on alive hosts
                port_results = []
                for port in ports:
                    port_results.append(check_port(ping_result["host"], port))
                ping_result["ports"] = port_results
            results.append(ping_result)
    
    return sorted(results, key=lambda x: x["host"])


def generate_html_report(results: list[dict], output_path: str) -> None:
    """Generate an HTML network scan report."""
    alive = [r for r in results if r.get("alive")]
    
    rows = ""
    for r in results:
        status = "🟢 Online" if r["alive"] else "🔴 Offline"
        latency = f"{r['avg_ms']} ms" if r.get("avg_ms") else "—"
        
        port_info = ""
        if r.get("ports"):
            port_info = " ".join(
                f"<span style='color:{'green' if p['open'] else 'red'}'>{p['port']}</span>"
                for p in r["ports"]
            )
        
        rows += f"<tr><td>{r['host']}</td><td>{status}</td><td>{latency}</td><td>{port_info or '—'}</td></tr>"
    
    html = f"""<!DOCTYPE html>
<html><head><title>Network Scan Report</title>
<style>body{{font-family:Arial;padding:20px}} table{{border-collapse:collapse;width:100%}}
th,td{{border:1px solid #ddd;padding:8px;text-align:left}} th{{background:#333;color:white}}</style>
</head><body>
<h1>🌐 Network Diagnostics Report</h1>
<p>Generated: {datetime.now().isoformat()} | Total hosts: {len(results)} | Online: {len(alive)}</p>
<table><tr><th>Host</th><th>Status</th><th>Avg Latency</th><th>Open Ports</th></tr>
{rows}</table></body></html>"""
    
    with open(output_path, "w") as f:
        f.write(html)
    print(f"📄 HTML report saved: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Network Diagnostics Tool")
    parser.add_argument("--subnet", type=str, help="Subnet to scan (e.g. 192.168.1.0/24)")
    parser.add_argument("--host", type=str, help="Single host to check")
    parser.add_argument("--ports", type=str, default="",
                        help="Comma-separated ports to check (e.g. 22,80,443)")
    parser.add_argument("--output", type=str, help="Output HTML report path")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    
    ports = [int(p) for p in args.ports.split(",") if p.strip()] if args.ports else []
    
    if args.host:
        print(f"🔍 Checking host: {args.host}")
        ip = resolve_dns(args.host)
        if ip:
            print(f"   DNS resolved: {args.host} → {ip}")
        result = ping_host(args.host)
        if ports:
            result["ports"] = [check_port(args.host, p) for p in ports]
        results = [result]
    elif args.subnet:
        results = scan_subnet(args.subnet, ports)
    else:
        parser.print_help()
        return
    
    # Output
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        alive = [r for r in results if r.get("alive")]
        print(f"\n📊 Results: {len(alive)}/{len(results)} hosts online")
        for r in alive:
            latency = f"{r['avg_ms']}ms" if r.get("avg_ms") else ""
            open_ports = [p["port"] for p in r.get("ports", []) if p["open"]]
            port_str = f"| Ports: {open_ports}" if open_ports else ""
            print(f"  ✅ {r['host']:20} {latency:10} {port_str}")
    
    if args.output:
        generate_html_report(results, args.output)


if __name__ == "__main__":
    main()
