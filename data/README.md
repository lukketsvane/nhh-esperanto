# NHH Esperanto Study - Data Directory

This directory contains all data files for the NHH Esperanto language learning experiment.

## 📁 Directory Structure

```
data/
├── raw/                    # Original, unprocessed data files
├── processed/              # Processed and matched datasets
│   ├── backups/           # Backup copies of datasets during processing
│   └── intermediate/      # Intermediate processing outputs
└── old/                    # Historical data exports and previous versions
```

## 🔑 Key Data Files

### Primary Dataset (USE THIS!)
**`processed/nhh_esperanto_finalized_dataset.csv`**
- **The main dataset for analysis**
- 604 survey responses with matched ChatGPT conversation data
- 389 successfully matched (64.4%)
- 215 unmatched (participants who didn't complete ChatGPT task)

### Structured Tables
These files break down the main dataset into normalized tables:

1. **`processed/nhh_esperanto_participants.csv`**
   - Participant demographic and survey data
   - One row per participant
   - Includes treatment assignment, demographics, survey responses

2. **`processed/nhh_esperanto_conversations.csv`**
   - Conversation metadata
   - One row per conversation
   - Includes conversation duration, message counts, timestamps

3. **`processed/nhh_esperanto_messages.csv`**
   - Individual conversation messages
   - One row per message
   - Includes author role, message content, timestamps

4. **`processed/nhh_esperanto_data_dictionary.csv`**
   - Variable descriptions and metadata
   - Explains all columns in the datasets

### Enhanced Dataset
**`processed/nhh_esperanto_enhanced_dataset.csv`**
- Enhanced version with additional calculated fields
- Cleaned Esperanto text
- Additional metrics for analysis

### Recovery Files
**`processed/recovered_conversation_messages.csv`**
- 366 messages from 21 conversations recovered from old CSN export
- These conversations were previously inaccessible due to data format issues

**`processed/recovered_matches.csv`**
- Details of 20 matches between recovered conversations and surveys
- Includes time differences and matching details

### Sample Dataset
**`processed/esperanto_sample_100.csv`**
- 100-participant sample for testing and exploration
- Same structure as main dataset

## 📊 Raw Data Files

### Survey Data
**`raw/iverdata.csv`**
- Original Qualtrics survey export
- 604 survey responses
- Contains demographics, treatment assignment, survey questions

### Conversation Data
**`raw/unified_conversation_data_complete.csv`**
- Complete conversation data (397 conversations)
- Includes original 376 + 21 recovered conversations
- Merged from multiple ChatGPT exports

**`raw/unified_conversation_data.csv`**
- Original conversation data export (376 conversations)
- Pre-recovery version

**`raw/unified_conversation_data_cleaned.csv`**
- Cleaned version of original data

**`raw/schedule_sessions.csv`**
- Session scheduling data

## 🗄️ Intermediate Files

Located in `processed/intermediate/`:

- `aligned_unified_conversation_data.csv` - Initial alignment of all data
- `aligned_unified_conversation_data_matched_only.csv` - Only matched records
- `aligned_unified_conversation_data_unmatched_conversations.csv` - Unmatched conversations
- `additional_conversation_messages.csv` - Additional extracted messages
- `optimal_matches.csv` - Optimal matching results
- `regenerated_ids_analysis.csv` - ID extraction and generation analysis

## 💾 Backup Files

Located in `processed/backups/`:

- `nhh_esperanto_finalized_dataset_backup_20251104_021921.csv` - Timestamped backup
- `nhh_esperanto_finalized_dataset_before_recovery_backup.csv` - Pre-recovery state
- `nhh_esperanto_finalized_dataset_updated_ids.csv` - After ID regeneration
- `nhh_esperanto_finalized_dataset_with_recovered.csv` - After adding recovered data
- `esperanto_final_matched_dataset.csv` - Earlier matched dataset version

## 📜 Historical Data

Located in `old/`:

### Critical Recovery Source
**`Unified_CSN_Data_-_16-12-2024.csv`** ⭐
- Old ChatGPT export containing 21 additional conversations
- Contains Python dictionary strings in `mapping` field
- Recovered using `ast.literal_eval()` parsing
- Enabled recovery of 20 additional matches

### Other Historical Files
- Previous versions of processed datasets
- JSON exports of conversation data
- Sample datasets (5, 10, 100 participants)

## 🔍 Data Matching Summary

### Match Methods

1. **ExplicitID** (8 matches, 1.3%)
   - Participants who explicitly stated their ID in the conversation
   - Direct matching via ID pattern recognition

2. **Timestamp** (361 matches, 59.8%)
   - Participants who **forgot to state their ID**
   - Matched via temporal proximity between survey and conversation
   - 24-hour tolerance window
   - Generated IDs from conversation timestamps

3. **RecoveredData** (20 matches, 3.3%)
   - Conversations recovered from old CSN export file
   - Previously inaccessible due to data format issues
   - Matched via timestamp proximity

### Unmatched Participants (215, 35.6%)

**Why they're unmatched:**
- 604 survey responses collected
- 397 conversations available
- Gap of 207 participants who never created conversations
- These participants completed the survey but didn't do the ChatGPT task
- All available conversation data has been exhaustively matched (98.0% success rate)

## 📈 Data Quality Metrics

- **Total survey responses**: 604
- **Available conversations**: 397
- **Successfully matched**: 389 (98.0% of available conversations)
- **Unused conversations**: 8 (all "Login assistance" test messages)
- **Average time difference** (timestamp matches): 10.71 hours
- **Average time difference** (recovered matches): 5.3 hours

## 🔐 Data Privacy

All data files contain anonymized participant IDs. Original identifying information has been removed or pseudonymized according to research ethics protocols.

## 📊 For Researchers

**To start your analysis**, use:
- `processed/nhh_esperanto_finalized_dataset.csv` - Main comprehensive dataset
- `processed/nhh_esperanto_data_dictionary.csv` - Variable documentation

**For specific analyses**:
- Participant demographics: `processed/nhh_esperanto_participants.csv`
- Conversation patterns: `processed/nhh_esperanto_conversations.csv`
- Message-level analysis: `processed/nhh_esperanto_messages.csv`

## ⚠️ Important Notes

1. **Duplicates**: Some participants completed the survey multiple times. These are marked with `data_status='Duplicate'`

2. **Time zones**: All timestamps are in Unix format for consistency. Original timezone was CET/CEST.

3. **ID format**: Generated IDs follow the pattern `DDMMYYYY_HHMM` or `DDMMYYYY_HHMM_N` where N is a sequence number.

4. **Missing data**: `HasMatch=False` indicates no conversation data exists for that participant (not that matching failed).

5. **Data completeness**: `data_status` field indicates:
   - `Complete`: Full match with high confidence
   - `Duplicate`: Multiple surveys for same participant
   - `Recovered`: Newly recovered from CSN file
   - `Missing conversation`: No conversation data exists

## 🔗 Related Documentation

- `/scripts/README.md` - Documentation of all processing scripts
- `/FINAL_MATCHING_REPORT.md` - Comprehensive recovery and matching report
- `/DATA_RECOVERY_SUMMARY.md` - Summary of data recovery process
- `/MATCHING_ANALYSIS.md` - Technical matching methodology

## 📧 Questions?

For questions about data processing or matching methodology, refer to the comprehensive documentation in the repository root and scripts directory.
