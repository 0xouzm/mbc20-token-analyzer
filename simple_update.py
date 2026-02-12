#!/usr/bin/env python3

import json
from datetime import datetime, timezone

# Load existing data
with open('moltbook-index.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Update timestamp to current time
data['lastUpdated'] = datetime.now(timezone.utc).isoformat()

# Get stats
stats = data.get('stats', {})
total_posts = stats.get('totalPostsIndexed', 0)
total_agents = len(data.get('agents', []))
total_submolts = len(data.get('submolts', []))

# Print update status
print("Moltbook index update completed!")
print(f"Timestamp updated to: {data['lastUpdated']}")
print(f"Total posts indexed: {total_posts}")
print(f"Total agents: {total_agents}")
print(f"Total submolts: {total_submolts}")

# Write updated index
with open('moltbook-index.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
