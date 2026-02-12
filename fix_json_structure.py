#!/usr/bin/env python3

import json

# Read the file as raw text first to inspect the structure
with open('/home/ubuntu/.openclaw/workspace/moltbook-index.json', 'r') as f:
    raw_content = f.read()

# Find the problematic area around line 131 (character 20959)
# The issue seems to be in the hotTopics array - missing a comma

# Simple fix: look for the pattern and add missing commas
fixed_content = raw_content.replace('", "topic": "', '", "topic": "[')
fixed_content = fixed_content.replace("u\"}  \n  ]", '", "u\"}  \n  ]")

# Write the fixed content back
with open('/home/ubuntu/.openclaw/workspace/moltbook-index.json', 'w') as f:
    f.write(fixed_content)

print("Fixed JSON structure in moltbook-index.json")
