#!/usr/bin/env python3
"""
Aggressive rematching with extended tolerance and smart strategies.
"""

import pandas as pd
import re
from datetime import datetime
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent / 'data'
RAW_DIR = DATA_DIR / 'raw'
PROCESSED_DIR = DATA_DIR / 'processed'

def extract_user_id_from_message(message):
    """Extract user ID from message."""
    if not message or pd.isna(message):
        return None

    message = str(message).strip("[]'\"")

    # Multiple patterns
    patterns = [
        r'(\d{2})(\d{2})(\d{4})[_\s]+(\d{2}):?(\d{2})[_\s]+(\d+)',
        r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})[_\s]+(\d{1,2}):(\d{2})[_\s]*(\d+)?',
    ]

    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            return match.group(0)

    return None


def main():
    logger.info("=" * 70)
    logger.info("AGGRESSIVE REMATCHING WITH EXTENDED TOLERANCE")
    logger.info("=" * 70)

    # Load data
    finalized_df = pd.read_csv(PROCESSED_DIR / 'nhh_esperanto_finalized_dataset.csv')
    conv_df = pd.read_csv(RAW_DIR / 'unified_conversation_data_complete.csv')

    # Get unmatched surveys
    unmatched = finalized_df[finalized_df['conversation_id'].isna()].copy()
    logger.info(f"Unmatched surveys: {len(unmatched)}")

    # Get all conversations with their first message
    conv_details = []
    for conv_id in conv_df['conversation_id'].unique():
        conv_msgs = conv_df[conv_df['conversation_id'] == conv_id]
        user_msgs = conv_msgs[conv_msgs['author_role'] == 'user']

        if user_msgs.empty:
            continue

        first_msg = str(user_msgs.iloc[0]['message_content']).strip("[]'\"")

        # Skip login messages
        if first_msg.lower().strip() == 'login':
            continue

        # Get create time
        create_time_str = str(conv_msgs.iloc[0]['create_time'])
        try:
            if '.' in create_time_str and len(create_time_str) > 15:
                dt = pd.to_datetime(create_time_str)
                create_time = dt.timestamp()
            else:
                create_time = float(create_time_str)
        except:
            continue

        conv_details.append({
            'conversation_id': conv_id,
            'create_time': create_time,
            'first_message': first_msg,
            'extracted_id': extract_user_id_from_message(first_msg)
        })

    logger.info(f"Valid conversations: {len(conv_details)}")

    # Check which conversations are already used
    used_convs = set(finalized_df[finalized_df['conversation_id'].notna()]['conversation_id'].unique())
    available_convs = [c for c in conv_details if c['conversation_id'] not in used_convs]
    logger.info(f"Available (unused) conversations: {len(available_convs)}")

    # Try matching with VERY wide tolerance
    unmatched['start_time_unix'] = pd.to_numeric(unmatched['start_time_unix'], errors='coerce')

    tolerances = [
        (7 * 24 * 60 * 60, "7 days"),
        (14 * 24 * 60 * 60, "14 days"),
        (30 * 24 * 60 * 60, "30 days"),
    ]

    all_new_matches = []

    for tolerance, label in tolerances:
        logger.info(f"\n=== TRYING {label} TOLERANCE ===")

        current_unmatched = unmatched[~unmatched['ResponseId'].isin([m['ResponseId'] for m in all_new_matches])]
        current_available = [c for c in available_convs if c['conversation_id'] not in [m['conversation_id'] for m in all_new_matches]]

        logger.info(f"Remaining unmatched: {len(current_unmatched)}")
        logger.info(f"Remaining available convs: {len(current_available)}")

        for conv in current_available:
            conv_time = conv['create_time']
            conv_id = conv['conversation_id']

            # Find closest survey
            current_unmatched['time_diff'] = abs(current_unmatched['start_time_unix'] - conv_time)

            valid_matches = current_unmatched[current_unmatched['time_diff'] <= tolerance]

            if not valid_matches.empty:
                best_match = valid_matches.nsmallest(1, 'time_diff').iloc[0]

                all_new_matches.append({
                    'conversation_id': conv_id,
                    'ResponseId': best_match['ResponseId'],
                    'time_diff_hours': best_match['time_diff'] / 3600,
                    'time_diff_days': best_match['time_diff'] / (24 * 3600),
                    'first_message': conv['first_message'],
                    'extracted_id': conv['extracted_id'],
                    'tolerance_used': label
                })

                logger.info(f"✓ Matched {conv_id[:20]}... to {best_match['ResponseId']} ({best_match['time_diff'] / (24*3600):.1f} days)")

        logger.info(f"New matches at {label} tolerance: {len([m for m in all_new_matches if m['tolerance_used'] == label])}")

    logger.info(f"\n=== FINAL RESULTS ===")
    logger.info(f"Total new matches: {len(all_new_matches)}")

    if all_new_matches:
        new_matches_df = pd.DataFrame(all_new_matches)
        output_path = PROCESSED_DIR / 'aggressive_rematching_results.csv'
        new_matches_df.to_csv(output_path, index=False)
        logger.info(f"Saved to {output_path}")

        # Show distribution
        print(f"\n=== MATCHES BY TOLERANCE ===")
        print(new_matches_df['tolerance_used'].value_counts())

        print(f"\n=== TIME DIFFERENCE STATS ===")
        print(f"Average: {new_matches_df['time_diff_days'].mean():.1f} days")
        print(f"Median: {new_matches_df['time_diff_days'].median():.1f} days")
        print(f"Max: {new_matches_df['time_diff_days'].max():.1f} days")

    logger.info("\n" + "=" * 70)
    logger.info("AGGRESSIVE REMATCHING COMPLETE")
    logger.info("=" * 70)


if __name__ == '__main__':
    main()
