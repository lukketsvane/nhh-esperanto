#!/usr/bin/env python3
"""
Create Clean Analysis Dataset v2

Strategy:
1. Load raw survey data (iverdata.csv) - CLEAN survey responses
2. Load finalized dataset - for matching information and conversation metrics
3. Merge them, keeping clean survey data and conversation metrics
4. Filter to main study, deduplicate, create final dataset

Output: data/processed/nhh_esperanto_final_analysis.csv
"""

import pandas as pd
import numpy as np

def main():
    print("=" * 80)
    print("CREATING CLEAN ANALYSIS DATASET V2")
    print("=" * 80)
    print()

    # === STEP 1: Load raw survey data (CLEAN) ===
    print("STEP 1: Loading raw survey data")
    print("-" * 80)

    df_survey_raw = pd.read_csv('data/raw/iverdata.csv')
    print(f"Raw survey data: {df_survey_raw.shape}")
    print(f"Columns: {len(df_survey_raw.columns)}")
    print()

    # === STEP 2: Load finalized dataset (for matching info) ===
    print("STEP 2: Loading finalized dataset for matching information")
    print("-" * 80)

    df_finalized = pd.read_csv('data/processed/nhh_esperanto_finalized_dataset.csv')
    print(f"Finalized dataset: {df_finalized.shape}")
    print()

    # === STEP 3: Extract conversation columns from finalized ===
    print("STEP 3: Extracting conversation metrics")
    print("-" * 80)

    # Conversation-related columns to keep from finalized dataset
    conv_cols = [
        'ResponseId',  # Key for merging
        'final_id',
        'participant_id',
        'conversation_id',
        'UserID',
        'HasMatch',
        'MatchMethod',
        'MessageCount',
        'UserMessageCount',
        'AIMessageCount',
        'AverageUserMessageLength',
        'AverageAIMessageLength',
        'ConversationDuration',
        'ConversationDurationMinutes',
        'MessageRatio',
        'create_time',
        'start_time_unix',
        'end_time_unix',
        'data_status',
        'match_confidence',
        'is_duplicate'
    ]

    # Keep only conversation columns that exist
    conv_cols_exist = [col for col in conv_cols if col in df_finalized.columns]
    df_conv_data = df_finalized[conv_cols_exist].copy()

    print(f"Extracted {len(conv_cols_exist)} conversation-related columns")
    print()

    # === STEP 4: Merge clean survey with conversation data ===
    print("STEP 4: Merging clean survey data with conversation metrics")
    print("-" * 80)

    # Merge on ResponseId
    df_merged = df_survey_raw.merge(
        df_conv_data,
        on='ResponseId',
        how='left',
        suffixes=('', '_drop')
    )

    # Drop any duplicate columns from the merge
    cols_to_drop = [col for col in df_merged.columns if col.endswith('_drop')]
    if cols_to_drop:
        df_merged = df_merged.drop(columns=cols_to_drop)

    print(f"Merged dataset: {df_merged.shape}")
    print(f"All {len(df_survey_raw)} survey responses preserved")
    print()

    # === STEP 5: Filter to main study ===
    print("STEP 5: Filtering to main study")
    print("-" * 80)

    df_main = df_merged[df_merged['pilot'] == 0].copy()
    print(f"Main study participants: {len(df_main)}")
    print(f"Removed {len(df_merged) - len(df_main)} pilot participants")
    print()

    # === STEP 6: Create clean treatment variable ===
    print("STEP 6: Creating clean treatment variable")
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

    # === STEP 7: Fix conversation duration ===
    print("STEP 7: Computing conversation duration")
    print("-" * 80)

    # Calculate duration from timestamps if available
    if 'start_time_unix' in df_main.columns and 'end_time_unix' in df_main.columns:
        has_times = (df_main['start_time_unix'].notna()) & (df_main['end_time_unix'].notna())
        df_main.loc[has_times, 'conversation_duration_minutes'] = (
            (df_main.loc[has_times, 'end_time_unix'] - df_main.loc[has_times, 'start_time_unix']) / 60
        )
        print(f"Calculated conversation duration for {has_times.sum()} participants")
    print()

    # === STEP 8: Handle duplicates ===
    print("STEP 8: Handling duplicate participant records")
    print("-" * 80)

    # Check for duplicates
    dup_count = df_main['ResponseId'].duplicated().sum()
    print(f"Duplicate ResponseIds: {dup_count}")

    if dup_count > 0:
        # Keep first occurrence of each ResponseId
        df_main = df_main.drop_duplicates(subset=['ResponseId'], keep='first')
        print(f"After deduplication: {len(df_main)} participants")
    print()

    # === STEP 9: Summary statistics ===
    print("STEP 9: Summary statistics")
    print("-" * 80)

    print(f"\nTotal participants (main study): {len(df_main)}")

    print(f"\nTreatment distribution:")
    print(df_main['treatment'].value_counts(dropna=False))

    if 'HasMatch' in df_main.columns:
        matched = df_main[df_main['HasMatch'] == True]
        unmatched_false = df_main[df_main['HasMatch'] == False]
        unmatched_nan = df_main[df_main['HasMatch'].isna()]

        print(f"\nConversation matching:")
        print(f"  Matched (HasMatch=True): {len(matched)}")
        print(f"  Unmatched (HasMatch=False): {len(unmatched_false)}")
        print(f"  No matching attempted (HasMatch=NaN): {len(unmatched_nan)}")

        if len(matched) > 0:
            print(f"\nConversation metrics (matched participants, n={len(matched)}):")
            if 'MessageCount' in matched.columns:
                print(f"  Mean messages: {matched['MessageCount'].mean():.1f}")
            if 'UserMessageCount' in matched.columns:
                print(f"  Mean user messages: {matched['UserMessageCount'].mean():.1f}")
            if 'conversation_duration_minutes' in matched.columns:
                dur_available = matched['conversation_duration_minutes'].notna().sum()
                if dur_available > 0:
                    print(f"  Mean duration (min): {matched['conversation_duration_minutes'].mean():.1f} (n={dur_available})")

    if 'testscore' in df_main.columns:
        print(f"\nTest scores:")
        print(f"  Available: {df_main['testscore'].notna().sum()}/{len(df_main)}")
        print(f"  Mean: {df_main['testscore'].mean():.2f}")
        print(f"  Std: {df_main['testscore'].std():.2f}")

    print()

    # === STEP 10: Save clean dataset ===
    print("STEP 10: Saving clean dataset")
    print("-" * 80)

    output_file = 'data/processed/nhh_esperanto_final_analysis.csv'
    df_main.to_csv(output_file, index=False)
    print(f"✓ Saved to: {output_file}")
    print(f"✓ Dataset: {len(df_main)} rows × {len(df_main.columns)} columns")
    print()

    # Create matched-only subset
    if 'HasMatch' in df_main.columns:
        df_matched = df_main[df_main['HasMatch'] == True].copy()
        matched_file = 'data/processed/nhh_esperanto_matched_participants.csv'
        df_matched.to_csv(matched_file, index=False)
        print(f"✓ Matched participants: {matched_file}")
        print(f"  {len(df_matched)} participants with conversation data")
        print()

    # === FINAL SUMMARY ===
    print("=" * 80)
    print("CLEAN DATASET CREATED SUCCESSFULLY")
    print("=" * 80)
    print()
    print(f"Main dataset: {output_file}")
    print(f"  - {len(df_main)} main study participants")
    print(f"  - Clean survey data from raw source")
    print(f"  - Conversation metrics where available")
    print(f"  - Ready for analysis")
    print()

if __name__ == "__main__":
    main()
