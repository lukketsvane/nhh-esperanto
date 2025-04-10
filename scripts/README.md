# NHH Esperanto Data Processing Scripts

This directory contains scripts for processing and enhancing the Esperanto language learning experiment data.

## Scripts Overview

### 1. `merge_datasets.py`

Merges survey data from Qualtrics (`iverdata.csv`) with conversation logs (`unified_conversation_data.csv`).

**Key functionality:**
- Matches participants across datasets using ID patterns and timestamps
- Converts timestamps to Unix format for consistent comparison
- Extracts conversation metrics (message counts, durations, etc.)
- Creates comprehensive matching statistics
- Generates matched and unmatched datasets

**Usage:**
```bash
python scripts/merge_datasets.py
```

**Outputs:**
- `data/processed/aligned_unified_conversation_data.csv`: Complete dataset with all records
- `data/processed/aligned_unified_conversation_data_matched_only.csv`: Only successfully matched records
- `data/processed/aligned_unified_conversation_data_unmatched_conversations.csv`: Conversation logs that couldn't be matched
- `data/processed/nhh_esperanto_finalized_dataset.csv`: Final version with participant IDs and complete metadata

### 2. `enhance_dataset.py`

Enhances the finalized dataset with additional metrics and restructures it into a more analysis-friendly format.

**Key functionality:**
- Fixes encoding and formatting issues
- Improves user identification and deduplication
- Cleans up Esperanto text fields
- Creates additional metrics for analysis
- Restructures the dataset into normalized tables
- Generates a data dictionary

**Usage:**
```bash
python scripts/enhance_dataset.py
```

**Outputs:**
- `data/processed/nhh_esperanto_enhanced_dataset.csv`: Enhanced full dataset
- `data/processed/nhh_esperanto_participants.csv`: Participant demographic data
- `data/processed/nhh_esperanto_conversations.csv`: Conversation metadata
- `data/processed/nhh_esperanto_messages.csv`: Individual messages in structured format
- `data/processed/nhh_esperanto_data_dictionary.csv`: Data dictionary with variable descriptions

## Running the Full Pipeline

To process the data from scratch, run these scripts in order:

```bash
# 1. Merge survey data with conversation logs
python scripts/merge_datasets.py

# 2. Enhance the merged dataset
python scripts/enhance_dataset.py
```

## Notes

- The scripts will look for raw data in the `data/raw/` directory
- All processed outputs will be saved in the `data/processed/` directory
- Both scripts include detailed logging to help track the processing steps
- Unix timestamps are used for all time calculations to ensure consistency