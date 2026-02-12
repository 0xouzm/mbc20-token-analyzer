#!/usr/bin/env python3

import json
from datetime import datetime, timezone

# Fetch latest posts from Moltbook
import subprocess
result = subprocess.run([
    'curl', '-s',
    'https://www.moltbook.com/api/v1/posts?sort=new&limit=50'
], capture_output=True, text=True)

response_data = json.loads(result.stdout)

if not response_data.get('success') or 'posts' not in response_data:
    print(f'Error fetching posts: {response_data}')
    exit(1)

posts = response_data['posts']
print(f'Fetched {len(posts)} posts from Moltbook')

# Load current index
with open('moltbook-index.json', 'r', encoding='utf-8') as f:
    index_data = json.load(f)

# Extract new agents
existing_agents = {agent['name']: agent for agent in index_data.get('agents', [])}
seen_in_batch = set()
post_times = {p['created_at'] for p in posts if p.get('created_at')}

for post in posts:
    if post.get('author') and post['author'].get('name'):
        agent_name = post['author']['name']
        if agent_name not in seen_in_batch:
            seen_in_batch.add(agent_name)
            if agent_name not in existing_agents:
                content = post.get('content') or ''
                existing_agents[agent_name] = {
                    'name': agent_name,
                    'description': content[:200],
                    'firstSeen': post.get('created_at', datetime.now(timezone.utc).isoformat())
                }

existing_agents_batch = [a for a in existing_agents.values() if a["name"] in seen_in_batch]
new_agents_batch = [a for a in existing_agents.values() if a["name"] in seen_in_batch and a["firstSeen"] not in post_times]

print(f'Found {len(existing_agents_batch)} existing agents in this batch')
print(f'Found {len(new_agents_batch)} truly new agents')

# Update index
index_data['agents'] = list(existing_agents.values())
index_data['lastUpdated'] = datetime.now(timezone.utc).isoformat()
index_data['lastPostCount'] = response_data.get('count', len(posts))
index_data['nextOffset'] = response_data.get('next_offset', 50)

# Update stats
index_data['stats'] = index_data.get('stats', {})
index_data['stats']['totalPostsIndexed'] = index_data['stats'].get('totalPostsIndexed', 0) + len(posts)
index_data['stats']['newAgents'] = len(existing_agents)
index_data['stats']['newSinceLastUpdate'] = len(posts)

# Extract new submolts
existing_submolts = {s['name']: s for s in index_data.get('submolts', [])}
new_submolts = []

for post in posts:
    if post.get('submolt') and post['submolt'].get('name'):
        submolt_name = post['submolt']['name']
        if submolt_name not in existing_submolts:
            existing_submolts[submolt_name] = {
                'name': post['submolt']['name'],
                'display_name': post['submolt'].get('display_name', post['submolt']['name']),
                'posts': 1
            }
            new_submolts.append(submolt_name)
        else:
            existing_submolts[submolt_name]['posts'] += 1

index_data['submolts'] = list(existing_submolts.values())
index_data['stats']['submoltsFound'] = len(existing_submolts)

# Detect CLAW mints
claw_mints = sum(1 for post in posts if post.get('content') and 'CLAW' in post['content'])
if claw_mints > 0:
    print(f'Detected {claw_mints} CLAW mint posts in this batch')

# Write updated index
with open('moltbook-index.json', 'w', encoding='utf-8') as f:
    json.dump(index_data, f, ensure_ascii=False, indent=2)

print(f'Index updated successfully!')
print(f'Total agents: {len(existing_agents)}')
print(f'Total submolts: {len(existing_submolts)}')
print(f'Total posts indexed: {index_data["stats"]["totalPostsIndexed"]}')
