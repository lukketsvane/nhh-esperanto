#!/usr/bin/env python3
"""
Apply corrected UserIDs to the finalized dataset.

This script updates the dataset with improved UserIDs based on:
1. Extracted IDs from conversation messages
2. Generated IDs from conversation timestamps (for those without stated IDs)
"""

import pandas as pd
import logging
from pathlib import Path
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# File paths
DATA_DIR = Path(__file__).parent.parent / 'data'
PROCESSED_DIR = DATA_DIR / 'processed'


def main():
    """Main execution."""
    logger.info("=" * 70)
    logger.info("APPLYING CORRECTED IDs TO DATASET")
    logger.info("=" * 70)

    # Load the regenerated IDs analysis
    analysis_df = pd.read_csv(PROCESSED_DIR / 'regenerated_ids_analysis.csv')
    logger.info(f"Loaded {len(analysis_df)} regenerated IDs")

    # Load the finalized dataset
    finalized_df = pd.read_csv(PROCESSED_DIR / 'nhh_esperanto_finalized_dataset.csv')
    logger.info(f"Loaded {len(finalized_df)} survey responses")

    # Create a mapping from ResponseId to new_UserID
    id_mapping = dict(zip(analysis_df['ResponseId'], analysis_df['new_UserID']))

    logger.info(f"\nUpdating UserIDs for {len(id_mapping)} matched entries...")

    # Track changes
    updated_count = 0
    unchanged_count = 0

    for idx, row in finalized_df.iterrows():
        response_id = row['ResponseId']

        if response_id in id_mapping:
            old_id = row.get('UserID')
            new_id = id_mapping[response_id]

            if old_id != new_id:
                finalized_df.at[idx, 'UserID'] = new_id
                finalized_df.at[idx, 'UserID_Source'] = analysis_df[
                    analysis_df['ResponseId'] == response_id
                ]['id_source'].iloc[0]
                updated_count += 1
            else:
                unchanged_count += 1

    logger.info(f"\nUpdates:")
    logger.info(f"  Changed: {updated_count}")
    logger.info(f"  Unchanged: {unchanged_count}")

    # Save updated dataset
    output_path = PROCESSED_DIR / 'nhh_esperanto_finalized_dataset_updated_ids.csv'
    finalized_df.to_csv(output_path, index=False)
    logger.info(f"\nSaved updated dataset to {output_path}")

    # Also update the original file (backup first)
    backup_path = PROCESSED_DIR / f'nhh_esperanto_finalized_dataset_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    original_df = pd.read_csv(PROCESSED_DIR / 'nhh_esperanto_finalized_dataset.csv')
    original_df.to_csv(backup_path, index=False)
    logger.info(f"Created backup at {backup_path}")

    finalized_df.to_csv(PROCESSED_DIR / 'nhh_esperanto_finalized_dataset.csv', index=False)
    logger.info(f"Updated original dataset at nhh_esperanto_finalized_dataset.csv")

    # Show statistics
    logger.info("\n=== UPDATED DATASET STATISTICS ===")
    logger.info(f"\nUserID Source Distribution:")
    if 'UserID_Source' in finalized_df.columns:
        logger.info(finalized_df['UserID_Source'].value_counts())

    # Show sample updated IDs
    updated_samples = finalized_df[finalized_df['ResponseId'].isin(list(id_mapping.keys())[:10])]
    logger.info(f"\n=== SAMPLE UPDATED ENTRIES ===")
    for idx, row in updated_samples.iterrows():
        logger.info(f"\n{row['ResponseId']}:")
        logger.info(f"  UserID: {row['UserID']}")
        logger.info(f"  Source: {row.get('UserID_Source', 'N/A')}")
        logger.info(f"  Match Method: {row.get('MatchMethod', 'N/A')}")
        logger.info(f"  Has Match: {row.get('HasMatch', 'N/A')}")

    logger.info("\n" + "=" * 70)
    logger.info("ID UPDATE COMPLETE")
    logger.info("=" * 70)


if __name__ == '__main__':
    main()
