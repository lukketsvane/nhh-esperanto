#!/usr/bin/env python3
"""
Create final consolidated dataset with all 604 survey entries.
Generates proper IDs for all participants including unmatched ones.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def generate_participant_id(row, idx):
    """Generate a unique participant ID from survey data."""

    # Try to use existing UserID if it's not an AutoID
    if pd.notna(row.get('UserID')) and not str(row['UserID']).startswith('AutoID_'):
        return row['UserID']

    # For unmatched participants, generate ID from survey timestamp
    if pd.notna(row.get('StartDate')):
        try:
            dt = pd.to_datetime(row['StartDate'])
            # Format: DDMMYYYY_HHMM_sequence
            participant_id = f"{dt.day:02d}{dt.month:02d}{dt.year}_{dt.hour:02d}{dt.minute:02d}_{idx}"
            return participant_id
        except Exception as e:
            logger.warning(f"Could not parse StartDate for ResponseId {row['ResponseId']}: {e}")

    # Fallback: Use ResponseId suffix
    response_id = row['ResponseId']
    return f"SURVEY_{response_id[-8:]}"

def create_final_consolidated_dataset():
    """Create the final consolidated dataset with all 604 entries."""

    logger.info("=" * 80)
    logger.info("CREATING FINAL CONSOLIDATED DATASET")
    logger.info("=" * 80)

    # Load current finalized dataset
    logger.info("\nLoading current finalized dataset...")
    df = pd.read_csv('data/processed/nhh_esperanto_finalized_dataset.csv')
    logger.info(f"Loaded {len(df)} entries")
    logger.info(f"  - Matched: {df['HasMatch'].sum()}")
    logger.info(f"  - Unmatched: {(~df['HasMatch']).sum()}")

    # Create clean consolidated dataset
    logger.info("\nGenerating proper participant IDs...")

    # Track sequence numbers for ID generation
    sequence_counter = {}

    def get_participant_id(row):
        """Generate or retrieve participant ID with proper sequencing."""

        # If matched and has good UserID, use it
        if row['HasMatch'] and pd.notna(row.get('UserID')) and not str(row['UserID']).startswith('AutoID_'):
            return row['UserID']

        # For unmatched or AutoID, generate from survey timestamp
        if pd.notna(row.get('StartDate')):
            try:
                dt = pd.to_datetime(row['StartDate'])
                base_id = f"{dt.day:02d}{dt.month:02d}{dt.year}_{dt.hour:02d}{dt.minute:02d}"

                # Get next sequence number for this timestamp
                if base_id not in sequence_counter:
                    sequence_counter[base_id] = 1
                else:
                    sequence_counter[base_id] += 1

                return f"{base_id}_{sequence_counter[base_id]}"
            except Exception as e:
                logger.warning(f"Could not parse StartDate for ResponseId {row['ResponseId']}: {e}")

        # Fallback: Use ResponseId suffix
        response_id = row['ResponseId']
        return f"SURVEY_{response_id[-8:]}"

    # Generate ParticipantID for all entries
    df['ParticipantID'] = df.apply(get_participant_id, axis=1)

    # Update UserID to match ParticipantID
    df['UserID'] = df['ParticipantID']

    logger.info(f"\nGenerated {df['ParticipantID'].nunique()} unique participant IDs")

    # Sort by treatment, match status, then timestamp
    logger.info("\nSorting dataset...")
    df = df.sort_values(['treatment_clean', 'HasMatch', 'StartDate'], ascending=[True, False, True])

    # Reset final_id to be sequential
    df['final_id'] = range(1, len(df) + 1)

    # Create consolidated dataset with key columns first
    logger.info("\nOrganizing columns...")

    key_columns = [
        'final_id',
        'ParticipantID',
        'ResponseId',
        'HasMatch',
        'treatment_clean',
        'treatment',
        'data_status',

        # Demographics
        'gender',
        'female',
        'age',
        'yearincollege',
        'faculty',
        'gpa',
        'highgpa',

        # AI usage
        'AIfamiliar',
        'AIsubscription',
        'AIadoption',
        'AIpaid',

        # Test score
        'testscore',
        'testscore_lb',
        'testscore_ub',
        'topscore',
        'lowscore',

        # Survey indices
        'index_confidence',
        'index_motivation',
        'index_complement',
        'index_cheating',

        # Conversation data
        'conversation_id',
        'create_time',
        'MessageCount',
        'UserMessageCount',
        'AIMessageCount',
        'ConversationDurationMinutes',
        'AverageUserMessageLength',
        'AverageAIMessageLength',
        'MessageRatio',

        # Matching metadata
        'MatchMethod',
        'UserID_Source',
        'match_confidence',
        'timestamp_diff_minutes',

        # Timestamps
        'StartDate',
        'EndDate',
        'start_time_unix',
        'end_time_unix',
        'Session',
        'session',
    ]

    # Add remaining columns
    other_columns = [col for col in df.columns if col not in key_columns and col != 'UserID']
    final_column_order = key_columns + other_columns

    # Select columns that exist
    final_columns = [col for col in final_column_order if col in df.columns]
    df_consolidated = df[final_columns].copy()

    # Save consolidated dataset
    output_path = 'data/processed/nhh_esperanto_final_consolidated_dataset.csv'
    logger.info(f"\nSaving consolidated dataset to {output_path}")
    df_consolidated.to_csv(output_path, index=False)

    # Create summary statistics
    logger.info("\n" + "=" * 80)
    logger.info("FINAL CONSOLIDATED DATASET SUMMARY")
    logger.info("=" * 80)

    logger.info(f"\nTotal entries: {len(df_consolidated)}")
    logger.info(f"Unique participants: {df_consolidated['ParticipantID'].nunique()}")

    logger.info("\n--- By Match Status ---")
    logger.info(f"Matched (with conversation data): {df_consolidated['HasMatch'].sum()} ({df_consolidated['HasMatch'].sum()/len(df_consolidated)*100:.1f}%)")
    logger.info(f"Unmatched (no conversation data): {(~df_consolidated['HasMatch']).sum()} ({(~df_consolidated['HasMatch']).sum()/len(df_consolidated)*100:.1f}%)")

    logger.info("\n--- By Treatment Group ---")
    treatment_counts = df_consolidated['treatment_clean'].value_counts()
    for treatment, count in treatment_counts.items():
        matched_count = df_consolidated[(df_consolidated['treatment_clean'] == treatment) & (df_consolidated['HasMatch'])].shape[0]
        logger.info(f"{treatment}: {count} total ({matched_count} matched, {count-matched_count} unmatched)")

    logger.info("\n--- By Data Status ---")
    status_counts = df_consolidated['data_status'].value_counts()
    for status, count in status_counts.items():
        logger.info(f"{status}: {count}")

    logger.info("\n--- Match Methods (for matched entries) ---")
    match_methods = df_consolidated[df_consolidated['HasMatch']]['MatchMethod'].value_counts()
    for method, count in match_methods.items():
        logger.info(f"{method}: {count}")

    # Save summary to file
    summary_path = 'data/processed/DATASET_SUMMARY.txt'
    with open(summary_path, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("NHH ESPERANTO FINAL CONSOLIDATED DATASET SUMMARY\n")
        f.write("=" * 80 + "\n")
        f.write(f"\nDataset: {output_path}\n")
        f.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"\nTotal entries: {len(df_consolidated)}\n")
        f.write(f"Unique participants: {df_consolidated['ParticipantID'].nunique()}\n")
        f.write(f"\nMatched (with conversation data): {df_consolidated['HasMatch'].sum()} ({df_consolidated['HasMatch'].sum()/len(df_consolidated)*100:.1f}%)\n")
        f.write(f"Unmatched (no conversation data): {(~df_consolidated['HasMatch']).sum()} ({(~df_consolidated['HasMatch']).sum()/len(df_consolidated)*100:.1f}%)\n")
        f.write("\n" + "-" * 80 + "\n")
        f.write("TREATMENT GROUPS\n")
        f.write("-" * 80 + "\n")
        for treatment, count in treatment_counts.items():
            matched_count = df_consolidated[(df_consolidated['treatment_clean'] == treatment) & (df_consolidated['HasMatch'])].shape[0]
            f.write(f"\n{treatment}:\n")
            f.write(f"  Total: {count}\n")
            f.write(f"  Matched: {matched_count}\n")
            f.write(f"  Unmatched: {count-matched_count}\n")

    logger.info(f"\nSummary saved to: {summary_path}")
    logger.info("\n" + "=" * 80)
    logger.info("DATASET CREATION COMPLETE!")
    logger.info("=" * 80)
    logger.info(f"\nFinal dataset: {output_path}")
    logger.info(f"Total entries: {len(df_consolidated)} (604 as expected)")

    return df_consolidated

if __name__ == '__main__':
    create_final_consolidated_dataset()
