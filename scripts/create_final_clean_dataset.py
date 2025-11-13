#!/usr/bin/env python3
"""
Create Final Clean Dataset for MIT NHH Paper Analysis

This script creates a clean, analysis-ready dataset by:
1. Removing duplicate participant records
2. Filtering to main study (excluding pilot)
3. Keeping one row per participant (best match when multiple exist)
4. Preserving all survey responses (matched and unmatched)
5. Fixing data corruption issues

Output: data/processed/nhh_esperanto_clean_analysis_dataset.csv
"""

import pandas as pd
import numpy as np
from datetime import datetime

def main():
    print("=" * 80)
    print("CREATING FINAL CLEAN DATASET FOR MIT NHH PAPER")
    print("=" * 80)
    print()

    # Load the current finalized dataset
    print("Loading finalized dataset...")
    df = pd.read_csv('data/processed/nhh_esperanto_finalized_dataset.csv')
    print(f"Initial shape: {df.shape}")
    print()

    # === STEP 1: Filter to main study (exclude pilot) ===
    print("STEP 1: Filtering to main study (excluding pilot)")
    print("-" * 80)

    # Keep only main study participants (pilot = 0 or source_survey = 'final')
    # Also keep rows without pilot designation if they have valid survey data
    main_study_mask = (
        (df['pilot'] == 0) |
        (df['source_survey'] == 'final') |
        ((df['pilot'].isna()) & (df['source_survey'].isna()) & (df['ResponseId'].notna()))
    )

    df_main = df[main_study_mask].copy()
    print(f"Rows after filtering to main study: {len(df_main)}")
    print(f"Removed {len(df) - len(df_main)} pilot study rows")
    print()

    # === STEP 2: Remove rows that are purely conversation data without survey ===
    print("STEP 2: Filtering to survey participants")
    print("-" * 80)

    # Keep only rows with valid ResponseId (survey responses)
    df_survey = df_main[df_main['ResponseId'].notna()].copy()
    print(f"Rows with survey responses: {len(df_survey)}")
    print(f"Removed {len(df_main) - len(df_survey)} rows without survey data")
    print()

    # === STEP 3: Handle duplicate participant records ===
    print("STEP 3: Handling duplicate participant records")
    print("-" * 80)

    # Group by ResponseId (unique survey response) and keep the best match
    # Priority:
    # 1. Complete matches (data_status = 'Complete')
    # 2. Recovered matches (data_status = 'Recovered')
    # 3. Duplicate matches (data_status = 'Duplicate')
    # 4. Missing conversation (data_status = 'Missing conversation')
    # 5. Any other row

    def priority_score(row):
        """Assign priority score for keeping the best match per participant"""
        status = row['data_status']
        has_match = row['HasMatch'] == True
        message_count = row['MessageCount'] if pd.notna(row['MessageCount']) else 0

        if status == 'Complete':
            return (4, message_count)
        elif status == 'Recovered':
            return (3, message_count)
        elif status == 'Duplicate' and has_match:
            return (2, message_count)
        elif has_match:
            return (1, message_count)
        else:
            return (0, 0)

    # Add priority score
    df_survey['_priority'] = df_survey.apply(priority_score, axis=1)

    # Sort by ResponseId and priority (descending)
    df_sorted = df_survey.sort_values(['ResponseId', '_priority'], ascending=[True, False])

    # Keep first (highest priority) row for each ResponseId
    df_dedup = df_sorted.drop_duplicates(subset=['ResponseId'], keep='first').copy()

    print(f"Unique survey responses (ResponseId): {df_dedup['ResponseId'].nunique()}")
    print(f"Rows after deduplication: {len(df_dedup)}")
    print(f"Removed {len(df_survey) - len(df_dedup)} duplicate records")
    print()

    # Remove temporary priority column
    df_dedup = df_dedup.drop(columns=['_priority'])

    # === STEP 4: Fix treatment assignment ===
    print("STEP 4: Fixing treatment assignment")
    print("-" * 80)

    # Create treatment_clean from indicator columns if it's missing or NaN
    def assign_treatment(row):
        """Assign treatment based on indicator columns"""
        # If treatment_clean already has a valid value, keep it
        if pd.notna(row['treatment_clean']) and row['treatment_clean'] in ['Control', 'AI-assisted', 'AI-guided']:
            return row['treatment_clean']

        # Otherwise, derive from indicator columns
        if row.get('control') == 1:
            return 'Control'
        elif row.get('ai_assist') == 1:
            return 'AI-assisted'
        elif row.get('ai_guided') == 1:
            return 'AI-guided'
        else:
            # Fallback to 'treat' column if available
            if pd.notna(row.get('treat')):
                return row['treat']
            return np.nan

    df_dedup['treatment_clean'] = df_dedup.apply(assign_treatment, axis=1)

    print("Treatment assignment after fixing:")
    print(df_dedup['treatment_clean'].value_counts(dropna=False))
    print()

    # === STEP 5: Fix conversation duration ===
    print("STEP 5: Fixing conversation duration")
    print("-" * 80)

    # ConversationDuration might be in seconds, need to convert to minutes
    if 'ConversationDuration' in df_dedup.columns:
        # Create ConversationDurationMinutes if not exists or if it's all zeros
        if df_dedup['ConversationDurationMinutes'].max() == 0:
            df_dedup['ConversationDurationMinutes'] = df_dedup['ConversationDuration'] / 60
            print("Converted ConversationDuration (seconds) to minutes")

        # Show statistics
        matched_conv = df_dedup[df_dedup['ConversationDuration'].notna()]
        if len(matched_conv) > 0:
            print(f"Conversation duration statistics (minutes):")
            print(f"  Mean: {matched_conv['ConversationDurationMinutes'].mean():.1f}")
            print(f"  Median: {matched_conv['ConversationDurationMinutes'].median():.1f}")
            print(f"  Min: {matched_conv['ConversationDurationMinutes'].min():.1f}")
            print(f"  Max: {matched_conv['ConversationDurationMinutes'].max():.1f}")
    print()

    # === STEP 6: Verify data integrity ===
    print("STEP 6: Verifying data integrity")
    print("-" * 80)

    print(f"Final dataset shape: {df_dedup.shape}")
    print(f"Unique participants: {df_dedup['ResponseId'].nunique()}")
    print()

    print("Data status breakdown:")
    print(df_dedup['data_status'].value_counts(dropna=False))
    print()

    print("Treatment groups:")
    print(df_dedup['treatment_clean'].value_counts(dropna=False))
    print()

    print("Match status:")
    print(f"Matched (HasMatch=True): {(df_dedup['HasMatch'] == True).sum()}")
    print(f"Unmatched (HasMatch=False): {(df_dedup['HasMatch'] == False).sum()}")
    print(f"Unknown (HasMatch=NaN): {df_dedup['HasMatch'].isna().sum()}")
    print()

    print("Survey completion:")
    # Check for completed surveys (Finished column should be 1 or True)
    if 'Durationinseconds' in df_dedup.columns:
        completed = df_dedup['Durationinseconds'].notna().sum()
        print(f"Completed surveys (has duration): {completed}")
    print()

    # === STEP 7: Create summary statistics ===
    print("STEP 7: Summary statistics")
    print("-" * 80)

    # Conversation metrics for matched participants
    matched = df_dedup[df_dedup['HasMatch'] == True]
    print(f"\nMatched participants: {len(matched)}")
    if len(matched) > 0:
        print(f"  - With message data: {matched['MessageCount'].notna().sum()}")
        print(f"  - Average message count: {matched['MessageCount'].mean():.1f}")
        print(f"  - Average user messages: {matched['UserMessageCount'].mean():.1f}")
        print(f"  - Average conversation duration (min): {matched['ConversationDurationMinutes'].mean():.1f}")

    print(f"\nUnmatched participants: {(df_dedup['HasMatch'] == False).sum()}")
    print(f"Test scores available: {df_dedup['testscore'].notna().sum()}")
    print()

    # === STEP 8: Save clean dataset ===
    print("STEP 8: Saving clean dataset")
    print("-" * 80)

    output_file = 'data/processed/nhh_esperanto_clean_analysis_dataset.csv'
    df_dedup.to_csv(output_file, index=False)
    print(f"✓ Saved to: {output_file}")
    print(f"✓ Final dataset: {len(df_dedup)} rows × {len(df_dedup.columns)} columns")
    print()

    # === STEP 9: Create main study only dataset (exclude all pilot) ===
    print("STEP 9: Creating additional filtered datasets")
    print("-" * 80)

    # Main study only with matched conversations
    df_main_matched = df_dedup[
        (df_dedup['HasMatch'] == True) &
        (df_dedup['MessageCount'].notna())
    ].copy()

    output_matched = 'data/processed/nhh_esperanto_matched_only.csv'
    df_main_matched.to_csv(output_matched, index=False)
    print(f"✓ Matched participants only: {output_matched}")
    print(f"  {len(df_main_matched)} rows")
    print()

    # === FINAL SUMMARY ===
    print("=" * 80)
    print("DATASET CREATION COMPLETE")
    print("=" * 80)
    print()
    print("Output files:")
    print(f"  1. {output_file}")
    print(f"     - All main study participants (matched + unmatched)")
    print(f"     - One row per participant")
    print(f"     - {len(df_dedup)} participants")
    print()
    print(f"  2. {output_matched}")
    print(f"     - Only participants with matched conversations")
    print(f"     - {len(df_main_matched)} participants")
    print()
    print("Next steps:")
    print("  - Use nhh_esperanto_clean_analysis_dataset.csv for full analysis")
    print("  - Use nhh_esperanto_matched_only.csv for conversation-specific analysis")
    print()

if __name__ == "__main__":
    main()
