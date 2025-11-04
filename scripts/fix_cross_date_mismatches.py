#!/usr/bin/env python3
"""
Fix cross-date mismatches by reassigning conversations to better-matching surveys.
"""

import pandas as pd
from datetime import datetime
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent / 'data'
RAW_DIR = DATA_DIR / 'raw'
PROCESSED_DIR = DATA_DIR / 'processed'


def main():
    logger.info("=" * 70)
    logger.info("FIXING CROSS-DATE MISMATCHES")
    logger.info("=" * 70)

    # Load data
    finalized_df = pd.read_csv(PROCESSED_DIR / 'nhh_esperanto_finalized_dataset.csv')
    conv_df = pd.read_csv(RAW_DIR / 'unified_conversation_data_complete.csv')

    # Get conversation dates
    conv_dates = {}
    for conv_id in conv_df['conversation_id'].unique():
        conv_msgs = conv_df[conv_df['conversation_id'] == conv_id]
        create_time_str = str(conv_msgs.iloc[0]['create_time'])

        try:
            if '.' in create_time_str and len(create_time_str) > 15:
                dt = pd.to_datetime(create_time_str)
                create_time = dt.timestamp()
            else:
                create_time = float(create_time_str)

            dt = datetime.fromtimestamp(create_time)
            conv_dates[conv_id] = {
                'timestamp': create_time,
                'date': dt.strftime('%Y-%m-%d')
            }
        except:
            pass

    # Get survey dates
    finalized_df['survey_date'] = pd.to_datetime(finalized_df['StartDate']).dt.strftime('%Y-%m-%d')

    # Find cross-date matches
    matched = finalized_df[finalized_df['conversation_id'].notna()].copy()

    cross_date_matches = []
    for idx, row in matched.iterrows():
        conv_id = row['conversation_id']

        if conv_id not in conv_dates:
            continue

        survey_date = row['survey_date']
        conv_date = conv_dates[conv_id]['date']

        if survey_date != conv_date:
            cross_date_matches.append({
                'index': idx,
                'ResponseId': row['ResponseId'],
                'conversation_id': conv_id,
                'survey_date': survey_date,
                'conv_date': conv_date,
                'conv_timestamp': conv_dates[conv_id]['timestamp'],
                'survey_timestamp': row['start_time_unix'],
                'time_diff_hours': abs(row['start_time_unix'] - conv_dates[conv_id]['timestamp']) / 3600
            })

    logger.info(f"Found {len(cross_date_matches)} cross-date mismatches")

    if not cross_date_matches:
        logger.info("No cross-date mismatches to fix!")
        return

    # For each mismatch, try to find a better survey match from the conversation's date
    fixes = []
    unmatched = finalized_df[finalized_df['conversation_id'].isna()].copy()
    unmatched['start_time_unix'] = pd.to_numeric(unmatched['start_time_unix'], errors='coerce')

    for mismatch in cross_date_matches:
        conv_id = mismatch['conversation_id']
        conv_date = mismatch['conv_date']
        conv_timestamp = mismatch['conv_timestamp']

        # Find unmatched surveys from the conversation's date
        same_date_unmatched = unmatched[unmatched['survey_date'] == conv_date]

        if not same_date_unmatched.empty:
            # Find closest by time
            same_date_unmatched['time_diff'] = abs(same_date_unmatched['start_time_unix'] - conv_timestamp)
            best_match = same_date_unmatched.nsmallest(1, 'time_diff').iloc[0]

            # Only fix if the new match is significantly better (within 12 hours)
            if best_match['time_diff'] / 3600 <= 12:
                fixes.append({
                    'conversation_id': conv_id,
                    'old_ResponseId': mismatch['ResponseId'],
                    'old_survey_date': mismatch['survey_date'],
                    'old_time_diff': mismatch['time_diff_hours'],
                    'new_ResponseId': best_match['ResponseId'],
                    'new_survey_date': conv_date,
                    'new_time_diff': best_match['time_diff'] / 3600,
                    'improvement': mismatch['time_diff_hours'] - (best_match['time_diff'] / 3600)
                })

                logger.info(f"✓ Can fix {conv_id[:20]}...")
                logger.info(f"  Old: {mismatch['ResponseId']} ({mismatch['survey_date']}, {mismatch['time_diff_hours']:.1f}h diff)")
                logger.info(f"  New: {best_match['ResponseId']} ({conv_date}, {best_match['time_diff'] / 3600:.1f}h diff)")
                logger.info(f"  Improvement: {fixes[-1]['improvement']:.1f} hours")

    logger.info(f"\n=== FIXABLE MISMATCHES ===")
    logger.info(f"Total: {len(fixes)}")

    if fixes:
        # Apply fixes
        finalized_updated = finalized_df.copy()

        for fix in fixes:
            # Unmatch the old survey
            old_mask = finalized_updated['ResponseId'] == fix['old_ResponseId']
            finalized_updated.loc[old_mask, 'conversation_id'] = None
            finalized_updated.loc[old_mask, 'UserID'] = f"AutoID_{fix['old_ResponseId'][-8:]}"
            finalized_updated.loc[old_mask, 'MatchMethod'] = None
            finalized_updated.loc[old_mask, 'HasMatch'] = False
            finalized_updated.loc[old_mask, 'data_status'] = 'Missing conversation'

            # Match the new survey
            new_mask = finalized_updated['ResponseId'] == fix['new_ResponseId']
            finalized_updated.loc[new_mask, 'conversation_id'] = fix['conversation_id']
            finalized_updated.loc[new_mask, 'MatchMethod'] = 'FixedCrossDate'
            finalized_updated.loc[new_mask, 'HasMatch'] = True
            finalized_updated.loc[new_mask, 'data_status'] = 'Fixed'

        # Save
        output_path = PROCESSED_DIR / 'nhh_esperanto_finalized_dataset_fixed.csv'
        finalized_updated.to_csv(output_path, index=False)
        logger.info(f"\nSaved fixed dataset to {output_path}")

        # Save fix details
        fixes_df = pd.DataFrame(fixes)
        fixes_path = PROCESSED_DIR / 'cross_date_fixes.csv'
        fixes_df.to_csv(fixes_path, index=False)
        logger.info(f"Saved fix details to {fixes_path}")

        # Statistics
        logger.info(f"\n=== STATISTICS ===")
        logger.info(f"Fixes applied: {len(fixes)}")
        logger.info(f"Average improvement: {fixes_df['improvement'].mean():.1f} hours")
        logger.info(f"Total improvement: {fixes_df['improvement'].sum():.1f} hours")

    logger.info("\n" + "=" * 70)
    logger.info("CROSS-DATE FIX COMPLETE")
    logger.info("=" * 70)


if __name__ == '__main__':
    main()
