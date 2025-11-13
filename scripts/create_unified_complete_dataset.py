#!/usr/bin/env python3
"""
Create Unified Complete Dataset - All Participants with IDs

This script creates a comprehensive dataset containing ALL 604 participants
(both main study and pilot) with:
- Proper participant IDs
- Clean survey data from raw source
- Conversation matching information where available
- Treatment assignment
- All relevant metrics

Output: data/processed/nhh_esperanto_complete_unified.csv
"""

import pandas as pd
import numpy as np

def main():
    print("=" * 80)
    print("CREATING UNIFIED COMPLETE DATASET - ALL PARTICIPANTS")
    print("=" * 80)
    print()

    # === STEP 1: Load raw survey data (ALL responses) ===
    print("STEP 1: Loading raw survey data (all responses)")
    print("-" * 80)

    df_survey_raw = pd.read_csv('data/raw/iverdata.csv')
    print(f"Total survey responses: {len(df_survey_raw)}")
    print(f"  Main study (pilot=0): {(df_survey_raw['pilot'] == 0).sum()}")
    print(f"  Pilot study (pilot=1): {(df_survey_raw['pilot'] == 1).sum()}")
    print()

    # === STEP 2: Load finalized dataset for conversation matching info ===
    print("STEP 2: Loading conversation matching information")
    print("-" * 80)

    df_finalized = pd.read_csv('data/processed/nhh_esperanto_finalized_dataset.csv')
    print(f"Finalized dataset rows: {len(df_finalized)}")
    print()

    # === STEP 3: Extract conversation and matching columns ===
    print("STEP 3: Extracting conversation and ID information")
    print("-" * 80)

    # All relevant columns from finalized dataset
    info_cols = [
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
        'Session',
        'data_status',
        'match_confidence',
        'is_duplicate',
        'UserID_Source',
        'timestamp_diff',
        'timestamp_diff_minutes'
    ]

    # Keep only columns that exist
    info_cols_exist = [col for col in info_cols if col in df_finalized.columns]

    # Get unique entries per ResponseId (keep best match)
    df_info = df_finalized[info_cols_exist].copy()

    # If there are duplicates, keep the first occurrence (should already be sorted by priority)
    df_info = df_info.drop_duplicates(subset=['ResponseId'], keep='first')

    print(f"Extracted {len(info_cols_exist)} information columns")
    print(f"Unique ResponseIds with info: {len(df_info)}")
    print()

    # === STEP 4: Merge clean survey with conversation info ===
    print("STEP 4: Merging survey data with conversation information")
    print("-" * 80)

    df_unified = df_survey_raw.merge(
        df_info,
        on='ResponseId',
        how='left',
        suffixes=('', '_drop')
    )

    # Drop any duplicate columns
    cols_to_drop = [col for col in df_unified.columns if col.endswith('_drop')]
    if cols_to_drop:
        df_unified = df_unified.drop(columns=cols_to_drop)

    print(f"Unified dataset: {df_unified.shape}")
    print(f"All {len(df_survey_raw)} survey responses included")
    print()

    # === STEP 5: Create clean treatment variable for ALL participants ===
    print("STEP 5: Creating treatment variable for all participants")
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

    df_unified['treatment'] = df_unified.apply(assign_treatment, axis=1)

    print("Treatment assignment (all participants):")
    print(df_unified['treatment'].value_counts(dropna=False))
    print()

    print("Treatment by study type:")
    print(pd.crosstab(df_unified['pilot'].map({0: 'Main Study', 1: 'Pilot'}),
                      df_unified['treatment'].fillna('Unassigned'),
                      margins=True))
    print()

    # === STEP 6: Calculate conversation duration ===
    print("STEP 6: Computing conversation duration")
    print("-" * 80)

    if 'start_time_unix' in df_unified.columns and 'end_time_unix' in df_unified.columns:
        has_times = (df_unified['start_time_unix'].notna()) & (df_unified['end_time_unix'].notna())
        df_unified.loc[has_times, 'conversation_duration_minutes'] = (
            (df_unified.loc[has_times, 'end_time_unix'] - df_unified.loc[has_times, 'start_time_unix']) / 60
        )
        print(f"Calculated conversation duration for {has_times.sum()} participants")
    print()

    # === STEP 7: Create study phase indicator ===
    print("STEP 7: Creating study phase indicator")
    print("-" * 80)

    df_unified['study_phase'] = df_unified['pilot'].map({
        0: 'Main Study',
        1: 'Pilot Study'
    })

    print("Study phase distribution:")
    print(df_unified['study_phase'].value_counts(dropna=False))
    print()

    # === STEP 8: Create comprehensive participant ID ===
    print("STEP 8: Creating comprehensive participant IDs")
    print("-" * 80)

    # Create a unified participant ID that works for everyone
    # Priority: final_id > participant_id > ResponseId
    def create_unified_id(row):
        # If we have a final_id, use it
        if pd.notna(row.get('final_id')):
            return f"ID_{int(row['final_id'])}"
        # If we have participant_id, use it
        elif pd.notna(row.get('participant_id')):
            return str(row['participant_id'])
        # Otherwise use ResponseId
        else:
            return f"R_{row['ResponseId']}"

    df_unified['unified_participant_id'] = df_unified.apply(create_unified_id, axis=1)

    print(f"Created unified IDs for all {len(df_unified)} participants")
    print(f"Sample IDs: {df_unified['unified_participant_id'].head(10).tolist()}")
    print()

    # === STEP 9: Summary statistics ===
    print("STEP 9: Summary statistics")
    print("-" * 80)

    print(f"\n=== ALL PARTICIPANTS ===")
    print(f"Total: {len(df_unified)}")
    print(f"  Main study: {(df_unified['pilot'] == 0).sum()}")
    print(f"  Pilot study: {(df_unified['pilot'] == 1).sum()}")

    print(f"\n=== TREATMENT DISTRIBUTION ===")
    print(df_unified.groupby(['study_phase', 'treatment']).size().unstack(fill_value=0))

    print(f"\n=== CONVERSATION MATCHING ===")
    if 'HasMatch' in df_unified.columns:
        matched = df_unified[df_unified['HasMatch'] == True]
        unmatched_false = df_unified[df_unified['HasMatch'] == False]
        unmatched_nan = df_unified[df_unified['HasMatch'].isna()]

        print(f"Matched (HasMatch=True): {len(matched)}")
        print(f"  Main study: {(matched['pilot'] == 0).sum()}")
        print(f"  Pilot study: {(matched['pilot'] == 1).sum()}")

        print(f"Unmatched (HasMatch=False): {len(unmatched_false)}")
        print(f"No matching attempted (HasMatch=NaN): {len(unmatched_nan)}")

        if len(matched) > 0:
            print(f"\n=== CONVERSATION METRICS (matched participants, n={len(matched)}) ===")
            if 'MessageCount' in matched.columns:
                print(f"Mean messages: {matched['MessageCount'].mean():.1f}")
            if 'UserMessageCount' in matched.columns:
                print(f"Mean user messages: {matched['UserMessageCount'].mean():.1f}")
            if 'conversation_duration_minutes' in matched.columns:
                dur_available = matched['conversation_duration_minutes'].notna().sum()
                if dur_available > 0:
                    print(f"Mean duration (min): {matched['conversation_duration_minutes'].mean():.1f} (n={dur_available})")

    print(f"\n=== TEST SCORES ===")
    if 'testscore' in df_unified.columns:
        print(f"Available: {df_unified['testscore'].notna().sum()}/{len(df_unified)}")
        print(f"  Main study: {df_unified[df_unified['pilot']==0]['testscore'].notna().sum()}")
        print(f"  Pilot study: {df_unified[df_unified['pilot']==1]['testscore'].notna().sum()}")
        print(f"Mean (all): {df_unified['testscore'].mean():.2f}")
        print(f"Mean (main study): {df_unified[df_unified['pilot']==0]['testscore'].mean():.2f}")

    print()

    # === STEP 10: Save unified complete dataset ===
    print("STEP 10: Saving unified complete dataset")
    print("-" * 80)

    output_file = 'data/processed/nhh_esperanto_complete_unified.csv'
    df_unified.to_csv(output_file, index=False)
    print(f"✓ Saved to: {output_file}")
    print(f"✓ Dataset: {len(df_unified)} rows × {len(df_unified.columns)} columns")
    print()

    # Also create separate files for convenience
    df_main = df_unified[df_unified['pilot'] == 0].copy()
    df_pilot = df_unified[df_unified['pilot'] == 1].copy()

    main_file = 'data/processed/nhh_esperanto_main_study_only.csv'
    pilot_file = 'data/processed/nhh_esperanto_pilot_study_only.csv'

    df_main.to_csv(main_file, index=False)
    df_pilot.to_csv(pilot_file, index=False)

    print(f"✓ Main study only: {main_file} ({len(df_main)} participants)")
    print(f"✓ Pilot study only: {pilot_file} ({len(df_pilot)} participants)")
    print()

    # === FINAL SUMMARY ===
    print("=" * 80)
    print("UNIFIED COMPLETE DATASET CREATED SUCCESSFULLY")
    print("=" * 80)
    print()
    print(f"Complete unified dataset: {output_file}")
    print(f"  - ALL {len(df_unified)} participants (main + pilot)")
    print(f"  - Unified participant IDs for everyone")
    print(f"  - Clean survey data from raw source")
    print(f"  - Conversation matching info where available")
    print(f"  - Treatment assignment")
    print(f"  - Ready for comprehensive analysis")
    print()
    print("Separate files for convenience:")
    print(f"  - Main study ({len(df_main)}): {main_file}")
    print(f"  - Pilot study ({len(df_pilot)}): {pilot_file}")
    print()

if __name__ == "__main__":
    main()
