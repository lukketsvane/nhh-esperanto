#!/usr/bin/env python3
"""
Enhanced matching script to match survey entries without IDs to conversations.

This script implements more flexible matching strategies for participants who
forgot to include their ID in their ChatGPT introduction message.
"""

import pandas as pd
import numpy as np
import re
from datetime import datetime, timedelta
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# File paths
DATA_DIR = Path(__file__).parent.parent / 'data'
RAW_DIR = DATA_DIR / 'raw'
PROCESSED_DIR = DATA_DIR / 'processed'

CONV_DATA_PATH = RAW_DIR / 'unified_conversation_data.csv'
PARTICIPANTS_PATH = PROCESSED_DIR / 'nhh_esperanto_participants.csv'
CONVERSATIONS_PATH = PROCESSED_DIR / 'nhh_esperanto_conversations.csv'
FINALIZED_DATASET_PATH = PROCESSED_DIR / 'nhh_esperanto_finalized_dataset.csv'

# Extended timestamp tolerance for difficult matches (48 hours)
EXTENDED_TOLERANCE = 48 * 60 * 60  # 48 hours in seconds


def load_data():
    """Load all necessary data files."""
    logger.info("Loading data files...")

    conv_df = pd.read_csv(CONV_DATA_PATH)
    participants_df = pd.read_csv(PARTICIPANTS_PATH)
    conversations_df = pd.read_csv(CONVERSATIONS_PATH)
    finalized_df = pd.read_csv(FINALIZED_DATASET_PATH)

    logger.info(f"Loaded {len(conv_df)} conversation messages")
    logger.info(f"Loaded {len(participants_df)} participants")
    logger.info(f"Loaded {len(conversations_df)} matched conversations")
    logger.info(f"Loaded {len(finalized_df)} finalized records")

    return conv_df, participants_df, conversations_df, finalized_df


def extract_first_user_message(conversation_id, conv_df):
    """Extract the first user message from a conversation."""
    conv_messages = conv_df[conv_df['conversation_id'] == conversation_id]
    user_messages = conv_messages[conv_messages['author_role'] == 'user']

    if user_messages.empty:
        return None

    # Sort by create_time if available, otherwise take first
    user_messages = user_messages.sort_values('create_time')
    first_msg = user_messages.iloc[0]['message_content']

    # Clean the message content
    if pd.notna(first_msg):
        # Remove array brackets if present
        msg = str(first_msg).strip("[]'\"")
        return msg
    return None


def extract_user_id_patterns(message):
    """
    Extract potential user IDs using multiple patterns.
    Returns list of potential IDs found.
    """
    if not message or pd.isna(message):
        return []

    message = str(message)
    found_ids = []

    # Pattern 1: Standard format DDMMYYYY_HHMM_ParticipantN or DDMMYYYY_HHMM_N
    match = re.search(r'(\d{2})(\d{2})(\d{4})_(\d{4})_(?:Participant)?(\d+)', message, re.IGNORECASE)
    if match:
        day, month, year, time, num = match.groups()
        found_ids.append(f"{day}{month}{year}_{time}_Participant{num}")
        found_ids.append(f"{day}{month}{year}_{time}_{num}")

    # Pattern 2: Date with slashes/dashes and time
    match = re.search(r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})[\s_]+(\d{1,2})[:\.]?(\d{2})[\s_]+(\d+)', message)
    if match:
        day, month, year, hour, minute, num = match.groups()
        if len(year) == 2:
            year = f"20{year}"
        day = day.zfill(2)
        month = month.zfill(2)
        hour = hour.zfill(2)
        minute = minute.zfill(2)
        found_ids.append(f"{day}{month}{year}_{hour}{minute}_{num}")

    # Pattern 3: "My ID is X" or "ID: X"
    match = re.search(r'(?:my\s+)?ID(?:\s+is)?[\s:]+(\S+)', message, re.IGNORECASE)
    if match:
        found_ids.append(match.group(1))

    # Pattern 4: Participant number
    match = re.search(r'[Pp]articipant\s*(\d+)', message)
    if match:
        found_ids.append(f"Participant{match.group(1)}")

    # Pattern 5: Any number that could be an ID (2-4 digits)
    matches = re.findall(r'\b(\d{2,4})\b', message)
    found_ids.extend(matches)

    return list(set(found_ids))  # Remove duplicates


def find_unmatched_conversations(conv_df, conversations_df):
    """Find conversations that haven't been matched yet."""
    matched_conv_ids = set(conversations_df['conversation_id'].unique())
    all_conv_ids = set(conv_df['conversation_id'].unique())

    unmatched_conv_ids = all_conv_ids - matched_conv_ids

    logger.info(f"Found {len(unmatched_conv_ids)} unmatched conversations")

    # Get details of unmatched conversations
    unmatched_details = []
    for conv_id in unmatched_conv_ids:
        conv_subset = conv_df[conv_df['conversation_id'] == conv_id]
        create_time = conv_subset['create_time'].iloc[0]
        first_msg = extract_first_user_message(conv_id, conv_df)

        # Skip test conversations with just "login"
        if first_msg and first_msg.strip().lower() != 'login':
            unmatched_details.append({
                'conversation_id': conv_id,
                'create_time': create_time,
                'create_datetime': datetime.fromtimestamp(create_time),
                'first_user_message': first_msg,
                'potential_ids': extract_user_id_patterns(first_msg)
            })

    logger.info(f"Found {len(unmatched_details)} valid unmatched conversations (excluding 'login' messages)")

    return pd.DataFrame(unmatched_details)


