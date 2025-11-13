# Unified Complete Dataset - NHH Esperanto Study

**Date**: November 13, 2025
**All Participants**: 604 (Main Study + Pilot)

## Overview

This document describes the **complete unified dataset** that includes ALL 604 participants from the NHH Esperanto language learning study (both main study and pilot participants).

## Dataset Files

### 1. Complete Unified Dataset (RECOMMENDED)

**File**: `data/processed/nhh_esperanto_complete_unified.csv`

- **Total participants**: 604
- **Main study**: 499 (82.6%)
- **Pilot study**: 105 (17.4%)
- **Treatment coverage**: 100%
- **Conversation matches**: 132 (21.9%)
- **Test scores**: 582 (96.4%)

**Use this file for:**
- Comprehensive analyses including all participants
- Comparing main study vs pilot results
- Maximum statistical power
- Complete participant tracking

### 2. Main Study Only

**File**: `data/processed/nhh_esperanto_main_study_only.csv`

- **Participants**: 499
- Same as `nhh_esperanto_final_analysis.csv` but extracted from unified dataset

**Use this file for:**
- Primary analyses for the MIT NHH paper
- Excluding pilot data
- Final publication results

### 3. Pilot Study Only

**File**: `data/processed/nhh_esperanto_pilot_study_only.csv`

- **Participants**: 105
- Pilot phase data for comparison

**Use this file for:**
- Pilot study analyses
- Method validation
- Comparing pilot vs main study

## Key Features

### Unified Participant IDs

Every participant has a `unified_participant_id` that works across all datasets:

| ID Type | Format | Example | Usage |
|---------|--------|---------|-------|
| Matched with conversation | `ID_#` | `ID_23` | Participants with matched conversations |
| Matched with participant_id | `P###` | `P042` | Alternative participant identifier |
| Survey only | `R_ResponseId` | `R_R_2YrX7B6LLgDiXaH` | Participants without conversation match |

### Complete Information

Each row contains:

1. **Survey Data** (from raw survey file)
   - All original survey responses
   - Demographics (age, gender, GPA)
   - Test scores
   - Survey timestamps and duration

2. **Treatment Assignment**
   - `treatment`: Clean treatment variable (Control, AI-assisted, AI-guided)
   - `pilot`: Study phase indicator (0=Main, 1=Pilot)
   - `study_phase`: Human-readable phase ("Main Study" or "Pilot Study")

3. **Conversation Data** (where available)
   - `conversation_id`: ChatGPT conversation identifier
   - `MessageCount`: Total messages exchanged
   - `UserMessageCount`: Participant messages
   - `AIMessageCount`: AI response messages
   - `conversation_duration_minutes`: Length of conversation
   - Conversation timestamps

4. **Matching Information**
   - `HasMatch`: Whether conversation was matched (True/False/NaN)
   - `MatchMethod`: How the match was made
   - `match_confidence`: Confidence score
   - `data_status`: Data quality status

## Summary Statistics

### Overall Distribution

| Category | Count | Percentage |
|----------|-------|------------|
| **Total Participants** | 604 | 100.0% |
| Main Study | 499 | 82.6% |
| Pilot Study | 105 | 17.4% |

### Treatment Assignment

| Treatment | Main Study | Pilot Study | Total |
|-----------|-----------|-------------|-------|
| Control | 163 | 46 | 209 (34.6%) |
| AI-assisted | 177 | 19 | 196 (32.5%) |
| AI-guided | 159 | 40 | 199 (32.9%) |

### Conversation Matching

| Status | Main Study | Pilot Study | Total |
|--------|-----------|-------------|-------|
| Matched (HasMatch=True) | 108 (21.6%) | 24 (22.9%) | 132 (21.9%) |
| No conversation | 177 (35.5%) | 38 (36.2%) | 215 (35.6%) |
| Not attempted | 214 (42.9%) | 43 (41.0%) | 257 (42.5%) |

### Data Completeness

| Variable | Available | Coverage |
|----------|-----------|----------|
| Treatment | 604/604 | 100.0% |
| Unified ID | 604/604 | 100.0% |
| Test scores | 582/604 | 96.4% |
| Gender | 604/604 | 100.0% |
| Age | 604/604 | 100.0% |
| GPA | 604/604 | 100.0% |
| Conversation data* | 132/604 | 21.9% |

*Among matched participants only

### Conversation Metrics (n=132 matched)

| Metric | Mean | Std |
|--------|------|-----|
| Messages per conversation | 22.5 | - |
| User messages | 10.5 | - |
| AI messages | 12.0 | - |
| Conversation duration (min) | 177.0 | - |

