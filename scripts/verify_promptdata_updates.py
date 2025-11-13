#!/usr/bin/env python3
"""Verify promptdata conversation files have been updated with participant information."""

import json
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
PROMPTDATA_DIR = PROJECT_DIR / 'promptdata'

# Check CSN1 folder as example
csn1_file = PROMPTDATA_DIR / 'CSN1' / 'csn1' / 'conversations.json'

with open(csn1_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

convs = data if isinstance(data, list) else [data]
matched = [c for c in convs if isinstance(c, dict) and c.get('participant_id')]

print(f'Total conversations in CSN1: {len(convs)}')
print(f'Conversations with participant_id: {len(matched)}')
print(f'Match rate: {len(matched) / len(convs) * 100:.1f}%')

if matched:
    sample = matched[0]
    print('\nSample matched conversation:')
    print(f'  Conversation ID: {sample.get("id", "")[:40]}...')
    print(f'  Participant ID: {sample.get("participant_id", "")}')
    print(f'  User ID: {sample.get("participant_user_id", "")}')
    print(f'  Match Method: {sample.get("match_method", "")}')
    print(f'  Participant Name: {sample.get("participant_name", "")}')
    print(f'  Matched: {sample.get("metadata", {}).get("matched_participant", False)}')
