#!/usr/bin/env python3
import json
import subprocess
from datetime import datetime, timezone

# Fetch latest posts
result = subprocess.run(
    ["curl", "-s", "https://www.moltbook.com/api/v1/posts?sort=new&limit=50&offset=0"],
    capture_output=True,
    text=True
)

if result.returncode != 0:
    raise Exception(f"API request failed with code {result.returncode}")

latest_posts_str = result.stdout.strip()
latest_posts = json.loads(latest_posts_str)

# Load existing index
try:
    with open('moltbook-index.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except Exception as e:
    raise Exception(f"Error reading existing file: {e}")

# Get existing agents and submolts
existing_agents = {agent["name"] for agent in data.get("agents", [])}
existing_submolts = {submolt["name"] for submolt in data.get("submolts", [])}

# Process new posts
new_agents = []
new_submolts = set()
new_agent_count = 0

for post in latest_posts.get("posts", []):
    # Extract agent
    author_name = post["author"]["name"]
    desc = post.get("content", "")[:200]
    
    # Check if agent already exists
    if author_name not in existing_agents:
        new_agents.append({
            "name": author_name,
            "description": desc
        })
        new_agent_count += 1
    
    # Extract submolt
    if "submolt" in post:
        submolt_name = post["submolt"]["name"]
        if submolt_name not in existing_submolts:
            new_submolts.add(submolt_name)

# Update stats
stats = data.get("stats", {})
stats["totalPostsIndexed"] = stats.get("totalPostsIndexed", 0) + 50
stats["newAgents"] = stats.get("newAgents", 0) + new_agent_count
stats["submoltsFound"] = stats.get("submoltsFound", 0) + len(new_submolts)

# Update timestamp
now = datetime.now(timezone.utc)
stats["lastUpdated"] = now.isoformat()
stats["lastPostCount"] = 50
stats["nextOffset"] = 50
stats["newSinceLastUpdate"] = 50

# Update data
data["agents"] = existing_agents + new_agents
data["submolts"] = existing_submolts + list(new_submolts)

# Write updated index
try:
    with open('moltbook-index.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Moltbook index updated successfully!")
    print(f"Total posts indexed: {data['stats']['totalPostsIndexed']}")
    print(f"New agents added: {new_agent_count}")
    print(f"Last updated: {data['stats']['lastUpdated']}")
except Exception as e:
    raise Exception(f"Error writing index: {e}")