### Test Score Results

| Group | n | Mean | Std |
|-------|---|------|-----|
| All participants | 582 | 8.02 | - |
| Main study | 478 | 8.03 | 1.88 |
| Pilot study | 104 | 7.98 | - |

## Data Quality

### Validation Checks Performed

✓ **No duplicates**: All 604 ResponseIds are unique
✓ **Treatment coverage**: 100% (all participants assigned)
✓ **Unified IDs**: 100% coverage
✓ **Data integrity**: All columns contain appropriate data types
✓ **No corruption**: Clean survey data from raw source
✓ **Proper merging**: Conversation data matched where available

### Known Limitations

1. **Conversation match rate**: Only 21.9% of participants have matched conversations
   - May have not completed conversation task
   - May have technical issues during data collection

2. **Missing test scores**: 22 participants (3.6%) lack test scores
   - Likely dropped out before completing test
   - Otherwise have complete survey data

3. **Match rate variation**: Similar across main (21.6%) and pilot (22.9%) studies

## Column Guide

### Key Identifier Columns

- `ResponseId`: Qualtrics survey response ID (primary key)
- `unified_participant_id`: Universal participant identifier
- `final_id`: Matched participant ID (numeric)
- `participant_id`: Conversation participant ID (e.g., P001)
- `conversation_id`: ChatGPT conversation ID

### Study Design Columns

- `pilot`: Binary indicator (0=Main, 1=Pilot)
- `study_phase`: Text indicator ("Main Study" or "Pilot Study")
- `treatment`: Clean treatment assignment
- `control`, `ai_assist`, `ai_guided`: Binary treatment indicators

### Outcome Variables

- `testscore`: Esperanto language test score (range: 1-12)
- `MessageCount`: Total conversation messages
- `UserMessageCount`: Participant messages
- `conversation_duration_minutes`: Conversation length

### Survey Variables

- Demographics: `gender`, `age`, `yearincollege`, `faculty`, `gpa`
- Attitudes: `AIfamiliar`, `AIsubscription`, `followrules`
- Indices: `index_confidence`, `index_motivation`, `index_complement`, `index_cheating`

### Matching Variables

- `HasMatch`: Conversation match status (True/False/NaN)
- `MatchMethod`: Method used for matching
- `match_confidence`: Confidence score
- `data_status`: Quality indicator
- `timestamp_diff_minutes`: Time difference between survey and conversation

## Usage Recommendations

### For Primary Publication Analyses

Use **Main Study dataset** (`nhh_esperanto_main_study_only.csv`, n=499):
- Primary treatment effects on test scores
- Main study results for publication
- Excludes pilot to avoid contamination

### For Comprehensive Analyses

Use **Complete Unified dataset** (`nhh_esperanto_complete_unified.csv`, n=604):
- Maximum statistical power
- Robustness checks including pilot
- Exploratory analyses
- Method validation

### For Conversation-Specific Analyses

Filter to `HasMatch == True` (n=132):
- Conversation engagement patterns
- Message analysis
- Duration effects
- Include both main and pilot matched participants

### For Pilot Validation

Use **Pilot Study dataset** (`nhh_esperanto_pilot_study_only.csv`, n=105):
- Pilot-specific analyses
- Method validation
- Comparison with main study

## Statistical Considerations

1. **Intent-to-Treat (ITT)**
   - Use all assigned participants regardless of conversation completion
   - Recommended for primary analyses
   - More conservative estimates

2. **As-Treated (AT)**
   - Use only participants who completed conversations (n=132)
   - Secondary analyses
   - May have selection bias

3. **Missing Data**
   - Conversation data: Consider as separate outcome
   - Test scores: 96.4% coverage, minimal impact
   - Use appropriate missing data methods

4. **Study Phase**
   - Consider pilot as sensitivity analysis
   - Check for differences between phases
   - May pool if no significant differences

## Related Documentation

- `DATA_CLEANING_REPORT.md`: Detailed cleaning process and issues resolved
- `FINAL_MATCHING_REPORT.md`: Original matching methodology
- `README.MD`: Repository overview
- `scripts/create_unified_complete_dataset.py`: Dataset creation script

## Change Log

### 2025-11-13
- Created unified complete dataset with all 604 participants
- Added unified_participant_id for all participants
- Separated main study, pilot study, and complete datasets
- Validated all data quality checks

---

**Prepared by**: Claude Code
**Session**: claude/review-clean-dataset-01SFqyVXGjF2VWwtfi3T6q3L
**Date**: November 13, 2025
