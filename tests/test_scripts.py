import pytest
from scripts.log_analyzer import analyze_log_content

def test_log_analyzer():
    logs = [
        '10.0.0.1 - - [23/Aug/2026:12:00:00 +0000] "GET /health HTTP/1.1" 200 50',
        '10.0.0.1 - - [23/Aug/2026:12:00:01 +0000] "GET /api HTTP/1.1" 500 200',
    ]
    res = analyze_log_content(logs)
    assert res["total_requests"] == 2
    assert res["status_distribution"]["200"] == 1
    assert res["status_distribution"]["500"] == 1
