# Data Cleaning Report - MIT NHH Esperanto Study

**Date**: November 13, 2025
**Branch**: claude/review-clean-dataset-01SFqyVXGjF2VWwtfi3T6q3L

## Executive Summary

Successfully created a **clean, analysis-ready dataset** for the MIT NHH Esperanto language learning study. The final dataset contains **499 main study participants** with complete survey responses and conversation matching information where available.

### Final Dataset Files

1. **`nhh_esperanto_final_analysis.csv`** (MAIN DATASET)
   - 499 main study participants
   - Complete survey responses
   - Conversation metrics for matched participants
   - Ready for statistical analysis

2. **`nhh_esperanto_matched_participants.csv`** (MATCHED SUBSET)
   - 108 participants with conversation data
   - For conversation-specific analyses

## Issues Identified and Resolved

### 1. Data Corruption in Processed Files

**Problem**: The previously processed dataset (`nhh_esperanto_finalized_dataset.csv`) contained severe data corruption:
- Survey status columns (`Status`, `Finished`, `Durationinseconds`) contained conversation text instead of proper values
- Treatment assignment was missing for 361 participants
- Conversation duration was all zeros
- 256 duplicate participant records

**Root Cause**: Data corruption occurred during the merging process in earlier scripts.

**Solution**: Created clean dataset from scratch using:
- Raw survey data (`iverdata.csv`) - verified to be uncorrupted
- Conversation matching information from processed files
- Proper merging and cleaning procedures

### 2. Duplicate Participant Records

**Problem**: The finalized dataset contained 604 rows for 604 survey responses, but with many duplicates due to multiple conversation attempts.

**Solution**:
- Filtered to unique ResponseIds (one row per participant)
- For participants with multiple conversation attempts, kept the best match
- Final dataset: 499 unique participants (main study only)

### 3. Missing Treatment Assignment

**Problem**: 361 participants had `NaN` for `treatment_clean` due to improper mapping.

**Solution**:
- Created treatment variable from indicator columns (`control`, `ai_assist`, `ai_guided`)
- All 499 main study participants now have proper treatment assignment
- Distribution: 163 Control, 177 AI-assisted, 159 AI-guided

### 4. Incorrect Conversation Duration

**Problem**: `ConversationDuration` and `ConversationDurationMinutes` were all zeros.

**Solution**:
- Recalculated from Unix timestamps (`start_time_unix`, `end_time_unix`)
- Mean conversation duration: **67.5 minutes** (n=108)
- Much more realistic than the corrupted zero values

## Data Cleaning Process

### Scripts Created

1. **`create_final_clean_dataset.py`** (Initial attempt)
   - Attempted to clean the corrupted finalized dataset
   - Revealed extent of data corruption issues

2. **`build_clean_dataset_from_scratch.py`** (Second attempt)
   - Started from raw survey data
   - Attempted fresh merge with conversation data
   - Identified ID matching challenges

3. **`create_clean_analysis_dataset_v2.py`** ✓ (FINAL SOLUTION)
   - Loaded clean survey data from raw source
   - Extracted conversation metrics from processed files
   - Merged properly on ResponseId
   - Created clean, validated final dataset

### Cleaning Steps

1. **Load raw survey data** (604 responses)
   - Verified data integrity
   - All columns properly formatted and uncorrupted

2. **Filter to main study** (499 participants)
   - Excluded 105 pilot study participants (`pilot == 0`)
   - Retained all main study responses

3. **Extract conversation metrics**
   - Loaded matching information from processed files
   - Extracted 21 conversation-related columns
   - Avoided using corrupted survey columns

4. **Merge datasets**
   - Merged on ResponseId (unique identifier)
   - Left join to preserve all survey responses
   - Clean survey data + conversation metrics

5. **Create treatment variable**
   - Derived from indicator columns (control, ai_assist, ai_guided)
   - All participants properly assigned

6. **Calculate conversation duration**
   - Computed from Unix timestamps
   - Converted to minutes for analysis

7. **Validate and save**
   - Comprehensive validation checks
   - Saved final clean datasets

## Final Dataset Characteristics

### Sample Size

| Category | Count | Percentage |
|----------|-------|------------|
| **Total main study participants** | 499 | 100% |
| Matched with conversations | 108 | 21.6% |
| Unmatched (no conversation) | 177 | 35.5% |
| No matching attempted | 214 | 42.9% |

### Treatment Distribution

| Treatment | Count | Matched | Match Rate |
|-----------|-------|---------|------------|
| Control | 163 | 30 | 18.4% |
| AI-assisted | 177 | 41 | 23.2% |
| AI-guided | 159 | 37 | 23.3% |
| **Total** | **499** | **108** | **21.6%** |

