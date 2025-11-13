#!/usr/bin/env python3
"""
Process conversation data from promptdata folders (CSN1-CSN22) and merge with the unified dataset.
Export final dataset with all matched participants.
"""

import json
import logging
import re
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List

import pandas as pd
import numpy as np

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# File paths
PROJECT_DIR = Path(__file__).parent.parent
PROMPTDATA_DIR = PROJECT_DIR / 'promptdata'
DATA_DIR = PROJECT_DIR / 'data'
PROCESSED_DIR = DATA_DIR / 'processed'

# ID extraction patterns
STRICT_ID_PATTERNS = [
    re.compile(
        r"\b(?P<day>\d{2})(?P<month>\d{2})(?P<year>\d{4})[_\s-]*(?P<hour>\d{2})(?P<minute>\d{2})[_\s-]*Participant\s*(?P<participant>\d{1,3})(?![\w])",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?P<day>\d{2})(?P<month>\d{2})(?P<year>\d{4})[_\s-]*(?P<hour>\d{2})[:h](?P<minute>\d{2})[_\s-]*Participant\s*(?P<participant>\d{1,3})(?![\w])",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bParticipant\s*(?P<participant>\d{1,3})(?![\w])[_\s-]*(?P<day>\d{2})(?P<month>\d{2})(?P<year>\d{4})[_\s-]*(?P<hour>\d{2})(?P<minute>\d{2})\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?P<day>\d{1,2})[/-](?P<month>\d{1,2})[/-](?P<year>\d{2,4}).{0,40}?(?P<hour>\d{1,2})[:.h](?P<minute>\d{2}).{0,40}?Participant\s*(?P<participant>\d{1,3})(?![\w])",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bParticipant\s*(?P<participant>\d{1,3})(?![\w]).{0,40}?(?P<day>\d{1,2})[/-](?P<month>\d{1,2})[/-](?P<year>\d{2,4}).{0,40}?(?P<hour>\d{1,2})[:.h](?P<minute>\d{2})",
        re.IGNORECASE,
    ),
]


def normalize_components(match: re.Match) -> Optional[str]:
    """Normalize date/time components from regex match."""
    groups = match.groupdict()

    try:
        day = int(groups['day'])
        month = int(groups['month'])
        year = int(groups['year']) if len(groups['year']) == 4 else int(f"20{groups['year']}")
        hour = int(groups['hour'])
        minute = int(groups['minute'])
        participant = int(groups['participant'])
    except (KeyError, ValueError):
        return None

    if not (1 <= day <= 31 and 1 <= month <= 12):
        return None
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        return None
    if participant <= 0:
        return None

    return f"{day:02d}{month:02d}{year:04d}_{hour:02d}{minute:02d}_Participant{participant}"


def extract_user_id_from_message(message: str) -> Optional[str]:
    """Extract user ID from message text."""
    if not message or (isinstance(message, float) and pd.isna(message)):
        return None

    text = str(message).strip("[]'\"")

    for pattern in STRICT_ID_PATTERNS:
        match = pattern.search(text)
        if not match:
            continue

        normalized = normalize_components(match)
        if normalized:
            return normalized

    return None


