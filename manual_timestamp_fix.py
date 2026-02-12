#!/usr/bin/env python3

import json
from datetime import datetime, timezone

# Load existing data
with open('moltbook-index.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Update timestamp to current time
data['lastUpdated'] = datetime.now(timezone.utc).isoformat()

# Write updated index
with open('moltbook-index.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Moltbook index timestamp updated to current time!")
print(f"Total posts: {data['stats']['totalPostsIndexed']}")
print(f"Last updated: {data['lastUpdated']}")
