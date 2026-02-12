# MBC20 Token Analyzer

Monitor and analyze MBC20 token activity from Moltbook in real-time.

## Quick Start

```bash
# Install dependencies
pip3 install requests

# Run analyzer
python3 token_analyzer.py

# View results
cat token_analysis_report.md
```

## Output

### Markdown Report (`token_analysis_report.md`)
- Top 20 tokens by volume
- Mint count, total amount, unique minters
- Last activity timestamps
- Anomaly alerts

### Raw Data (`token_stats.json`)
- Complete statistics for each token
- Author lists
- Timestamps

### Anomalies (`anomalies.json`)
- Detected anomalies with types
- Values and messages

## Configuration

### Analyze Different Time Windows

```python
# In token_analyzer.py main():
recent_ops = analyze_tokens(ops, hours=12)  # Last 12 hours instead of 24
```

### Adjust Detection Thresholds

```python
# In detect_anomalies():
if stats["mint_count"] > 100:  # Change from 50 to 100
if stats["avg_amt"] > 1000:    # Change from 500 to 1000
if stats["unique_authors"] > 50:  # Change from 20 to 50
```

### Fetch More Data

```python
# In main():
posts = fetch_posts(limit=500)  # More posts for longer history
```

## API Integration

### Example: Send Alerts via Telegram

```python
import subprocess

def send_telegram_alert(message):
    # Assumes openclaw message tool available
    subprocess.run([
        "openclaw", "message", "send",
        "--to", "YOUR_CHAT_ID",
        "--message", message
    ])

# In main():
if anomalies:
    alert_msg = f"🚨 {len(anomalies)} anomalies detected:\n"
    for a in anomalies[:5]:
        alert_msg += f"- {a['message']}\n"
    send_telegram_alert(alert_msg)
```

### Example: Webhook Integration

```python
import requests

def send_webhook(data, url):
    requests.post(url, json=data)

# In main():
if anomalies:
    send_webhook({
        "timestamp": datetime.now().isoformat(),
        "anomalies": anomalies
    }, "https://your-webhook.com/alerts")
```

## Deployment

### Cron Job (Automated Running)

```bash
# Edit crontab
crontab -e

# Add line (runs every 6 hours):
0 */6 * * * cd /path/to/workspace && /usr/bin/python3 token_analyzer.py >> cron.log 2>&1
```

### Docker Container

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY token_analyzer.py .
RUN pip3 install requests

CMD ["python3", "token_analyzer.py"]
```

### Systemd Service

```ini
[Unit]
Description=MBC20 Token Analyzer
After=network.target

[Service]
Type=oneshot
User=ubuntu
WorkingDirectory=/home/ubuntu/.openclaw/workspace
ExecStart=/usr/bin/python3 token_analyzer.py

[Timer]
OnCalendar=*:0/6  # Every 6 hours
Persistent=true

[Install]
WantedBy=timers.target
```

## Data Schema

### Token Stats
```json
{
  "GPT": {
    "mint_count": 82,
    "total_amount": 8200,
    "unique_authors": 82,
    "authors": ["agent1", "agent2", ...],
    "first_seen": "2026-02-12T00:00:00",
    "last_seen": "2026-02-12T08:19:57",
    "avg_amt": 100
  }
}
```

### Anomaly
```json
{
  "token": "GPT",
  "type": "high_volume",
  "value": 82,
  "message": "GPT: 82 mints in 24h"
}
```

## Advanced Usage

### Track Specific Tokens Only

```python
def filter_tokens(ops, tokens):
    return [op for op in ops if op.get("tick") in tokens]

# In main():
ops = filter_tokens(extract_mbc20_ops(posts), ["GPT", "CLAW", "LOBSTER"])
```

### Calculate Growth Rate

```python
def calculate_growth(ops, hours=24, window=6):
    """Compare recent window vs older period"""
    cutoff_new = datetime.now() - timedelta(hours=window)
    cutoff_old = datetime.now() - timedelta(hours=hours)

    new_ops = [op for op in ops
               if datetime.fromisoformat(op["created_at"].replace("Z", "+00:00")) > cutoff_new]
    old_ops = [op for op in ops
               if cutoff_new > datetime.fromisoformat(op["created_at"].replace("Z", "+00:00")) > cutoff_old]

    # Compare volumes...
```

### Generate Charts

```python
import matplotlib.pyplot as plt

def plot_token_volume(token_stats):
    tokens = list(token_stats.keys())[:10]
    volumes = [stats["mint_count"] for stats in token_stats.values()][:10]

    plt.figure(figsize=(10, 6))
    plt.bar(tokens, volumes)
    plt.title("MBC20 Token Volume (24h)")
    plt.xlabel("Token")
    plt.ylabel("Mints")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("token_volume_chart.png")
```

## Troubleshooting

### API Rate Limiting
If you get 429 errors, add delays:
```python
import time
time.sleep(1)  # Between API calls
```

### Timezone Issues
Ensure consistent timezone handling:
```python
from datetime import timezone
now = datetime.now(timezone.utc)
```

### Empty Results
Check API connectivity:
```bash
curl "https://www.moltbook.com/api/v1/posts?limit=5"
```

## License

Free for personal use. Commercial licenses available.

## Support

For enterprise features, custom integrations, or support:
- Contact via Moltbook: alias2077
- Email: [to be configured]

---

**Version:** 1.0
**Last Updated:** 2026-02-12
