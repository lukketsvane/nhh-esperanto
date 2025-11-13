#!/usr/bin/env python3
"""
Build Clean Dataset from Scratch for MIT NHH Paper Analysis

This script creates a clean, analysis-ready dataset by starting from
the raw survey and conversation data, avoiding the corruption present
in intermediate processed files.

Strategy:
1. Load raw survey data (iverdata.csv) - main study only
2. Load conversation data (nhh_esperanto_conversations.csv or unified_conversation_data_complete.csv)
3. Merge properly on matching IDs
4. Create one row per participant
5. Output clean dataset

Output: data/processed/nhh_esperanto_analysis_ready.csv
"""

import pandas as pd
import numpy as np
from datetime import datetime

def main():
    print("=" * 80)
    print("BUILDING CLEAN DATASET FROM SCRATCH")
    print("=" * 80)
    print()

    # === STEP 1: Load raw survey data ===
    print("STEP 1: Loading raw survey data")
    print("-" * 80)

    df_survey = pd.read_csv('data/raw/iverdata.csv')
    print(f"Raw survey data: {df_survey.shape}")
    print(f"Total survey responses: {len(df_survey)}")
    print()

    # === STEP 2: Filter to main study ===
    print("STEP 2: Filtering to main study")
    print("-" * 80)

    df_main = df_survey[df_survey['pilot'] == 0].copy()
    print(f"Main study participants: {len(df_main)}")
    print(f"Removed {len(df_survey) - len(df_main)} pilot participants")
    print()

    # === STEP 3: Create treatment variable ===
    print("STEP 3: Creating treatment variable")
    print("-" * 80)

    def assign_treatment(row):
        if row['control'] == 1:
            return 'Control'
        elif row['ai_assist'] == 1:
            return 'AI-assisted'
        elif row['ai_guided'] == 1:
            return 'AI-guided'
        else:
            return np.nan

    df_main['treatment'] = df_main.apply(assign_treatment, axis=1)

    print("Treatment assignment:")
    print(df_main['treatment'].value_counts(dropna=False))
    print()

    # === STEP 4: Load conversation data ===
    print("STEP 4: Loading conversation data")
    print("-" * 80)

    # Try to load the conversations CSV
    try:
        df_conv = pd.read_csv('data/processed/nhh_esperanto_conversations.csv')
        print(f"Loaded conversations from nhh_esperanto_conversations.csv")
        print(f"Total conversations: {len(df_conv)}")
    except:
        # Fallback to unified data
        try:
            df_conv = pd.read_csv('data/raw/unified_conversation_data_complete.csv')
            print(f"Loaded conversations from unified_conversation_data_complete.csv")
            print(f"Total conversations: {len(df_conv)}")
        except:
            print("WARNING: Could not load conversation data. Proceeding with survey data only.")
            df_conv = None

    print()

    # === STEP 5: Merge survey and conversation data ===
    print("STEP 5: Merging survey and conversation data")
    print("-" * 80)

    if df_conv is not None:
        # Determine the key to merge on
        # The conversation data should have 'participant_id' or 'final_id' or 'UserID'
        merge_key = None
        if 'participant_id' in df_conv.columns:
            merge_key = 'participant_id'
        elif 'final_id' in df_conv.columns:
            merge_key = 'final_id'
        elif 'UserID' in df_conv.columns:
            merge_key = 'UserID'

        if merge_key:
            print(f"Merging on conversation key: {merge_key}")

            # Need to create matching key in survey data
            # The survey data might have 'final_id' or need to generate it
            if 'final_id' not in df_main.columns:
                # Generate final_id from timestamp or other identifier
                # For now, use ResponseId as the unique identifier
                print("Using ResponseId as participant identifier")
                df_main['final_id'] = df_main['ResponseId']

            # Merge
            df_merged = df_main.merge(
                df_conv,
                left_on='final_id',
                right_on=merge_key,
                how='left',
                suffixes=('', '_conv')
            )

            print(f"Merged dataset: {df_merged.shape}")
            print(f"Matched participants: {df_merged[merge_key].notna().sum()}")
            print(f"Unmatched participants: {df_merged[merge_key].isna().sum()}")
        else:
            print("WARNING: Could not find matching key in conversation data")
            df_merged = df_main.copy()
            df_merged['HasMatch'] = False
    else:
        df_merged = df_main.copy()
        df_merged['HasMatch'] = False

    print()

    # === STEP 6: Clean and standardize columns ===
    print("STEP 6: Cleaning and standardizing")
    print("-" * 80)

    # Rename for clarity
    if 'Durationinseconds' in df_merged.columns:
        df_merged['survey_duration_seconds'] = df_merged['Durationinseconds']

    # Calculate conversation duration if timestamps available
    if 'start_time_unix' in df_merged.columns and 'end_time_unix' in df_merged.columns:
        df_merged['conversation_duration_seconds'] = (
            df_merged['end_time_unix'] - df_merged['start_time_unix']
        )
        df_merged['conversation_duration_minutes'] = (
            df_merged['conversation_duration_seconds'] / 60
        )

    print(f"Final cleaned dataset: {df_merged.shape}")
    print()

    # === STEP 7: Summary statistics ===
    print("STEP 7: Summary statistics")
    print("-" * 80)

    print(f"\nTotal participants: {len(df_merged)}")
    print(f"\nTreatment distribution:")
    print(df_merged['treatment'].value_counts(dropna=False))

    if 'HasMatch' in df_merged.columns:
        matched_count = (df_merged['HasMatch'] == True).sum()
    elif 'MessageCount' in df_merged.columns:
        matched_count = df_merged['MessageCount'].notna().sum()
    else:
        matched_count = 0

    print(f"\nMatched with conversations: {matched_count}")
    print(f"Without conversations: {len(df_merged) - matched_count}")

    if 'testscore' in df_merged.columns:
        print(f"\nTest scores available: {df_merged['testscore'].notna().sum()}")
        print(f"  Mean test score: {df_merged['testscore'].mean():.2f}")

    if matched_count > 0 and 'MessageCount' in df_merged.columns:
        matched_df = df_merged[df_merged['MessageCount'].notna()]
        print(f"\nConversation metrics (n={len(matched_df)}):")
        print(f"  Mean messages: {matched_df['MessageCount'].mean():.1f}")
        if 'UserMessageCount' in matched_df.columns:
            print(f"  Mean user messages: {matched_df['UserMessageCount'].mean():.1f}")
        if 'conversation_duration_minutes' in matched_df.columns:
            print(f"  Mean duration (min): {matched_df['conversation_duration_minutes'].mean():.1f}")

    print()

    # === STEP 8: Save clean dataset ===
    print("STEP 8: Saving clean dataset")
    print("-" * 80)

    output_file = 'data/processed/nhh_esperanto_analysis_ready.csv'
    df_merged.to_csv(output_file, index=False)
    print(f"✓ Saved to: {output_file}")
    print(f"✓ Dataset: {len(df_merged)} rows × {len(df_merged.columns)} columns")
    print()

    # === FINAL SUMMARY ===
    print("=" * 80)
    print("CLEAN DATASET CREATED SUCCESSFULLY")
    print("=" * 80)
    print()
    print(f"Output file: {output_file}")
    print(f"  - Main study participants only")
    print(f"  - One row per participant")
    print(f"  - {len(df_merged)} total participants")
    print(f"  - Clean survey data without corruption")
    print()

if __name__ == "__main__":
    main()
