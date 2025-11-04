#!/usr/bin/env python3
"""
Regenerate UserIDs for all matched entries and verify match quality.

This script:
1. For each matched conversation, extracts the stated ID from the first message
2. Generates a proper UserID based on timestamp if no ID stated
3. Updates the dataset with corrected UserIDs
4. Identifies potential mismatches where stated ID doesn't align with matched survey
"""

import pandas as pd
import re
from datetime import datetime
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


def extract_id_from_message(message):
    """Extract all potential ID patterns from a message."""
    if not message or pd.isna(message):
        return []

    message = str(message)
    found_ids = []

    # Pattern 1: DDMMYYYY_HHMM_N or DD/MM/YYYY_HHMM_N
    patterns = [
        r'(\d{2})[/-]?(\d{2})[/-]?(\d{4})[_\s]+(\d{2}):?(\d{2})[_\s#]+(\d+)',  # 03122024_1000_6
        r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})[_\s]+(\d{1,2}):(\d{2})[_\s#]*(\d+)',  # 5 December_1500_#19
        r'(\d{2})(\d{2})(\d{4})_(\d{2})(\d{2})_(\d+)',  # Standard format
    ]

    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            groups = match.groups()
            if len(groups) == 6:
                day, month, year, hour, minute, num = groups
                # Normalize
                day = day.zfill(2)
                month = month.zfill(2)
                if len(year) == 2:
                    year = f"20{year}"
                hour = hour.zfill(2)
                minute = minute.zfill(2)

                found_ids.append({
                    'id': f"{day}{month}{year}_{hour}{minute}_{num}",
                    'day': int(day),
                    'month': int(month),
                    'year': int(year),
                    'hour': int(hour),
                    'minute': int(minute),
                    'participant_num': int(num),
                    'pattern': 'datetime_participant'
                })

    # Pattern 2: Just "My ID is X" or "ID: X" where X is any string
    match = re.search(r'(?:my\s+)?ID(?:\s+is)?[\s:]+([^\s,\.]+)', message, re.IGNORECASE)
    if match:
        id_str = match.group(1)
        # Try to parse it
        found_ids.append({
            'id': id_str,
            'pattern': 'explicit_id'
        })

    # Pattern 3: Date-like pattern alone (might be participant number)
    match = re.search(r'(\d{2})/(\d{2})[_\s]+(\d{2}):(\d{2})[_\s]+(\d+)', message)
    if match:
        day, month, hour, minute, num = match.groups()
        found_ids.append({
            'id': f"{day}{month}_time_{hour}{minute}_{num}",
            'day': int(day),
            'month': int(month),
            'hour': int(hour),
            'minute': int(minute),
            'participant_num': int(num),
            'pattern': 'date_time_participant'
        })

    return found_ids


def generate_id_from_timestamp(timestamp):
    """Generate a standardized ID from unix timestamp."""
    if pd.isna(timestamp):
        return None

    dt = datetime.fromtimestamp(timestamp)
    return f"{dt.day:02d}{dt.month:02d}{dt.year}_{dt.hour:02d}{dt.minute:02d}"


