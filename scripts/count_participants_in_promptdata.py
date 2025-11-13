#!/usr/bin/env python3
"""Count unique participants in promptdata."""

import json
from pathlib import Path
from collections import Counter

PROJECT_DIR = Path(__file__).parent.parent
PROMPTDATA_DIR = PROJECT_DIR / 'promptdata'

# Get all CSN folders
csn_folders = sorted([d for d in PROMPTDATA_DIR.iterdir() if d.is_dir() and d.name.startswith('CSN')])

total_conversations = 0
matched_conversations = 0
participant_ids = []

for folder in csn_folders:
    conv_files = list(folder.rglob('conversations.json'))

    for conv_file in conv_files:
        try:
            with open(conv_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            conversations = data if isinstance(data, list) else [data]

            for conv in conversations:
                if not isinstance(conv, dict):
                    continue

                total_conversations += 1

                participant_id = conv.get('participant_id')
                if participant_id:
                    matched_conversations += 1
                    participant_ids.append(participant_id)

        except Exception as e:
            print(f"Error reading {conv_file}: {e}")

# Count unique participants
unique_participants = len(set(participant_ids))
participant_counts = Counter(participant_ids)
multiple_conversations = sum(1 for count in participant_counts.values() if count > 1)

print("=" * 80)
print("PROMPTDATA PARTICIPANT ANALYSIS")
print("=" * 80)
print(f"\nTotal conversations: {total_conversations}")
print(f"Conversations with participant_id: {matched_conversations}")
print(f"Conversations without participant_id: {total_conversations - matched_conversations}")
print(f"\nUnique participants in promptdata: {unique_participants}")
print(f"Participants with multiple conversations: {multiple_conversations}")
print(f"\nMatch rate: {matched_conversations / total_conversations * 100:.1f}%")

if multiple_conversations > 0:
    print(f"\nParticipants with multiple conversations:")
    for pid, count in participant_counts.most_common(10):
        if count > 1:
            print(f"  {pid}: {count} conversations")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Main dataset participants: 604")
print(f"Promptdata unique participants: {unique_participants}")
print(f"Promptdata total conversations: {total_conversations}")
print("=" * 80)