def extract_conversations_from_folder(folder_path: Path) -> List[Dict]:
    """Extract conversation data from a CSN folder."""
    conversations = []

    # Look for conversations.json in both root and subdirectory
    conv_files = list(folder_path.rglob('conversations.json'))

    for conv_file in conv_files:
        try:
            with open(conv_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Handle both list and dict formats
            conv_list = data if isinstance(data, list) else [data]

            for conv in conv_list:
                if not isinstance(conv, dict):
                    continue

                conv_id = conv.get('id')
                if not conv_id:
                    continue

                # Extract basic conversation info
                create_time = conv.get('create_time', 0)
                title = conv.get('title', '')
                mapping = conv.get('mapping', {})

                # Extract messages
                messages = []
                for msg_id, msg_data in mapping.items():
                    if not isinstance(msg_data, dict):
                        continue

                    message = msg_data.get('message')
                    if not message or not isinstance(message, dict):
                        continue

                    author_role = message.get('author', {}).get('role', '')
                    content_parts = message.get('content', {}).get('parts', [])
                    msg_create_time = message.get('create_time', create_time)

                    # Join content parts
                    message_content = ' '.join([str(p) for p in content_parts if p])

                    if message_content and author_role:
                        messages.append({
                            'message_id': msg_id,
                            'author_role': author_role,
                            'message_content': message_content,
                            'create_time': msg_create_time
                        })

                if messages:
                    conversations.append({
                        'conversation_id': conv_id,
                        'title': title,
                        'create_time': create_time,
                        'messages': messages,
                        'folder': folder_path.name
                    })

        except Exception as e:
            logger.warning(f"Error processing {conv_file}: {e}")

    return conversations


def calculate_conversation_stats(messages: List[Dict]) -> Dict:
    """Calculate statistics for a conversation."""
    user_msgs = [m for m in messages if m['author_role'] == 'user']
    ai_msgs = [m for m in messages if m['author_role'] == 'assistant']

    user_lengths = [len(m['message_content']) for m in user_msgs] if user_msgs else [0]
    ai_lengths = [len(m['message_content']) for m in ai_msgs] if ai_msgs else [0]

    # Calculate duration
    times = [m['create_time'] for m in messages if m['create_time']]
    duration = max(times) - min(times) if len(times) > 1 else 0

    return {
        'MessageCount': len(messages),
        'UserMessageCount': len(user_msgs),
        'AIMessageCount': len(ai_msgs),
        'AverageUserMessageLength': np.mean(user_lengths),
        'AverageAIMessageLength': np.mean(ai_lengths),
        'ConversationDuration': duration,
        'ConversationDurationMinutes': duration / 60
    }


def main():
    """Main execution."""
    logger.info("=" * 80)
    logger.info("PROCESSING PROMPTDATA AND EXPORTING FINAL DATASET")
    logger.info("=" * 80)

    # Load current unified dataset
    unified_df = pd.read_csv(PROCESSED_DIR / 'nhh_esperanto_complete_unified.csv')
    logger.info(f"\nLoaded unified dataset: {len(unified_df)} participants")
    logger.info(f"  - With conversation_id: {unified_df['conversation_id'].notna().sum()}")
    logger.info(f"  - Without conversation_id: {unified_df['conversation_id'].isna().sum()}")

    # Extract conversations from all promptdata folders
    logger.info(f"\n{'='*80}")
    logger.info("EXTRACTING CONVERSATIONS FROM PROMPTDATA")
    logger.info(f"{'='*80}")

    all_conversations = []
    csn_folders = sorted([d for d in PROMPTDATA_DIR.iterdir() if d.is_dir() and d.name.startswith('CSN')])

    logger.info(f"Found {len(csn_folders)} CSN folders")

    for folder in csn_folders:
        logger.info(f"\nProcessing {folder.name}...")
        convs = extract_conversations_from_folder(folder)
        all_conversations.extend(convs)
        logger.info(f"  Extracted {len(convs)} conversations")

    logger.info(f"\nTotal conversations extracted: {len(all_conversations)}")

    # Get unmatched participants
    unmatched_df = unified_df[unified_df['conversation_id'].isna()].copy()
    logger.info(f"\n{'='*80}")
    logger.info(f"MATCHING {len(all_conversations)} CONVERSATIONS TO {len(unmatched_df)} UNMATCHED PARTICIPANTS")
    logger.info(f"{'='*80}")

    # Prepare timestamp column
    unmatched_df['start_time_unix'] = pd.to_numeric(unmatched_df['start_time_unix'], errors='coerce')

    # Track matches
    matches = []
    matched_conv_ids = set()
    matched_response_ids = set()

    # Match conversations to participants
    for conv in all_conversations:
        if conv['conversation_id'] in matched_conv_ids:
            continue

        messages = conv['messages']
        if not messages:
            continue

        # Get first user message
        user_msgs = [m for m in messages if m['author_role'] == 'user']
        if not user_msgs:
            continue

        first_msg = user_msgs[0]['message_content']
        conv_create_time = conv['create_time']

        # Extract ID from message
        extracted_id = extract_user_id_from_message(first_msg)

        # Match by timestamp (within 24 hours)
        try:
            create_time_float = float(conv_create_time)
        except (ValueError, TypeError):
            logger.warning(f"Could not parse create_time: {conv_create_time}")
            continue

        # Calculate time differences with unmatched participants
        available_unmatched = unmatched_df[~unmatched_df['ResponseId'].isin(matched_response_ids)].copy()
        if available_unmatched.empty:
            break

        available_unmatched['time_diff'] = abs(available_unmatched['start_time_unix'] - create_time_float)

        # Find closest match within 24 hours
        tolerance = 24 * 60 * 60  # 24 hours
        valid_matches = available_unmatched[available_unmatched['time_diff'] <= tolerance]

        if not valid_matches.empty:
            best_match = valid_matches.nsmallest(1, 'time_diff').iloc[0]

            # Calculate conversation statistics
            stats = calculate_conversation_stats(messages)

            match_info = {
                'conversation_id': conv['conversation_id'],
                'ResponseId': best_match['ResponseId'],
                'create_time': create_time_float,
                'survey_start_time': best_match['start_time_unix'],
                'time_diff_hours': best_match['time_diff'] / 3600,
                'first_user_message': first_msg[:200],
                'extracted_id': extracted_id,
                'match_method': 'PromptData',
                'folder': conv['folder'],
                **stats
            }

            matches.append(match_info)
            matched_conv_ids.add(conv['conversation_id'])
            matched_response_ids.add(best_match['ResponseId'])

            logger.info(f"✓ Matched {conv['folder']}/{conv['conversation_id'][:20]}... to {best_match['ResponseId']}")
            logger.info(f"  Time diff: {best_match['time_diff'] / 3600:.2f} hours")

    logger.info(f"\n{'='*80}")
    logger.info(f"MATCHING SUMMARY")
    logger.info(f"{'='*80}")
    logger.info(f"Total conversations found: {len(all_conversations)}")
    logger.info(f"Successfully matched: {len(matches)}")
    logger.info(f"Match rate: {len(matches) / len(all_conversations) * 100:.1f}%")

    # Update unified dataset with new matches
    logger.info(f"\n{'='*80}")
    logger.info("UPDATING UNIFIED DATASET")
    logger.info(f"{'='*80}")

    updated_df = unified_df.copy()

    for match in matches:
        mask = updated_df['ResponseId'] == match['ResponseId']

        # Update fields
        updated_df.loc[mask, 'conversation_id'] = match['conversation_id']
        updated_df.loc[mask, 'create_time'] = match['create_time']
        updated_df.loc[mask, 'start_time_unix'] = match['survey_start_time']
        updated_df.loc[mask, 'UserID'] = match['extracted_id'] if match['extracted_id'] else f"Generated_{datetime.fromtimestamp(match['create_time']).strftime('%d%m%Y_%H%M')}"
        updated_df.loc[mask, 'HasMatch'] = True
        updated_df.loc[mask, 'MatchMethod'] = 'PromptData'
        updated_df.loc[mask, 'data_status'] = 'Recovered from promptdata'
        updated_df.loc[mask, 'UserID_Source'] = 'promptdata_conversation'
        updated_df.loc[mask, 'MessageCount'] = match['MessageCount']
        updated_df.loc[mask, 'UserMessageCount'] = match['UserMessageCount']
        updated_df.loc[mask, 'AIMessageCount'] = match['AIMessageCount']
        updated_df.loc[mask, 'AverageUserMessageLength'] = match['AverageUserMessageLength']
        updated_df.loc[mask, 'AverageAIMessageLength'] = match['AverageAIMessageLength']
        updated_df.loc[mask, 'ConversationDuration'] = match['ConversationDuration']
        updated_df.loc[mask, 'ConversationDurationMinutes'] = match['ConversationDurationMinutes']

    # Export final dataset
    output_path = PROCESSED_DIR / 'nhh_esperanto_complete_unified_updated.csv'
    updated_df.to_csv(output_path, index=False)
    logger.info(f"\nExported updated dataset to: {output_path}")

    # Save match details
    if matches:
        matches_df = pd.DataFrame(matches)
        matches_output = PROCESSED_DIR / 'promptdata_matches.csv'
        matches_df.to_csv(matches_output, index=False)
        logger.info(f"Saved match details to: {matches_output}")

    # Final statistics
    logger.info(f"\n{'='*80}")
    logger.info("FINAL DATASET STATISTICS")
    logger.info(f"{'='*80}")
    logger.info(f"Total participants: {len(updated_df)}")
    logger.info(f"With conversation data: {updated_df['conversation_id'].notna().sum()}")
    logger.info(f"Without conversation data: {updated_df['conversation_id'].isna().sum()}")
    logger.info(f"Overall match rate: {updated_df['conversation_id'].notna().sum() / len(updated_df) * 100:.1f}%")

    # Breakdown by data source
    if 'data_status' in updated_df.columns:
        logger.info(f"\nData sources:")
        for status, count in updated_df['data_status'].value_counts().items():
            logger.info(f"  {status}: {count}")

    logger.info(f"\n{'='*80}")
    logger.info("EXPORT COMPLETE")
    logger.info(f"{'='*80}")
    logger.info(f"\nFinal dataset saved to:")
    logger.info(f"  {output_path}")


if __name__ == '__main__':
    main()