def main():
    """Main execution."""
    logger.info("=" * 70)
    logger.info("REGENERATE IDS AND VERIFY MATCHES")
    logger.info("=" * 70)

    # Load data
    finalized_df = pd.read_csv(PROCESSED_DIR / 'nhh_esperanto_finalized_dataset.csv')
    conv_df = pd.read_csv(RAW_DIR / 'unified_conversation_data.csv')

    logger.info(f"Loaded {len(finalized_df)} survey responses")
    logger.info(f"Loaded {len(conv_df)} conversation messages")

    # Process matched entries
    matched = finalized_df[finalized_df['conversation_id'].notna()].copy()
    logger.info(f"\nProcessing {len(matched)} matched entries...")

    results = []

    for idx, row in matched.iterrows():
        conv_id = row['conversation_id']

        # Get first user message
        conv_subset = conv_df[conv_df['conversation_id'] == conv_id]
        user_msgs = conv_subset[conv_subset['author_role'] == 'user']

        first_msg = None
        conv_create_time = None

        if not user_msgs.empty:
            user_msgs = user_msgs.sort_values('create_time')
            first_msg = str(user_msgs.iloc[0]['message_content']).strip("[]'\"")
            conv_create_time = float(user_msgs.iloc[0]['create_time'])

        # Extract IDs from message
        extracted_ids = extract_id_from_message(first_msg)

        # Get survey timestamp
        survey_time = row.get('start_time_unix')
        if pd.notna(survey_time):
            survey_time = float(survey_time)
            survey_dt = datetime.fromtimestamp(survey_time)
        else:
            survey_dt = None

        # Get conversation timestamp
        if conv_create_time:
            conv_dt = datetime.fromtimestamp(conv_create_time)
        else:
            conv_dt = None

        # Determine best UserID
        best_id = None
        id_source = None

        if extracted_ids:
            # Use extracted ID
            best_id = extracted_ids[0]['id']
            id_source = 'extracted_from_message'

            # Check if extracted ID timestamp matches survey or conversation time
            if 'day' in extracted_ids[0]:
                try:
                    extracted_dt = datetime(
                        extracted_ids[0].get('year', 2024),
                        extracted_ids[0]['month'],
                        extracted_ids[0]['day'],
                        extracted_ids[0].get('hour', 0),
                        extracted_ids[0].get('minute', 0)
                    )
                except ValueError:
                    # Invalid date (e.g., month/day swapped), skip date comparison
                    extracted_dt = None

                if extracted_dt and survey_dt:
                    survey_diff_hours = abs((extracted_dt - survey_dt).total_seconds()) / 3600
                else:
                    survey_diff_hours = None

                if extracted_dt and conv_dt:
                    conv_diff_hours = abs((extracted_dt - conv_dt).total_seconds()) / 3600
                else:
                    conv_diff_hours = None
            else:
                survey_diff_hours = None
                conv_diff_hours = None
        else:
            # No ID in message, use conversation timestamp
            if conv_create_time:
                best_id = generate_id_from_timestamp(conv_create_time)
                id_source = 'generated_from_conv_time'
            elif survey_time:
                best_id = generate_id_from_timestamp(survey_time)
                id_source = 'generated_from_survey_time'
            else:
                best_id = f"UNKNOWN_{row['ResponseId'][-8:]}"
                id_source = 'fallback'

            survey_diff_hours = None
            conv_diff_hours = None

        # Time difference between survey and conversation
        if survey_time and conv_create_time:
            time_diff_hours = abs(survey_time - conv_create_time) / 3600
        else:
            time_diff_hours = None

        results.append({
            'ResponseId': row['ResponseId'],
            'conversation_id': conv_id,
            'old_UserID': row.get('UserID'),
            'new_UserID': best_id,
            'id_source': id_source,
            'first_message': first_msg[:100] if first_msg else None,
            'survey_time': survey_dt,
            'conv_time': conv_dt,
            'survey_conv_diff_hours': time_diff_hours,
            'id_survey_diff_hours': survey_diff_hours,
            'id_conv_diff_hours': conv_diff_hours,
            'extracted_ids_count': len(extracted_ids),
            'current_MatchMethod': row.get('MatchMethod'),
            'data_status': row.get('data_status')
        })

    results_df = pd.DataFrame(results)

    # Statistics
    logger.info("\n=== ID REGENERATION STATISTICS ===")
    logger.info(f"\nID Source Distribution:")
    logger.info(results_df['id_source'].value_counts())

    logger.info(f"\nUserID Changes:")
    changed = results_df[results_df['old_UserID'] != results_df['new_UserID']]
    logger.info(f"Changed: {len(changed)}")
    logger.info(f"Unchanged: {len(results_df) - len(changed)}")

    # Save results
    output_path = PROCESSED_DIR / 'regenerated_ids_analysis.csv'
    results_df.to_csv(output_path, index=False)
    logger.info(f"\nSaved analysis to {output_path}")

    # Show sample changes
    if len(changed) > 0:
        logger.info(f"\n=== SAMPLE ID CHANGES ===")
        for idx, row in changed.head(20).iterrows():
            logger.info(f"\n{row['ResponseId']}:")
            logger.info(f"  Old ID: {row['old_UserID']}")
            logger.info(f"  New ID: {row['new_UserID']}")
            logger.info(f"  Source: {row['id_source']}")
            logger.info(f"  First msg: {row['first_message']}")
            if row['survey_conv_diff_hours']:
                logger.info(f"  Survey-Conv diff: {row['survey_conv_diff_hours']:.1f} hours")

    # Identify potential mismatches
    logger.info("\n=== POTENTIAL MISMATCHES ===")

    # Large time differences between survey and conversation
    large_diff = results_df[results_df['survey_conv_diff_hours'] > 48]
    logger.info(f"\nMatches with >48h survey-conversation diff: {len(large_diff)}")

    if len(large_diff) > 0:
        logger.info("\nSample:")
        for idx, row in large_diff.head(10).iterrows():
            logger.info(f"  {row['ResponseId']}: {row['survey_conv_diff_hours']:.1f}h diff")
            logger.info(f"    ID: {row['new_UserID']}, Method: {row['current_MatchMethod']}")

    # Cases where stated ID time doesn't match either survey or conversation
    potential_wrong_match = results_df[
        (results_df['id_survey_diff_hours'].notna()) &
        (results_df['id_conv_diff_hours'].notna()) &
        (results_df['id_survey_diff_hours'] > 24) &
        (results_df['id_conv_diff_hours'] < 2)
    ]

    logger.info(f"\nPotential wrong matches (stated ID matches conv but not survey): {len(potential_wrong_match)}")

    if len(potential_wrong_match) > 0:
        for idx, row in potential_wrong_match.head(10).iterrows():
            logger.info(f"\n  {row['ResponseId']}:")
            logger.info(f"    Stated ID: {row['new_UserID']}")
            logger.info(f"    ID-Survey diff: {row['id_survey_diff_hours']:.1f}h")
            logger.info(f"    ID-Conv diff: {row['id_conv_diff_hours']:.1f}h")
            logger.info(f"    Msg: {row['first_message']}")

    logger.info("\n" + "=" * 70)
    logger.info("ANALYSIS COMPLETE")
    logger.info("=" * 70)


if __name__ == '__main__':
    main()
