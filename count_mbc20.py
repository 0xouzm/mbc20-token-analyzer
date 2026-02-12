#!/usr/bin/env python3
import json

# Read new posts
with open('/tmp/moltbook_posts_50.json') as f:
    data = json.load(f)
    posts = data.get('posts', [])

# Count MBC20 operations
mbc20_count = 0
token_counts = {}

for post in posts:
    content = post.get('content', '')
    if '"p":"mbc-20"' in content:
        mbc20_count += 1
        # Try to extract token
        try:
            data = json.loads(content)
            tick = data.get('tick', 'UNKNOWN')
            token_counts[tick] = token_counts.get(tick, 0) + 1
        except:
            pass

print(f'Total MBC20 operations: {mbc20_count}')
print(f'Per token: {token_counts}')
print(f'Total posts checked: {len(posts)}')

# Get top tokens
sorted_tokens = sorted(token_counts.items(), key=lambda x: x[1], reverse=True)[:5]
print(f'Top 5 tokens:')
for token, count in sorted_tokens:
    print(f'  {token}: {count}')
