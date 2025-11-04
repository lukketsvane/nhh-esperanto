#!/usr/bin/env python3
"""
Match the 21 recovered conversations to unmatched surveys.
"""

import re
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional

import pandas as pd

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


def _normalize_components(match: re.Match) -> Optional[str]:
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

    return (
        f"{day:02d}{month:02d}{year:04d}_{hour:02d}{minute:02d}_Participant{participant}"
    )


def extract_user_id_from_message(message):
    """Extract user ID from message text, enforcing a timestamp + participant pattern."""
    if not message or (isinstance(message, float) and pd.isna(message)):
        return None

    text = str(message).strip("[]'\"")

    for pattern in STRICT_ID_PATTERNS:
        match = pattern.search(text)
        if not match:
            continue

        normalized = _normalize_components(match)
        if normalized:
            return normalized

    return None


def main():
    """Main execution."""
    logger.info("=" * 70)
    logger.info("MATCHING RECOVERED CONVERSATIONS TO UNMATCHED SURVEYS")
    logger.info("=" * 70)

    # Load recovered conversation messages
    recovered_msgs = pd.read_csv(PROCESSED_DIR / 'recovered_conversation_messages.csv')
    logger.info(f"Loaded {len(recovered_msgs)} messages from {recovered_msgs['conversation_id'].nunique()} recovered conversations")

    # Load finalized dataset
    finalized_df = pd.read_csv(PROCESSED_DIR / 'nhh_esperanto_finalized_dataset.csv')
    logger.info(f"Loaded finalized dataset: {len(finalized_df)} entries")

    # Get unmatched surveys
    unmatched = finalized_df[finalized_df['conversation_id'].isna()].copy()
    logger.info(f"Unmatched surveys: {len(unmatched)}")

    # Get unique recovered conversation IDs
    recovered_conv_ids = recovered_msgs['conversation_id'].unique()

    # For each recovered conversation, extract first user message and ID
    recovered_details = []
    for conv_id in recovered_conv_ids:
        conv_msgs = recovered_msgs[recovered_msgs['conversation_id'] == conv_id]
        user_msgs = conv_msgs[conv_msgs['author_role'] == 'user']

        if user_msgs.empty:
            continue

        first_msg = user_msgs.iloc[0]['message_content']
        create_time = conv_msgs.iloc[0]['create_time']

        # Extract ID from message
        user_id = extract_user_id_from_message(first_msg)

        recovered_details.append({
            'conversation_id': conv_id,
            'create_time': create_time,
            'first_user_message': first_msg,
            'extracted_id': user_id
        })

    logger.info(f"\n=== RECOVERED CONVERSATIONS ===")
    for detail in recovered_details:
        logger.info(f"{detail['conversation_id'][:30]}... : {detail['extracted_id']}")

    # Try to match recovered conversations to unmatched surveys
    # Method 1: By explicit ID
    # Method 2: By timestamp proximity

    new_matches = []

    # Method 1: Explicit ID matching
    logger.info(f"\n=== MATCHING BY EXPLICIT ID ===")
    for detail in recovered_details:
        if not detail['extracted_id']:
            continue

        extracted_id = detail['extracted_id']

        # Try to match with survey
        # The survey data doesn't have a direct ID field to match,
        # so we'll use timestamp matching as primary method

    # Method 2: Timestamp matching
    logger.info(f"\n=== MATCHING BY TIMESTAMP ===")
    unmatched['start_time_unix'] = pd.to_numeric(unmatched['start_time_unix'], errors='coerce')

    for detail in recovered_details:
        # Parse create_time (could be unix timestamp or datetime string)
        try:
            create_time = float(detail['create_time'])
        except (ValueError, TypeError):
            # Try parsing as datetime string
            try:
                dt = pd.to_datetime(detail['create_time'])
                create_time = dt.timestamp()
            except:
                logger.warning(f"Could not parse create_time: {detail['create_time']}")
                continue

        conv_id = detail['conversation_id']

        # Calculate time differences
        unmatched['time_diff'] = abs(unmatched['start_time_unix'] - create_time)

        # Find closest match within 24 hours
        tolerance = 24 * 60 * 60  # 24 hours
        valid_matches = unmatched[unmatched['time_diff'] <= tolerance]

        if not valid_matches.empty:
            best_match = valid_matches.nsmallest(1, 'time_diff').iloc[0]

            new_matches.append({
                'conversation_id': conv_id,
                'ResponseId': best_match['ResponseId'],
                'create_time': create_time,
                'survey_start_time': best_match['start_time_unix'],
                'time_diff_hours': best_match['time_diff'] / 3600,
                'first_user_message': detail['first_user_message'],
                'extracted_id': detail['extracted_id'],
                'match_method': 'RecoveredTimestamp'
            })

            logger.info(f"✓ Matched {conv_id[:20]}... to {best_match['ResponseId']}")
            logger.info(f"  Time diff: {best_match['time_diff'] / 3600:.1f} hours")
            logger.info(f"  First msg: {detail['first_user_message'][:60]}")

            # Remove from unmatched to avoid duplicate matching
            unmatched = unmatched[unmatched['ResponseId'] != best_match['ResponseId']]

    logger.info(f"\n=== MATCHING SUMMARY ===")
    logger.info(f"Total recovered conversations: {len(recovered_details)}")
    logger.info(f"Successfully matched: {len(new_matches)}")
    logger.info(f"Remaining unmatched surveys: {len(unmatched)}")

    # Save new matches
    if new_matches:
        new_matches_df = pd.DataFrame(new_matches)
        output_path = PROCESSED_DIR / 'recovered_matches.csv'
        new_matches_df.to_csv(output_path, index=False)
        logger.info(f"\nSaved new matches to {output_path}")

        # Update finalized dataset
        logger.info("\n=== UPDATING FINALIZED DATASET ===")
        finalized_updated = finalized_df.copy()

        for idx, match in new_matches_df.iterrows():
            response_id = match['ResponseId']
            conv_id = match['conversation_id']

            # Find the row in finalized dataset
            mask = finalized_updated['ResponseId'] == response_id

            # Update fields
            finalized_updated.loc[mask, 'conversation_id'] = conv_id
            finalized_updated.loc[mask, 'create_time'] = match['create_time']
            finalized_updated.loc[mask, 'UserID'] = match['extracted_id'] if pd.notna(match['extracted_id']) else f"Generated_{datetime.fromtimestamp(match['create_time']).strftime('%d%m%Y_%H%M')}"
            finalized_updated.loc[mask, 'MatchMethod'] = 'RecoveredData'
            finalized_updated.loc[mask, 'HasMatch'] = True
            finalized_updated.loc[mask, 'data_status'] = 'Recovered'
            finalized_updated.loc[mask, 'UserID_Source'] = 'recovered_conversation'

        # Save updated dataset
        updated_output = PROCESSED_DIR / 'nhh_esperanto_finalized_dataset_with_recovered.csv'
        finalized_updated.to_csv(updated_output, index=False)
        logger.info(f"Saved updated dataset to {updated_output}")

        # Statistics
        logger.info(f"\n=== FINAL STATISTICS ===")
        logger.info(f"Original matched: {finalized_df['HasMatch'].sum()}")
        logger.info(f"Newly matched: {len(new_matches)}")
        logger.info(f"Total matched: {finalized_updated['HasMatch'].sum()}")
        logger.info(f"Remaining unmatched: {(~finalized_updated['HasMatch']).sum()}")
        logger.info(f"Match rate: {finalized_updated['HasMatch'].sum() / len(finalized_updated) * 100:.1f}%")

    logger.info("\n" + "=" * 70)
    logger.info("MATCHING COMPLETE")
    logger.info("=" * 70)


if __name__ == '__main__':
    main()
