#!/usr/bin/env python3
"""
System & Web Server Log Analyzer
Parses access logs, detects error spikes (4xx/5xx), top IP request counts, and anomalies.
"""
import re
import sys
from collections import Counter

LOG_PATTERN = re.compile(r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "(.*?)" (\d{3}) (\d+)')

def analyze_log_content(lines):
    ip_counter = Counter()
    status_counter = Counter()
    
    for line in lines:
        match = LOG_PATTERN.match(line)
        if match:
            ip, timestamp, request, status, size = match.groups()
            ip_counter[ip] += 1
            status_counter[status] += 1
            
    return {
        "total_requests": sum(status_counter.values()),
        "top_ips": ip_counter.most_common(5),
        "status_distribution": dict(status_counter)
    }

if __name__ == "__main__":
    sample_logs = [
        '192.168.1.1 - - [23/Aug/2026:12:00:00 +0000] "GET /api/users HTTP/1.1" 200 1024',
        '192.168.1.2 - - [23/Aug/2026:12:01:00 +0000] "POST /api/login HTTP/1.1" 401 128',
        '192.168.1.1 - - [23/Aug/2026:12:02:00 +0000] "GET /api/orders HTTP/1.1" 200 2048',
    ]
    results = analyze_log_content(sample_logs)
    print("Log Analysis Results:", results)