def find_unmatched_participants(participants_df, conversations_df):
    """Find participants who don't have matched conversations."""
    matched_participant_ids = set(conversations_df['participant_id'].unique())
    all_participant_ids = set(participants_df['participant_id'].unique())

    unmatched_participant_ids = all_participant_ids - matched_participant_ids

    logger.info(f"Found {len(unmatched_participant_ids)} unmatched participants")

    return unmatched_participant_ids


def get_survey_timestamps(finalized_df, participant_id):
    """Get start and end timestamps for a participant from survey data."""
    # Extract participant number
    p_num = int(participant_id.replace('P', ''))

    # Find matching records in finalized dataset
    # Note: finalized dataset has one row per response, not per participant
    # We need to find records that could belong to this participant

    # For now, return None - we'd need to map participant_id to ResponseId
    return None, None


def match_by_extended_timestamp(unmatched_convs_df, finalized_df):
    """
    Try to match conversations to survey responses using extended timestamp tolerance.
    """
    logger.info("Attempting extended timestamp matching...")

    # Get unmatched survey responses from finalized dataset
    unmatched_surveys = finalized_df[
        (finalized_df['conversation_id'].isna()) |
        (finalized_df['conversation_id'] == '') |
        (finalized_df['HasMatch'] == False)
    ].copy()

    logger.info(f"Found {len(unmatched_surveys)} unmatched survey responses")

    if unmatched_surveys.empty or unmatched_convs_df.empty:
        logger.info("No unmatched surveys or conversations to match")
        return pd.DataFrame()

    matches = []

    # Convert timestamps
    unmatched_surveys['start_time_unix'] = pd.to_numeric(
        unmatched_surveys['start_time_unix'], errors='coerce'
    )

    # For each unmatched conversation, find closest survey response
    for idx, conv_row in unmatched_convs_df.iterrows():
        conv_time = conv_row['create_time']
        conv_id = conv_row['conversation_id']

        # Calculate time differences
        unmatched_surveys['time_diff'] = abs(
            unmatched_surveys['start_time_unix'] - conv_time
        )

        # Find closest match within extended tolerance
        valid_matches = unmatched_surveys[
            unmatched_surveys['time_diff'] <= EXTENDED_TOLERANCE
        ].copy()

        if not valid_matches.empty:
            # Get best match (smallest time difference)
            best_match = valid_matches.nsmallest(1, 'time_diff').iloc[0]

            time_diff_minutes = best_match['time_diff'] / 60

            matches.append({
                'conversation_id': conv_id,
                'ResponseId': best_match['ResponseId'],
                'create_time': conv_time,
                'survey_start_time': best_match['start_time_unix'],
                'time_diff_minutes': time_diff_minutes,
                'first_user_message': conv_row['first_user_message'],
                'match_method': 'ExtendedTimestamp',
                'match_confidence': max(0, 100 - (time_diff_minutes / 10))  # Decrease confidence with time
            })

            logger.info(f"Matched conversation {conv_id[:8]}... to survey {best_match['ResponseId']} "
                       f"(time diff: {time_diff_minutes:.1f} minutes)")

    logger.info(f"Found {len(matches)} new matches using extended timestamp matching")

    return pd.DataFrame(matches)


def main():
    """Main execution function."""
    logger.info("=" * 60)
    logger.info("Enhanced ID Matching Script")
    logger.info("=" * 60)

    # Load data
    conv_df, participants_df, conversations_df, finalized_df = load_data()

    # Find unmatched conversations and participants
    unmatched_convs_df = find_unmatched_conversations(conv_df, conversations_df)
    unmatched_participant_ids = find_unmatched_participants(participants_df, conversations_df)

    # Display unmatched conversation details
    if not unmatched_convs_df.empty:
        logger.info("\n" + "=" * 60)
        logger.info("UNMATCHED CONVERSATIONS:")
        logger.info("=" * 60)
        for idx, row in unmatched_convs_df.iterrows():
            logger.info(f"\nConversation: {row['conversation_id'][:16]}...")
            logger.info(f"  Time: {row['create_datetime']}")
            logger.info(f"  First message: {row['first_user_message'][:100]}")
            logger.info(f"  Potential IDs: {row['potential_ids']}")

    # Try extended timestamp matching
    new_matches_df = match_by_extended_timestamp(unmatched_convs_df, finalized_df)

    # Save results
    if not new_matches_df.empty:
        output_path = PROCESSED_DIR / 'enhanced_matches.csv'
        new_matches_df.to_csv(output_path, index=False)
        logger.info(f"\nSaved {len(new_matches_df)} new matches to {output_path}")

        # Display summary
        logger.info("\n" + "=" * 60)
        logger.info("SUMMARY OF NEW MATCHES:")
        logger.info("=" * 60)
        logger.info(f"Total new matches: {len(new_matches_df)}")
        logger.info(f"Average time difference: {new_matches_df['time_diff_minutes'].mean():.1f} minutes")
        logger.info(f"Max time difference: {new_matches_df['time_diff_minutes'].max():.1f} minutes")
        logger.info(f"Average confidence: {new_matches_df['match_confidence'].mean():.1f}%")
    else:
        logger.info("\nNo new matches found")

    # Final statistics
    logger.info("\n" + "=" * 60)
    logger.info("FINAL STATISTICS:")
    logger.info("=" * 60)
    logger.info(f"Total participants: {len(participants_df)}")
    logger.info(f"Previously matched: {len(conversations_df)}")
    logger.info(f"Still unmatched: {len(unmatched_participant_ids)}")
    logger.info(f"New matches found: {len(new_matches_df)}")
    logger.info(f"Remaining unmatched: {len(unmatched_participant_ids) - len(new_matches_df)}")


if __name__ == '__main__':
    main()
