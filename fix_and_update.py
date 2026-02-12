#!/usr/bin/env python3

import json

# Read file as raw text
with open('/home/ubuntu/.openclaw/workspace/moltbook-index.json', 'r') as f:
    raw_content = f.read()

# Simple fix: look for the specific pattern and add missing comma
# The error was around line 131, column 94 in the "hotTopics" array
# Pattern: "topic": "uwu_culture_recruitment" (last element before notableContent)

fixed_content = raw_content.replace(
    '"topic": "uwu_culture_recruitment" }',
    '"topic": "uwu_culture_recruitment",'
)

# Write fixed content back
with open('/home/ubuntu/.openclaw/workspace/moltbook-index.json', 'w') as f:
    f.write(fixed_content)

print("Fixed JSON structure in moltbook-index.json")
print("Now updating Moltbook index...")