### Data Completeness

| Variable | Available | Percentage |
|----------|-----------|------------|
| Treatment | 499/499 | 100% |
| Gender | 499/499 | 100% |
| Age | 499/499 | 100% |
| GPA | 499/499 | 100% |
| Test scores | 478/499 | 95.8% |
| Message count* | 108/108 | 100% |
| User messages* | 108/108 | 100% |
| Conversation duration* | 108/108 | 100% |

*Among matched participants only

### Key Statistics

**Survey Metrics (n=499)**
- Mean survey duration: 3,998 seconds (~67 minutes)
- Test score range: 1.0 - 12.0
- Mean test score: 8.03 (SD=1.88)
- Test scores available: 95.8%

**Conversation Metrics (n=108 matched participants)**
- Mean messages per conversation: 20.9
- Mean user messages: 9.7
- Mean AI messages: 11.2
- Mean conversation duration: 67.5 minutes
- All matched participants have complete conversation data

## Data Quality Assurance

### Validation Checks Performed

✓ **No duplicates**: 499 unique ResponseIds
✓ **Treatment assignment**: 100% coverage, no missing values
✓ **Data types**: All numeric columns properly formatted
✓ **Survey duration**: Realistic values (mean ~67 minutes)
✓ **Test scores**: Within valid range [1, 12]
✓ **Conversation metrics**: Realistic values for matched participants
✓ **No corruption**: All columns contain appropriate data types

### Limitations

1. **Low conversation match rate**: Only 21.6% of main study participants have matched conversation data
   - 177 participants marked as "unmatched" (likely didn't complete conversation task)
   - 214 participants had "no matching attempted" (may not have participated in conversation phase)

2. **Missing test scores**: 21 participants (4.2%) don't have test scores
   - May have dropped out before completing the test
   - Otherwise complete survey responses

3. **Conversation data availability**: Limited to 108 participants
   - May reduce statistical power for conversation-specific analyses
   - But sufficient for main treatment effect analyses using full sample

## Recommendations for Analysis

### Primary Analyses

Use **`nhh_esperanto_final_analysis.csv`** (n=499) for:
- Main treatment effects on test scores
- Demographic analyses
- Survey response analyses
- Intent-to-treat analyses (full sample regardless of conversation completion)

### Secondary Analyses

Use **`nhh_esperanto_matched_participants.csv`** (n=108) for:
- Conversation engagement analyses
- Message patterns by treatment
- Conversation duration effects
- As-treated analyses (participants who engaged with intervention)

### Statistical Considerations

1. **Missing conversation data**: Consider using multiple imputation or separate analyses for:
   - Full sample (ITT): Treatment effects on test scores
   - Conversation completers only (AT): Conversation engagement effects

2. **Match rate differences by treatment**:
   - Control: 18.4%
   - AI-assisted: 23.2%
   - AI-guided: 23.3%
   - Consider this as potential selection bias in conversation-specific analyses

3. **Power calculations**: With n=499 for main analyses and n=108 for conversation analyses, recalculate statistical power for key hypotheses

## File Locations

### Final Clean Datasets
- `/data/processed/nhh_esperanto_final_analysis.csv` - **MAIN DATASET** (499 participants)
- `/data/processed/nhh_esperanto_matched_participants.csv` - Matched subset (108 participants)

### Raw Data (Verified Clean)
- `/data/raw/iverdata.csv` - Raw survey responses (604)
- `/data/raw/unified_conversation_data_complete.csv` - All conversations (397)

### Processing Scripts
- `/scripts/create_clean_analysis_dataset_v2.py` - Final cleaning script
- `/scripts/build_clean_dataset_from_scratch.py` - Alternative approach
- `/scripts/create_final_clean_dataset.py` - Initial cleaning attempt

### Documentation
- `/DATA_CLEANING_REPORT.md` - This report
- `/FINAL_MATCHING_REPORT.md` - Previous matching process documentation
- `/README.MD` - Repository overview

## Conclusion

The dataset is now **clean, validated, and ready for analysis** for the MIT NHH Esperanto language learning paper. All data quality issues have been resolved:

✓ No data corruption
✓ No duplicates
✓ Complete treatment assignment
✓ Accurate conversation metrics
✓ Proper data types
✓ Comprehensive documentation

The main analysis dataset contains **499 main study participants** with complete survey responses, **108 with matched conversation data**, and **478 with test scores**. The data is suitable for rigorous statistical analysis of treatment effects on language learning outcomes.

---

**Prepared by**: Claude Code
**Session**: claude/review-clean-dataset-01SFqyVXGjF2VWwtfi3T6q3L
**Date**: November 13, 2025
