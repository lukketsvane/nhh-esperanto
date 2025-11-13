# NHH Esperanto Exports

## Available Files

### 📦 nhh_esperanto_promptdata_FINAL.zip
**Size**: 4.15 MB (compressed from 48.06 MB)
**Compression**: 91.4%
**Created**: 2025-11-13

#### Contents
- **22 CSN folders** (CSN1-CSN22) with complete conversation data
- **397 total conversations** from study participants
- **268 conversations** successfully matched to survey participants
- **121 files** including:
  - Updated `conversations.json` files with participant information
  - User profile data (`user.json`)
  - Chat HTML exports (`chat.html`)
  - Message feedback and model comparisons
  - Account screenshots

#### What's New
All matched conversations now include:
- `participant_id`: Survey ResponseId linking to main dataset
- `participant_user_id`: Generated or extracted user ID
- `participant_email`: Participant email address
- `participant_name`: Participant full name
- `match_method`: How the participant was matched (PromptData, Timestamp, etc.)
- `survey_start_time`: Unix timestamp of survey start
- `metadata.matched_participant`: Boolean flag
- `metadata.match_timestamp`: When the match was made

#### Data Quality by Folder

**High Quality (100% match rate)**:
- CSN10, CSN11, CSN13, CSN14, CSN15, CSN16, CSN17, CSN18

**Very Good (>90% match rate)**:
- CSN1 (95.2%)

**Good (60-90% match rate)**:
- CSN7 (70.0%), CSN19 (68.8%), CSN20 (63.2%), CSN2 (60.0%)

**Moderate (<60% match rate)**:
- CSN8 (57.1%), CSN21 (47.1%), CSN4 (47.1%), CSN6 (31.6%), CSN3 (30.0%), CSN5 (23.1%), CSN9 (22.9%), CSN22 (15.4%)

**Note**: Lower match rates may indicate pilot data, test conversations, or participants who completed conversations outside the main study window.

#### Usage
1. Extract the zip file
2. Navigate to individual CSN folders
3. Read `conversations.json` files to access conversation data with participant linkage
4. Use `participant_id` field to join with main dataset (`nhh_esperanto_complete_unified.csv`)

#### Integration with Main Dataset
The `participant_id` field in each conversation matches the `ResponseId` field in:
- `data/processed/nhh_esperanto_complete_unified.csv`

This allows you to:
- Link conversation patterns to survey responses
- Analyze conversation behavior by participant demographics
- Study the relationship between AI usage and test performance

#### Structure
```
promptdata/
├── CSN1/
│   ├── csn1/conversations.json (21 conversations, 20 matched)
│   ├── user.json
│   ├── chat.html
│   └── accounts screenshots
├── CSN2/
│   ├── conversations.json (20 conversations, 12 matched)
│   └── ...
├── CSN3/ - CSN22/
│   └── ...
```

## Additional Files

### promptdata_zip_summary_*.txt
Detailed summary of the zip archive including:
- Compression statistics
- File counts
- Data structure
- Updated conversation fields

## Data Provenance

All conversations in this archive have been:
1. Extracted from raw ChatGPT export data
2. Matched to survey participants using timestamp analysis
3. Enriched with participant information from survey responses
4. Validated for data quality and integrity
5. Backed up (original files saved as `.json.backup`)

## Questions?

For questions about the data structure or matching process, see:
- `EXPORT_SUMMARY.md` in project root
- `data/processed/promptdata_matches.csv` for match details
- `data/processed/promptdata_update_summary.csv` for folder statistics
