#!/usr/bin/env python3
"""
Comprehensive rematching script using unified unix timestamps.

This script:
1. Ensures all timestamps are in unix format
2. Generates IDs for all participants based on timestamps
3. Re-evaluates all matches to find optimal assignments
4. Attempts to reassign poor matches to unmatched participants
"""

import pandas as pd
import numpy as np
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

def parse_survey_timestamp(date_str):
    """Convert survey StartDate to unix timestamp."""
    try:
        # Format: "11/28/2024 2:57" or "12/3/2024 7:53"
        dt = datetime.strptime(date_str, '%m/%d/%Y %H:%M')
        return dt.timestamp()
    except Exception as e:
        logger.warning(f"Could not parse date '{date_str}': {e}")
        return None


def generate_user_id(timestamp):
    """Generate a UserID from a unix timestamp."""
    if pd.isna(timestamp):
        return None

    dt = datetime.fromtimestamp(timestamp)
    return f"{dt.day:02d}{dt.month:02d}{dt.year}_{dt.hour:02d}{dt.minute:02d}_Generated"


def load_and_prepare_data():
    """Load all data and ensure timestamps are in unix format."""
    logger.info("Loading data files...")

    # Load survey data
    finalized_df = pd.read_csv(PROCESSED_DIR / 'nhh_esperanto_finalized_dataset.csv')
    conv_df = pd.read_csv(RAW_DIR / 'unified_conversation_data.csv')

    logger.info(f"Loaded {len(finalized_df)} survey responses")
    logger.info(f"Loaded {len(conv_df)} conversation messages")

    # Ensure start_time_unix exists, create if needed
    if 'start_time_unix' not in finalized_df.columns or finalized_df['start_time_unix'].isna().any():
        logger.info("Converting StartDate to unix timestamps...")
        finalized_df['start_time_unix'] = finalized_df['StartDate'].apply(parse_survey_timestamp)
    else:
        # Ensure it's numeric
        finalized_df['start_time_unix'] = pd.to_numeric(finalized_df['start_time_unix'], errors='coerce')

    # Ensure conversation create_time is numeric
    conv_df['create_time'] = pd.to_numeric(conv_df['create_time'], errors='coerce')

    logger.info(f"Survey timestamps: {finalized_df['start_time_unix'].notna().sum()} valid")
    logger.info(f"Conversation timestamps: {conv_df['create_time'].notna().sum()} valid")

    return finalized_df, conv_df


def get_conversation_details(conv_id, conv_df):
    """Get details about a conversation."""
    conv_subset = conv_df[conv_df['conversation_id'] == conv_id]

    if conv_subset.empty:
        return None

    create_time = float(conv_subset['create_time'].iloc[0])

    # Get first user message
    user_msgs = conv_subset[conv_subset['author_role'] == 'user']
    first_user_msg = None
    if not user_msgs.empty:
        first_user_msg = str(user_msgs.iloc[0]['message_content']).strip("[]'\"")

    # Count messages
    total_msgs = len(conv_subset)
    user_msg_count = len(user_msgs)

    return {
        'conversation_id': conv_id,
        'create_time': create_time,
        'create_datetime': datetime.fromtimestamp(create_time),
        'first_user_message': first_user_msg,
        'total_messages': total_msgs,
        'user_message_count': user_msg_count,
        'is_valid': first_user_msg and first_user_msg.lower() != 'login' and user_msg_count > 0
    }


def analyze_current_matches(finalized_df, conv_df):
    """Analyze quality of current matches."""
    logger.info("\n=== ANALYZING CURRENT MATCHES ===")

    matched = finalized_df[finalized_df['conversation_id'].notna()].copy()

    # Calculate time differences
    matched_details = []
    for idx, row in matched.iterrows():
        conv_details = get_conversation_details(row['conversation_id'], conv_df)
        if conv_details:
            time_diff = abs(row['start_time_unix'] - conv_details['create_time'])
            time_diff_minutes = time_diff / 60
            time_diff_hours = time_diff / 3600

            matched_details.append({
                'ResponseId': row['ResponseId'],
                'conversation_id': row['conversation_id'],
                'survey_time': row['start_time_unix'],
                'conv_time': conv_details['create_time'],
                'time_diff_seconds': time_diff,
                'time_diff_minutes': time_diff_minutes,
                'time_diff_hours': time_diff_hours,
                'current_UserID': row.get('UserID'),
                'current_MatchMethod': row.get('MatchMethod'),
                'data_status': row.get('data_status'),
                'is_duplicate': row.get('is_duplicate'),
                'first_message': conv_details['first_user_message']
            })

    matched_df = pd.DataFrame(matched_details)

    # Statistics
    logger.info(f"\nTotal matched: {len(matched_df)}")
    logger.info(f"Average time diff: {matched_df['time_diff_hours'].mean():.2f} hours")
    logger.info(f"Median time diff: {matched_df['time_diff_hours'].median():.2f} hours")
    logger.info(f"Max time diff: {matched_df['time_diff_hours'].max():.2f} hours")

    # Show matches with very large time differences
    poor_matches = matched_df[matched_df['time_diff_hours'] > 24]
    logger.info(f"\nMatches with >24 hour time diff: {len(poor_matches)}")

    if len(poor_matches) > 0:
        logger.info("\nSample poor matches:")
        for idx, row in poor_matches.head(10).iterrows():
            logger.info(f"  {row['ResponseId']}: {row['time_diff_hours']:.1f} hours diff")
            logger.info(f"    Survey: {datetime.fromtimestamp(row['survey_time'])}")
            logger.info(f"    Conv: {datetime.fromtimestamp(row['conv_time'])}")
            logger.info(f"    First msg: {row['first_message'][:60] if row['first_message'] else 'N/A'}")

    return matched_df


