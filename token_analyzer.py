#!/usr/bin/env python3
"""
Moltbook Token Analyzer
Analyzes MBC20 token activity from Moltbook posts
"""

import json
import requests
from collections import defaultdict, Counter
from datetime import datetime, timedelta
import re

MOLTBOOK_API = "https://www.moltbook.com/api/v1"

def fetch_posts(limit=100, offset=0):
    """Fetch recent posts from Moltbook"""
    response = requests.get(
        f"{MOLTBOOK_API}/posts",
        params={"limit": limit, "sort": "new", "offset": offset}
    )
    response.raise_for_status()
    return response.json().get("posts", [])

def extract_mbc20_ops(posts):
    """Extract MBC20 operations from posts"""
    ops = []

    for post in posts:
        content = post.get("content", "")
        try:
            # Try to parse as JSON
            data = json.loads(content)
            if data.get("p") == "mbc-20":
                ops.append({
                    "author": post.get("author", {}).get("name"),
                    "op": data.get("op"),
                    "tick": data.get("tick"),
                    "amt": data.get("amt"),
                    "created_at": post.get("created_at"),
                    "post_id": post.get("id")
                })
        except:
            # Try to parse from plain text
            mint_pattern = r'{"p":"mbc-20","op":"mint","tick":"(\w+)","amt":"(\d+)"}'
            match = re.search(mint_pattern, content)
            if match:
                ops.append({
                    "author": post.get("author", {}).get("name"),
                    "op": "mint",
                    "tick": match.group(1),
                    "amt": match.group(2),
                    "created_at": post.get("created_at"),
                    "post_id": post.get("id")
                })

    return ops

def analyze_tokens(ops, hours=24):
    """Analyze token activity"""
    # Filter by time (make both offset-aware)
    cutoff = datetime.now().replace(tzinfo=None) - timedelta(hours=hours)
    recent_ops = [op for op in ops if datetime.fromisoformat(op["created_at"].replace("Z", "+00:00")).replace(tzinfo=None) > cutoff]

    return recent_ops

def compute_token_stats(ops):
    """Compute statistics for tokens"""
    token_stats = defaultdict(lambda: {
        "mint_count": 0,
        "total_amount": 0,
        "unique_authors": set(),
        "authors": [],
        "first_seen": None,
        "last_seen": None,
        "avg_amt": 0
    })

    for op in ops:
        if op["op"] == "mint":
            tick = op["tick"]
            token_stats[tick]["mint_count"] += 1
            token_stats[tick]["unique_authors"].add(op["author"])
            token_stats[tick]["authors"].append(op["author"])
            try:
                amt = int(op["amt"])
                token_stats[tick]["total_amount"] += amt
            except:
                pass

            ts = datetime.fromisoformat(op["created_at"].replace("Z", "+00:00")).replace(tzinfo=None)
            if token_stats[tick]["first_seen"] is None or ts < token_stats[tick]["first_seen"]:
                token_stats[tick]["first_seen"] = ts
            if token_stats[tick]["last_seen"] is None or ts > token_stats[tick]["last_seen"]:
                token_stats[tick]["last_seen"] = ts

    # Convert sets to counts and compute averages
    for tick, stats in token_stats.items():
        stats["unique_authors"] = len(stats["unique_authors"])
        if stats["mint_count"] > 0:
            stats["avg_amt"] = stats["total_amount"] // stats["mint_count"]

    return token_stats

def detect_anomalies(token_stats):
    """Detect anomalous activity (sudden spikes)"""
    anomalies = []

    for tick, stats in token_stats.items():
        # High mint count
        if stats["mint_count"] > 50:
            anomalies.append({
                "token": tick,
                "type": "high_volume",
                "value": stats["mint_count"],
                "message": f"{tick}: {stats['mint_count']} mints in 24h"
            })

        # Large batch operations
        if stats["avg_amt"] > 500:
            anomalies.append({
                "token": tick,
                "type": "large_batches",
                "value": stats["avg_amt"],
                "message": f"{tick}: avg {stats['avg_amt']} per mint"
            })

        # Multiple authors (botnet?)
        if stats["unique_authors"] > 20:
            anomalies.append({
                "token": tick,
                "type": "multi_author",
                "value": stats["unique_authors"],
                "message": f"{tick}: {stats['unique_authors']} unique minters"
            })

    return anomalies

    # Count by token
    token_stats = defaultdict(lambda: {
        "mint_count": 0,
        "total_amount": 0,
        "unique_authors": set(),
        "authors": [],
        "first_seen": None,
        "last_seen": None
    })

    for op in recent_ops:
        if op["op"] == "mint":
            tick = op["tick"]
            token_stats[tick]["mint_count"] += 1
            token_stats[tick]["unique_authors"].add(op["author"])
            token_stats[tick]["authors"].append(op["author"])
            try:
                token_stats[tick]["total_amount"] += int(op["amt"])
            except:
                pass

            ts = datetime.fromisoformat(op["created_at"].replace("Z", "+00:00"))
            if token_stats[tick]["first_seen"] is None or ts < token_stats[tick]["first_seen"]:
                token_stats[tick]["first_seen"] = ts
            if token_stats[tick]["last_seen"] is None or ts > token_stats[tick]["last_seen"]:
                token_stats[tick]["last_seen"] = ts

    # Convert sets to counts
    for tick, stats in token_stats.items():
        stats["unique_authors"] = len(stats["unique_authors"])

    return token_stats

def generate_report(token_stats):
    """Generate analysis report"""
    # Sort by mint count
    sorted_tokens = sorted(token_stats.items(), key=lambda x: x[1]["mint_count"], reverse=True)

    report = "# MBC20 Token Analysis Report\n\n"
    report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n"
    report += "## Top Tokens by Activity\n\n"

    for i, (tick, stats) in enumerate(sorted_tokens[:20], 1):
        report += f"### {i}. {tick}\n"
        report += f"- Mint count: {stats['mint_count']}\n"
        report += f"- Total amount: {stats['total_amount']:,}\n"
        report += f"- Unique minters: {stats['unique_authors']}\n"
        if stats['last_seen']:
            report += f"- Last activity: {stats['last_seen'].strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
        report += "\n"

    return report

def main():
    print("Fetching Moltbook posts...")
    posts = fetch_posts(limit=200)
    print(f"Fetched {len(posts)} posts")

    print("Extracting MBC20 operations...")
    ops = extract_mbc20_ops(posts)
    print(f"Found {len(ops)} MBC20 operations")

    print("Analyzing token activity...")
    recent_ops = analyze_tokens(ops, hours=24)
    token_stats = compute_token_stats(recent_ops)
    print(f"Found {len(token_stats)} unique tokens")

    print("Detecting anomalies...")
    anomalies = detect_anomalies(token_stats)
    print(f"Found {len(anomalies)} anomalies")

    report = generate_report(token_stats)

    # Add anomalies section
    if anomalies:
        report += "\n## 🚨 Anomalies Detected\n\n"
        for a in anomalies[:10]:
            report += f"- **{a['type']}**: {a['message']}\n"

    # Save report
    report_path = "token_analysis_report.md"
    with open(report_path, "w") as f:
        f.write(report)

    print(f"\nReport saved to {report_path}")
    print("\n" + report)

    # Save raw data
    with open("token_stats.json", "w") as f:
        json.dump(dict(token_stats), f, indent=2, default=str)
    print("Raw stats saved to token_stats.json")

    # Save anomalies
    with open("anomalies.json", "w") as f:
        json.dump(anomalies, f, indent=2)
    print("Anomalies saved to anomalies.json")

if __name__ == "__main__":
    main()
