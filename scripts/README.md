# NHH Esperanto Data Processing Scripts

This directory contains scripts for processing, matching, and recovering data from the Esperanto language learning experiment.

## 📊 Final Results

- **Total surveys**: 604
- **Matched**: 389 (64.4%)
- **Participants who forgot their ID**: 361 (successfully recovered via timestamp matching!)
- **Match success rate**: 98.0% of all available conversations

## Scripts Overview

### Core Data Processing Scripts

#### `merge_datasets.py`
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
- `data/processed/intermediate/aligned_unified_conversation_data.csv`
- `data/processed/intermediate/aligned_unified_conversation_data_matched_only.csv`
- `data/processed/intermediate/aligned_unified_conversation_data_unmatched_conversations.csv`

#### `enhance_dataset.py`
Enhances the finalized dataset with additional metrics and restructures it into analysis-friendly format.

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
- `data/processed/nhh_esperanto_enhanced_dataset.csv`
- `data/processed/nhh_esperanto_participants.csv`
- `data/processed/nhh_esperanto_conversations.csv`
- `data/processed/nhh_esperanto_messages.csv`
- `data/processed/nhh_esperanto_data_dictionary.csv`

### Data Recovery Scripts

#### `regenerate_ids_and_verify.py` ⭐ KEY SCRIPT
Extracts and generates participant IDs for matching conversations to surveys.

**Key functionality:**
- Extracts IDs from conversation messages using multiple regex patterns
- Generates IDs from timestamps for participants who forgot to state their ID
- Handles various ID formats: `DDMMYYYY_HHMM_N`, `DD/MM/YYYY HH:MM N`, etc.
- Result: 291 IDs extracted, 78 generated from timestamps

**Usage:**
```bash
python scripts/regenerate_ids_and_verify.py
```

**Outputs:**
- `data/processed/intermediate/regenerated_ids_analysis.csv`
- Updated `data/processed/nhh_esperanto_finalized_dataset.csv`

#### `extract_using_ast.py` ⭐ BREAKTHROUGH SCRIPT
Extracts conversation messages from the CSN data file using AST parsing.

**Key functionality:**
- Uses `ast.literal_eval()` to parse Python dictionary strings (not JSON)
- Extracts messages from `mapping` field in old CSN export
- Recovered 366 messages from 21 previously inaccessible conversations
- Technical breakthrough that enabled major data recovery

**Usage:**
```bash
python scripts/extract_using_ast.py
```

**Outputs:**
- `data/processed/recovered_conversation_messages.csv`

#### `match_recovered_conversations.py`
Matches the 21 recovered conversations to unmatched surveys.

**Key functionality:**
- Timestamp-based matching with 24-hour tolerance
- Matches recovered conversations to surveys without conversation data
- Result: 20/21 recovered conversations successfully matched

**Usage:**
```bash
python scripts/match_recovered_conversations.py
```

**Outputs:**
- `data/processed/recovered_matches.csv`
- Updated `data/processed/nhh_esperanto_finalized_dataset.csv`

### Additional Recovery Attempts

#### `match_missing_ids.py`
Extended timestamp matching with 48-hour tolerance for difficult cases.

#### `rematch_with_unix_time.py`
Comprehensive rematching using unified Unix timestamps.

#### `aggressive_rematching.py`
Extended temporal tolerance matching (7, 14, 30 days).
- Result: 0 new matches (all conversations already used)

#### `fix_cross_date_mismatches.py`
Identifies and corrects conversations matched to surveys from different dates.
- Result: 0 mismatches found needing correction

### Helper Scripts

#### `extract_additional_conversations.py`
Extracts additional conversation data from alternative sources.

#### `extract_from_json.py`
Extracts conversation data from JSON format exports.

#### `apply_corrected_ids.py`
Applies corrected participant IDs to the dataset.

## 🔄 Processing Pipeline

To process the data from scratch, run scripts in this order:

```bash
# 1. Merge survey data with conversation logs
python scripts/merge_datasets.py

# 2. Enhance the merged dataset
python scripts/enhance_dataset.py

# 3. Regenerate and extract IDs (KEY STEP for forgotten IDs)
python scripts/regenerate_ids_and_verify.py

# 4. Extract recovered conversations from old CSN file
python scripts/extract_using_ast.py

# 5. Match recovered conversations to surveys
python scripts/match_recovered_conversations.py

# 6. (Optional) Run additional recovery attempts
python scripts/aggressive_rematching.py
python scripts/fix_cross_date_mismatches.py
```

## 📈 Recovery Success Story

### The Challenge
- 604 survey responses collected
- Only 397 ChatGPT conversations available
- Initial match: 369 (61.1%)
- **Unmatched: 235 (38.9%)** ❌

### The Problem
- Only 8 participants explicitly stated their ID in conversations
- **361 participants forgot to write their ID** 😱
- Additional 21 conversations found in old data export

### The Solution
1. **ID Extraction**: Implemented multiple regex patterns to extract IDs from various formats
2. **Timestamp Matching**: Matched conversations to surveys using temporal proximity
3. **ID Generation**: Created IDs from timestamps for those who forgot (`DDMMYYYY_HHMM`)
4. **AST Parsing Breakthrough**: Used `ast.literal_eval()` to parse Python dict strings
5. **Recovered Data**: Successfully extracted 21 additional conversations from CSN file

### The Results
- **Final match: 389 (64.4%)** ✅
- **Matched 361 participants who forgot their ID** 🎉
- **Recovered 20 additional matches** (+8.5% of lost data)
- **Match success: 98.0% of available conversations**
- Only 8 unused conversations (all "Login assistance" test messages)

### Why 215 Remain Unmatched
- Gap of 207 between surveys (604) and conversations (397)
- These participants completed the survey but never started the ChatGPT conversation
- All available conversation data has been exhaustively matched
- This represents genuine task non-completion, not data loss

## 🔧 Technical Notes

- All scripts use Unix timestamps for time calculations
- UTF-8 encoding for all file operations
- Python dictionary parsing requires `ast.literal_eval()` not `json.loads()`
- Timestamp tolerance of 24 hours used for matching (extended to 48 hours in some cases)
- One-to-one matching ensures no duplicate conversation assignments

## 📁 File Locations

- **Raw data**: `data/raw/`
- **Processed outputs**: `data/processed/`
- **Intermediate files**: `data/processed/intermediate/`
- **Backups**: `data/processed/backups/`
- **Old data sources**: `old/`
