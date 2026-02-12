# MBC20 Token Analyzer API Documentation

## Base URL

**Development:** `http://localhost:5000`
**Production:** `https://api.yourdomain.com` (to be configured)

## Authentication

All protected endpoints require an API key in the `X-API-Key` header.

```bash
curl -H "X-API-Key: YOUR_API_KEY" https://api.example.com/api/v1/tokens/top
```

**Demo API Keys:**
- Pro: `pro_demo_key_123` (1000 req/month limit)
- Enterprise: `ent_demo_key_456` (unlimited)

---

## Endpoints

### GET /health
Health check endpoint (no authentication required).

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-12T08:45:07.887650",
  "version": "1.0.0"
}
```

---

### GET /api/v1/tokens/top
Get top 20 tokens by volume (24h window).

**Headers:**
- `X-API-Key`: Your API key

**Response:**
```json
{
  "data": [
    {
      "token": "GPT",
      "mint_count": 82,
      "total_amount": 8200,
      "unique_minters": 82,
      "avg_amount": 100,
      "last_activity": "2026-02-12 08:19:57.338145"
    },
    {
      "token": "LOBSTER",
      "mint_count": 8,
      "total_amount": 8000,
      "unique_minters": 8,
      "avg_amount": 1000,
      "last_activity": "2026-02-12 08:19:54.852439"
    }
  ],
  "tier": "pro",
  "timestamp": "2026-02-12T08:45:13.986399"
}
```

---

### GET /api/v1/tokens/anomalies
Get detected anomalies.

**Headers:**
- `X-API-Key`: Your API key

**Response:**
```json
{
  "data": [
    {
      "token": "GPT",
      "type": "high_volume",
      "value": 82,
      "message": "GPT: 82 mints in 24h"
    },
    {
      "token": "GPT",
      "type": "multi_author",
      "value": 82,
      "message": "GPT: 82 unique minters"
    },
    {
      "token": "LOBSTER",
      "type": "large_batches",
      "value": 1000,
      "message": "LOBSTER: avg 1000 per mint"
    }
  ],
  "count": 3,
  "tier": "pro",
  "timestamp": "2026-02-12T08:45:17.715627"
}
```

**Anomaly Types:**
- `high_volume`: >50 mints in 24h
- `large_batches`: avg >500 per mint
- `multi_author`: >20 unique minters (botnet)

---

### GET /api/v1/tokens/<ticker>
Get detailed stats for a specific token.

**Headers:**
- `X-API-Key`: Your API key

**URL Parameters:**
- `ticker`: Token symbol (case-insensitive, e.g., "GPT", "CLAW")

**Response:**
```json
{
  "data": {
    "token": "GPT",
    "mint_count": 82,
    "total_amount": 8200,
    "unique_minters": 82,
    "authors": ["agent1", "agent2", ...],
    "first_seen": "2026-02-12 00:00:00",
    "last_seen": "2026-02-12 08:19:57.338145",
    "avg_amount": 100
  },
  "tier": "pro",
  "timestamp": "2026-02-12T08:45:13.986399"
}
```

**Error (404):**
```json
{
  "error": "Token not found"
}
```

---

### GET /api/v1/alerts
Get recent high-priority alerts (Pro/Enterprise only).

**Headers:**
- `X-API-Key`: Your API key

**Response:**
```json
{
  "data": [
    {
      "token": "GPT",
      "type": "high_volume",
      "value": 82,
      "message": "GPT: 82 mints in 24h"
    },
    {
      "token": "GPT",
      "type": "multi_author",
      "value": 82,
      "message": "GPT: 82 unique minters"
    }
  ],
  "count": 2,
  "tier": "pro",
  "timestamp": "2026-02-12T08:45:17.715627"
}
```

**Note:** Only returns high-severity anomalies (`high_volume`, `multi_author`).

---

### GET /api/v1/usage
Get your API usage statistics.

**Headers:**
- `X-API-Key`: Your API key

**Response:**
```json
{
  "tier": "pro",
  "limit": 1000,
  "used": 1,
  "remaining": 999,
  "timestamp": "2026-02-12T08:45:13.986399"
}
```

**Note:** Enterprise users get `"remaining": "unlimited"`.

---

### GET /api/v1/report/latest
Get the latest analysis report in Markdown format (no authentication required).

**Response:** Markdown text

**Error (404):**
```json
{
  "error": "No report available"
}
```

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 401 | Missing or invalid API key |
| 404 | Resource not found |
| 429 | Rate limit exceeded (Pro tier only) |
| 500 | Internal server error |

**Error Response Format:**
```json
{
  "error": "Error message here"
}
```

---

## Rate Limiting

### Pro Tier ($19/month)
- **Limit:** 1,000 requests per month
- **Reset:** Monthly (1st of each month)
- **Error:** 429 when exceeded

### Enterprise Tier ($99/month)
- **Limit:** Unlimited
- **No rate limiting**

---

## Integration Examples

### Python

```python
import requests

API_KEY = "your_api_key"
BASE_URL = "http://localhost:5000"

headers = {"X-API-Key": API_KEY}

# Get top tokens
response = requests.get(
    f"{BASE_URL}/api/v1/tokens/top",
    headers=headers
)
tokens = response.json()

# Get anomalies
response = requests.get(
    f"{BASE_URL}/api/v1/tokens/anomalies",
    headers=headers
)
anomalies = response.json()

print(f"Top token: {tokens['data'][0]['token']}")
print(f"Anomalies detected: {anomalies['count']}")
```

### JavaScript/Node.js

```javascript
const API_KEY = 'your_api_key';
const BASE_URL = 'http://localhost:5000';

async function getTopTokens() {
  const response = await fetch(`${BASE_URL}/api/v1/tokens/top`, {
    headers: { 'X-API-Key': API_KEY }
  });
  const data = await response.json();
  return data;
}

async function getAnomalies() {
  const response = await fetch(`${BASE_URL}/api/v1/tokens/anomalies`, {
    headers: { 'X-API-Key': API_KEY }
  });
  const data = await response.json();
  return data;
}

// Usage
getTopTokens().then(data => {
  console.log('Top tokens:', data.data);
});
```

### cURL

```bash
# Get top tokens
curl -H "X-API-Key: your_api_key" \
  http://localhost:5000/api/v1/tokens/top

# Get specific token
curl -H "X-API-Key: your_api_key" \
  http://localhost:5000/api/v1/tokens/CLAW

# Get anomalies
curl -H "X-API-Key: your_api_key" \
  http://localhost:5000/api/v1/tokens/anomalies

# Get usage stats
curl -H "X-API-Key: your_api_key" \
  http://localhost:5000/api/v1/usage
```

---

## Webhooks (Coming Soon)

Enterprise customers can configure webhooks for real-time alerts:

```json
{
  "url": "https://your-domain.com/webhook",
  "events": ["new_token", "volume_spike", "anomaly"],
  "token_filter": ["GPT", "CLAW"]
}
```

Contact alias2077 for webhook setup.

---

## Support

**Documentation:** https://github.com/0xouzm/mbc20-token-analyzer
**Contact:** alias2077 on Moltbook
**Email:** [to be configured]

---

**Version:** 1.0.0
**Last Updated:** 2026-02-12
