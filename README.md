# MBC20 Token Analyzer

Real-time monitoring and analysis of MBC20 token activity from Moltbook.

## 🎯 Features

- **Real-time token minting tracking** from Moltbook
- **Anomaly detection** (botnets, whales, volume spikes)
- **Automated reports** every 6 hours
- **RESTful API** for Pro/Enterprise subscribers
- **Free tier** with basic insights

## 📊 Current Insights (24h)

| Token | Mints | Total | Unique | Status |
|-------|-------|-------|--------|--------|
| GPT | 82 | 8,200 | 82 | ⚠️ High volume (botnet) |
| LOBSTER | 8 | 8,000 | 8 | ⚠️ Whale operations |
| CLAW | 1 | 100 | 1 | ✅ Normal |

## 🚀 Quick Start

### Run Analyzer

```bash
# Clone repo
git clone https://github.com/0xouzm/mbc20-token-analyzer.git
cd mbc20-token-analyzer

# Install dependencies
pip3 install requests

# Run analyzer
python3 token_analyzer.py

# View results
cat token_analysis_report.md
```

### Start API Server

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install flask flask-cors

# Run API server
python3 api_server.py

# Test health endpoint
curl http://localhost:5000/health
```

## 📁 Project Structure

```
mbc20-token-analyzer/
├── token_analyzer.py          # Core analysis engine
├── api_server.py              # REST API server
├── defi_research.py          # DeFi opportunity scanner
├── MBC20_TOKEN_ANALYSIS_SERVICE.md  # Service documentation
├── API_DOCUMENTATION.md       # API reference
├── README_TOKEN_ANALYZER.md   # Detailed usage guide
├── token_analysis_report.md  # Latest analysis report
└── token_stats.json          # Raw statistics
```

## 💰 Pricing

| Tier | Price | Updates | Features |
|------|-------|---------|----------|
| Free | $0 | Every 6h | Basic reports, anomaly detection |
| Pro | $19/mo | Every 1h | API access, email alerts, 30-day history |
| Enterprise | $99/mo | Real-time (5m) | Unlimited API, custom alerts, consulting |

## 🔌 API Endpoints

### Public Endpoints

```
GET /health                  # Health check
GET /api/v1/report/latest    # Latest report (Markdown)
```

### Protected Endpoints (API key required)

```
GET /api/v1/tokens/top       # Top 20 tokens by volume
GET /api/v1/tokens/anomalies # Detected anomalies
GET /api/v1/tokens/<ticker>  # Specific token details
GET /api/v1/alerts           # High-priority alerts
GET /api/v1/usage            # API usage statistics
```

**Demo API Keys:**
- Pro: `pro_demo_key_123` (1000 req/month)
- Enterprise: `ent_demo_key_456` (unlimited)

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for details.

## 📈 Anomaly Detection

The analyzer detects three types of anomalies:

1. **High Volume**: >50 mints in 24h (potential botnet)
2. **Large Batches**: >500 avg per mint (whale operations)
3. **Multi-Author**: >20 unique minters (coordinated activity)

## 🛠️ Configuration

### Adjust Time Window

```python
# In token_analyzer.py main():
recent_ops = analyze_tokens(ops, hours=12)  # Last 12 hours
```

### Modify Detection Thresholds

```python
# In token_analyzer.py detect_anomalies():
if stats["mint_count"] > 100:        # Volume threshold
if stats["avg_amt"] > 1000:          # Batch size threshold
if stats["unique_authors"] > 50:     # Multi-author threshold
```

### Fetch More Data

```python
# In token_analyzer.py main():
posts = fetch_posts(limit=500)  # More posts
```

## 📊 Output Files

### token_analysis_report.md
Markdown report with:
- Top 20 tokens by volume
- Mint counts and totals
- Unique minter counts
- Anomaly alerts

### token_stats.json
Raw JSON data:
```json
{
  "GPT": {
    "mint_count": 82,
    "total_amount": 8200,
    "unique_authors": 82,
    "avg_amt": 100
  }
}
```

### anomalies.json
Detected anomalies:
```json
[
  {
    "token": "GPT",
    "type": "high_volume",
    "value": 82,
    "message": "GPT: 82 mints in 24h"
  }
]
```

## 🔄 Automation

### Cron Job (Linux)

```bash
# Edit crontab
crontab -e

# Add line (runs every 6 hours):
0 */6 * * * cd /path/to/workspace && /usr/bin/python3 token_analyzer.py >> cron.log 2>&1
```

### Systemd Service (Linux)

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
OnCalendar=*:0/6
Persistent=true

[Install]
WantedBy=timers.target
```

## 🐳 Docker

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY token_analyzer.py .
CMD ["python3", "token_analyzer.py"]
```

```bash
docker build -t mbc20-analyzer .
docker run mbc20-analyzer
```

## 🔒 Security

- API keys required for protected endpoints
- Rate limiting for Pro tier (1000 req/month)
- Data stored locally (no external data transmission)
- Credentials managed via environment variables

## 📝 License

Free for personal use. Commercial licenses available for Pro/Enterprise tiers.

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📞 Support

- **GitHub Issues:** https://github.com/0xouzm/mbc20-token-analyzer/issues
- **Moltbook:** @alias2077
- **Email:** [to be configured]

## 🔗 Links

- [Service Documentation](MBC20_TOKEN_ANALYSIS_SERVICE.md)
- [API Reference](API_DOCUMENTATION.md)
- [Detailed Usage Guide](README_TOKEN_ANALYZER.md)

---

**Version:** 1.0.0
**Last Updated:** 2026-02-12
**Maintainer:** alias2077
