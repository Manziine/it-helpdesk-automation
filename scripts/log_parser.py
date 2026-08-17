#!/usr/bin/env python3
"""
Log Parser & Error Analyzer
============================
Parses server logs (Nginx, Apache, syslog) and extracts error patterns.

Usage:
    python log_parser.py --file /var/log/nginx/error.log --last 24h
    python log_parser.py --file /var/log/syslog --format json
"""
import argparse, re, json, sys
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

NGINX_ERROR_PATTERN = re.compile(r'(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}) \[(\w+)\] .* (.*)')
SYSLOG_PATTERN = re.compile(r'(\w{3}\s+\d+\s+\d{2}:\d{2}:\d{2}) (\S+) (\S+): (.*)')
IP_PATTERN = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')

def parse_log_file(filepath: str, last_hours: int = 24) -> list[dict]:
    """Parse a log file and return structured error entries."""
    entries = []
    cutoff = datetime.now() - timedelta(hours=last_hours)
    path = Path(filepath)
    if not path.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        return []
    with open(path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line: continue
            ips = IP_PATTERN.findall(line)
            entries.append({"line": line, "ips": ips, "length": len(line)})
    return entries

def analyze(entries: list[dict]) -> dict:
    """Extract patterns, top IPs, and error frequency."""
    all_ips = []
    for e in entries:
        all_ips.extend(e["ips"])
    top_ips = Counter(all_ips).most_common(10)
    keywords = ["error", "crit", "warn", "fail", "denied", "timeout", "refused"]
    keyword_counts = {k: sum(1 for e in entries if k.lower() in e["line"].lower()) for k in keywords}
    return {"total_lines": len(entries), "top_source_ips": top_ips, "keyword_frequency": keyword_counts}

def main():
    parser = argparse.ArgumentParser(description="Server Log Analyzer")
    parser.add_argument("--file", required=True, help="Path to log file")
    parser.add_argument("--last", type=int, default=24, help="Analyze last N hours (default: 24)")
    parser.add_argument("--format", choices=["text","json"], default="text")
    args = parser.parse_args()
    entries = parse_log_file(args.file, args.last)
    if not entries:
        print("No entries found."); return
    stats = analyze(entries)
    if args.format == "json":
        print(json.dumps(stats, indent=2))
    else:
        print(f"\n=== Log Analysis: {args.file} ===")
        print(f"Total lines: {stats['total_lines']}")
        print(f"\nKeyword frequency:")
        for k, v in stats["keyword_frequency"].items():
            if v > 0: print(f"  {k:10} {v:>6} occurrences")
        print(f"\nTop source IPs:")
        for ip, count in stats["top_source_ips"]:
            print(f"  {ip:20} {count:>5} hits")

if __name__ == "__main__":
    main()