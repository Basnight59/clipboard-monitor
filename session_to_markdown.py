import json
import os

# Config: Adjust if needed
module_id = "chat-session-20250723"
meta_path = f"./ttl_modules/{module_id}.json"
txt_path = f"./ttl_modules/{module_id}.txt"
md_path = f"./ttl_modules/{module_id}.md"

# Load metadata and content
with open(meta_path, "r") as meta_file:
    metadata = json.load(meta_file)
with open(txt_path, "r") as txt_file:
    content = txt_file.read()

# Compose markdown
md = []
md.append(f"# TTL SDK Knowledge Module: `{module_id}`\n")
md.append(f"**Creator:** {metadata.get('authorship', {}).get('creator', 'N/A')}")
md.append(f"**Date:** {metadata.get('authorship', {}).get('date', 'N/A')}")
md.append(f"**License:** {metadata.get('license_type', 'N/A')}")
md.append(f"**Consent Policy:** {metadata.get('consent_policy', {})}")
md.append(f"**Tags:** {', '.join(metadata.get('cultural_tags', []))}")
md.append(f"**Spiritual Context:** {metadata.get('spiritual_context', 'universal')}")
md.append(f"**Created At:** {metadata.get('created_at', '')}\n")
md.append("---\n")
md.append(f"## Full Session Transcript\n")

# Process session into turns separated by '---'
lines = content.strip().splitlines()
turns = []
current_turn = []

for line in lines:
    if line.strip().startswith("USER:") and current_turn:
        turns.append('\n'.join(current_turn))
        current_turn = []
    current_turn.append(line)
if current_turn:
    turns.append('\n'.join(current_turn))

for turn in turns:
    md.append(turn.strip())
    md.append('\n---\n')

# Save as markdown file
with open(md_path, "w", encoding="utf-8") as md_file:
    md_file.write('\n'.join(md))

print(f"\n[SAVED] Markdown knowledge module with horizontal rules: {md_path}")
