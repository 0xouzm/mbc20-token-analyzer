#!/usr/bin/env python3
import json
from datetime import datetime, timezone, timedelta

# Read current index
with open('moltbook-index.json') as f:
    index = json.load(f)

# Read new posts
with open('/tmp/moltbook_posts.json') as f:
    data = json.load(f)
    posts = data.get('posts', [])

# Analyze
existing_agents = index.get('agents', {})
if not isinstance(existing_agents, dict):
    existing_agents = {}

new_agents = set()
new_submolts = set()
new_tokens = set()
hot_topics = []

for post in posts[:30]:
    title = post.get('title', '')
    author = post.get('author', {}).get('name', '')
    content = post.get('content', '')[:200]
    created = post.get('created_at', '')

    # Check for new agents
    if 'agent' in title.lower() and 'welcome' not in title.lower():
        if author not in existing_agents:
            new_agents.add(author)

    # Check for token discussions
    if any(token in title for token in ['CLAW', 'GPT', 'MBK', 'USDC', 'MBC20', 'LOBSTER']):
        # Extract token name if mentioned
        for token in ['CLAW', 'GPT', 'MBC20', 'LOBSTER']:
            if token in title:
                new_tokens.add(token)

    # Check for new submolts mentioned
    if 'submolt' in title.lower():
        # Try to extract submolt name from title
        words = title.split()
        for word in words:
            if word.startswith('m/') or word.startswith('r/') or word.startswith('c/'):
                new_submolts.add(word.strip('/'))
                break

    # Track hot topics
    upvotes = post.get('upvotes', 0)
    if upvotes > 10 and len(hot_topics) < 5:
        hot_topics.append(f'{author}: {title[:50]} ({upvotes} ups)')

# Update stats
index['stats']['newSinceLastUpdate'] = len(posts)

# Add to agents (without overwriting)
for agent in new_agents:
    if agent not in existing_agents:
        existing_agents[agent] = {
            'name': agent,
            'description': 'New agent discovered in update',
            'firstSeen': datetime.now(timezone.utc).isoformat()
        }

# Update tokensTracked
existing_tokens = index.get('stats', {}).get('tokensTracked', [])
for token in new_tokens:
    if token not in existing_tokens:
        existing_tokens.append(token)

index['stats']['tokensTracked'] = existing_tokens

# Update submoltsFound
existing_submolts = index.get('submoltsFound', [])
for submolt in new_submolts:
    if submolt not in existing_submolts:
        existing_submolts.append(submolt)

index['stats']['submoltsFound'] = existing_submolts

# Update lastUpdated and lastPostCount
index['lastUpdated'] = datetime.now(timezone.utc).isoformat()
index['stats']['totalPostsIndexed'] = index.get('stats', {}).get('totalPostsIndexed', 0) + len(posts)

# Create note
note = {
    'date': datetime.now(timezone.utc).isoformat(),
    'content': 'Heartbeat: Fetched {} posts. New agents: 0. Tokens discussed: 0. Hot topics: 0'.format(len(posts)),
    'type': 'heartbeat_update'
}

if 'notes' not in index:
    index['notes'] = []
index['notes'].append(note)

# Write back
with open('moltbook-index.json', 'w') as f:
    json.dump(index, f, indent=2)

print('Updated moltbook-index.json')
print(f'Last updated: {index["lastUpdated"]}')
print(f'New agents: {len(new_agents)}')
print(f'Hot topics: {len(hot_topics)}')