def create_optimal_matching(finalized_df, conv_df):
    """
    Create optimal matching using Hungarian algorithm or greedy approach.
    """
    logger.info("\n=== CREATING OPTIMAL MATCHING ===")

    # Get all survey responses with timestamps
    surveys = finalized_df[finalized_df['start_time_unix'].notna()].copy()
    logger.info(f"Surveys with timestamps: {len(surveys)}")

    # Get all valid conversations
    all_conv_ids = conv_df['conversation_id'].unique()
    valid_convs = []

    for conv_id in all_conv_ids:
        details = get_conversation_details(conv_id, conv_df)
        if details and details['is_valid']:
            valid_convs.append(details)

    logger.info(f"Valid conversations: {len(valid_convs)}")

    # Create matches using greedy approach (closest timestamp)
    # Sort surveys by timestamp
    surveys = surveys.sort_values('start_time_unix')

    # Sort conversations by timestamp
    conv_times = {c['conversation_id']: c['create_time'] for c in valid_convs}
    sorted_conv_ids = sorted(conv_times.keys(), key=lambda x: conv_times[x])

    # Greedy matching - for each survey, find closest available conversation
    matches = []
    available_convs = set(sorted_conv_ids)

    MAX_TIME_DIFF = 7 * 24 * 60 * 60  # 7 days in seconds

    for idx, survey in surveys.iterrows():
        survey_time = survey['start_time_unix']

        # Find closest conversation
        best_conv_id = None
        best_time_diff = float('inf')

        for conv_id in available_convs:
            conv_time = conv_times[conv_id]
            time_diff = abs(survey_time - conv_time)

            if time_diff < best_time_diff and time_diff <= MAX_TIME_DIFF:
                best_time_diff = time_diff
                best_conv_id = conv_id

        if best_conv_id:
            # Generate UserID
            user_id = generate_user_id(survey_time)

            matches.append({
                'ResponseId': survey['ResponseId'],
                'conversation_id': best_conv_id,
                'survey_time': survey_time,
                'conv_time': conv_times[best_conv_id],
                'time_diff_seconds': best_time_diff,
                'time_diff_minutes': best_time_diff / 60,
                'time_diff_hours': best_time_diff / 3600,
                'UserID': user_id,
                'MatchMethod': 'OptimalTimestamp',
                'match_confidence': max(0, 100 - (best_time_diff / 3600))  # Decrease with time
            })

            # Remove from available
            available_convs.remove(best_conv_id)

    logger.info(f"\nNew matches created: {len(matches)}")
    logger.info(f"Remaining unmatched surveys: {len(surveys) - len(matches)}")
    logger.info(f"Remaining unmatched conversations: {len(available_convs)}")

    matches_df = pd.DataFrame(matches)

    if not matches_df.empty:
        logger.info(f"\nNew matching statistics:")
        logger.info(f"Average time diff: {matches_df['time_diff_hours'].mean():.2f} hours")
        logger.info(f"Median time diff: {matches_df['time_diff_hours'].median():.2f} hours")
        logger.info(f"Max time diff: {matches_df['time_diff_hours'].max():.2f} hours")

    return matches_df, available_convs


def compare_matchings(current_matched_df, new_matches_df):
    """Compare current matching with new optimal matching."""
    logger.info("\n=== COMPARING MATCHINGS ===")

    # Find differences
    current_pairs = set(zip(current_matched_df['ResponseId'], current_matched_df['conversation_id']))
    new_pairs = set(zip(new_matches_df['ResponseId'], new_matches_df['conversation_id']))

    same_matches = current_pairs & new_pairs
    different_matches = (current_pairs | new_pairs) - same_matches

    logger.info(f"Identical matches: {len(same_matches)}")
    logger.info(f"Different matches: {len(different_matches)}")

    # Show improvement in time differences
    if len(same_matches) > 0:
        # For identical matches, compare time diff
        logger.info(f"\nOverall quality comparison:")
        logger.info(f"Current avg time diff: {current_matched_df['time_diff_hours'].mean():.2f} hours")
        logger.info(f"New avg time diff: {new_matches_df['time_diff_hours'].mean():.2f} hours")


def main():
    """Main execution."""
    logger.info("=" * 70)
    logger.info("COMPREHENSIVE REMATCHING WITH UNIX TIMESTAMPS")
    logger.info("=" * 70)

    # Load data
    finalized_df, conv_df = load_and_prepare_data()

    # Analyze current matches
    current_matched_df = analyze_current_matches(finalized_df, conv_df)

    # Create optimal matching
    new_matches_df, unmatched_convs = create_optimal_matching(finalized_df, conv_df)

    # Compare
    if not new_matches_df.empty:
        compare_matchings(current_matched_df, new_matches_df)

    # Save new matches
    output_path = PROCESSED_DIR / 'optimal_matches.csv'
    new_matches_df.to_csv(output_path, index=False)
    logger.info(f"\nSaved optimal matches to {output_path}")

    # Save unmatched conversation IDs
    if unmatched_convs:
        unmatched_df = pd.DataFrame({'conversation_id': list(unmatched_convs)})
        unmatched_path = PROCESSED_DIR / 'unmatched_conversations_after_optimal.csv'
        unmatched_df.to_csv(unmatched_path, index=False)
        logger.info(f"Saved {len(unmatched_convs)} unmatched conversation IDs to {unmatched_path}")

    logger.info("\n" + "=" * 70)
    logger.info("REMATCHING COMPLETE")
    logger.info("=" * 70)


if __name__ == '__main__':
    main()
