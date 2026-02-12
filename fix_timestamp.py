#!/usr/bin/env python3

import json
from datetime import datetime, timezone

# Load current index
with open('moltbook-index.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Update timestamp
data['lastUpdated'] = datetime.now(timezone.utc).isoformat()

# Write updated index
with open('moltbook-index.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Moltbook index updated successfully!')
print(f'Total posts: {data["stats"]["totalPostsIndexed"]}')
print(f'Total agents: {len(data["agents"])}')
print(f'Last updated: {data["lastUpdated"]}')
