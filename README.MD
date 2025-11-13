# NHH Esperanto - Language Learning Experiment Dataset

**Final Consolidated Dataset** - All 604 survey responses with matched ChatGPT conversation data

## 🎉 Dataset Complete - 604 Entries Ready for Analysis!

**Major Achievement**: Successfully recovered 361 participants (92.8% of matches) who forgot to state their ID!

### Quick Stats
- ✅ **604 total entries** (all survey responses)
- ✅ **389 matched** (64.4%) with ChatGPT conversation data
- ✅ **361 participants who forgot their ID** - successfully recovered via timestamp matching!
- ✅ **20 additional conversations** recovered from old data exports
- ✅ **98.0% match success rate** of all available conversations

### Main Dataset File
📊 **`data/processed/nhh_esperanto_final_consolidated_dataset.csv`** (3.29 MB)

See [FINAL_DATASET_DOCUMENTATION.md](FINAL_DATASET_DOCUMENTATION.md) for complete documentation.

## Repository Structure

```
nhh-esperanto/
├── data/
│   ├── raw/                      # Raw input data files
│   │   ├── iverdata.csv         # Survey responses (604)
│   │   └── unified_conversation_data_complete.csv  # All conversations (397)
│   │
│   ├── processed/                # Final processed datasets
│   │   ├── nhh_esperanto_final_consolidated_dataset.csv  # 🔑 MAIN DATASET (604 entries)
│   │   ├── nhh_esperanto_participants.csv      # Participant demographics
│   │   ├── nhh_esperanto_conversations.csv     # Conversation metadata
│   │   ├── nhh_esperanto_messages.csv          # Individual messages
│   │   ├── nhh_esperanto_data_dictionary.csv   # Variable descriptions
│   │   ├── recovered_conversation_messages.csv # Recovered data (366 messages)
│   │   ├── recovered_matches.csv               # Recovery match details (20 matches)
│   │   └── DATASET_SUMMARY.txt                 # Quick statistics
│   │
│   └── old/                      # Archive of historical data exports
│       └── Unified_CSN_Data_-_16-12-2024.csv  # Source of recovered data
│
├── scripts/                    # Processing and recovery scripts
│   ├── create_final_consolidated_dataset.py  # ⭐ Creates final 604-entry dataset
│   ├── cleanup_old_files.py                  # Cleans up old files
│   ├── regenerate_ids_and_verify.py          # Extracts/generates participant IDs
│   ├── extract_using_ast.py                  # Recovers data from CSN file
│   ├── match_recovered_conversations.py      # Matches recovered conversations
│   └── README.md                             # Scripts documentation
│
├── explorer/                   # Data exploration app (Next.js)
│
├── FINAL_DATASET_DOCUMENTATION.md  # 📊 Complete dataset documentation
├── RECOVERY_VERIFICATION_REPORT.md # Recovery verification details
├── FINAL_MATCHING_REPORT.md        # Matching methodology
└── README.MD                        # This file
```

## Dataset Description

This dataset documents an experiment where participants were assigned to different treatment groups while learning Esperanto:

- **Control**: No AI assistance
- **AI-assisted**: Basic AI assistance for answering questions
- **AI-guided**: Enhanced AI assistance with structured guidance and exercises

The experiment measured how different forms of AI assistance affect language learning, confidence, motivation, and other metrics.

## Key Variables

### Participant Variables
- `final_id`: Participant ID
- `treatment_clean`: Treatment group (Control, AI-assisted, AI-guided)
- `gender`: Participant gender
- `highgpa`: Binary indicator for high GPA
- `testscore`: Score on Esperanto language test
- `index_confidence`, `index_motivation`, `index_complement`, `index_cheating`: Psychological indices

### Conversation Metrics
- `MessageCount`: Total messages exchanged
- `UserMessageCount`: Number of user messages
- `AIMessageCount`: Number of AI messages
- `ConversationDurationMinutes`: Duration in minutes
- `AverageUserMessageLength`: Average characters per user message
- `AverageAIMessageLength`: Average characters per AI message

## Data Recovery & Processing Pipeline

Our data processing pipeline successfully recovered participants who forgot to state their ID and matched them to their conversations.

### Recovery Process

**The Challenge**: 361 out of 389 matched participants (92.8%) forgot to state their ID in the introductory ChatGPT message!

**The Solution**:
1. **ID Extraction** (`regenerate_ids_and_verify.py`): Extracted IDs from messages using multiple regex patterns
2. **Timestamp Matching**: Matched conversations to surveys using temporal proximity (24-hour tolerance)
3. **ID Generation**: Generated IDs from timestamps for those who forgot: `DDMMYYYY_HHMM` format
4. **Data Recovery** (`extract_using_ast.py`): Found 21 additional conversations in old CSN export
5. **AST Parsing Breakthrough**: Used `ast.literal_eval()` to parse Python dict strings (not JSON!)
6. **Additional Matching** (`match_recovered_conversations.py`): Matched 20/21 recovered conversations

**The Results**:
- ✅ **361 participants who forgot their ID successfully recovered!**
- ✅ **20 additional matches from recovered data**
- ✅ **98.0% match success rate** (of available conversations)
- Only 8 unused conversations (all "Login assistance" test messages)

### Core Processing Steps

#### 1. Data Merging (`merge_datasets.py`)

Merges survey responses with conversation logs:
- Matches participants across datasets using ID patterns and timestamps
- Extracts conversation metrics
- Identifies unmatched records for review
- Computes match confidence scores

#### 2. Data Enhancement (`enhance_dataset.py`)

Improves the merged dataset:
- Fixes encoding issues and standardizes formats
- Improves user identification
- Creates derived metrics
- Splits the data into normalized tables
- Generates a data dictionary

#### 3. ID Regeneration (`regenerate_ids_and_verify.py`) ⭐

Extracts and generates participant IDs:
- Extracts IDs from conversation messages using regex
- Generates IDs from timestamps for those who forgot
- Result: 291 extracted, 78 generated

#### 4. Data Recovery (`extract_using_ast.py`) ⭐

Recovers conversations from old CSN export:
- Uses `ast.literal_eval()` to parse Python dictionary strings
- Extracts 366 messages from 21 conversations
- Enables matching of previously inaccessible data

## Running the Data Processing Scripts

### Quick Start (Use Existing Processed Data)

The repository already contains fully processed and matched data:
- **Main dataset**: `data/processed/nhh_esperanto_finalized_dataset.csv`
- **Participant data**: `data/processed/nhh_esperanto_participants.csv`
- **Conversation data**: `data/processed/nhh_esperanto_conversations.csv`
- **Message data**: `data/processed/nhh_esperanto_messages.csv`

### Full Processing Pipeline (From Scratch)

To reproduce the entire processing and recovery pipeline:

```bash
# Create necessary directories if they don't exist
mkdir -p data/raw data/processed

# 1. Merge survey data with conversation logs
python scripts/merge_datasets.py

# 2. Enhance the merged dataset
python scripts/enhance_dataset.py

# 3. Extract and generate participant IDs (KEY STEP!)
python scripts/regenerate_ids_and_verify.py

# 4. Extract recovered conversations from old CSN file
python scripts/extract_using_ast.py

# 5. Match recovered conversations to surveys
python scripts/match_recovered_conversations.py

# 6. (Optional) Run additional recovery attempts
python scripts/aggressive_rematching.py
python scripts/fix_cross_date_mismatches.py
```

See [scripts/README.md](scripts/README.md) for detailed documentation of all scripts.

## Data Explorer Application

The repository includes a Next.js application for exploring and visualizing the dataset.

To set up and run the explorer:

```bash
# 1. Install dependencies
cd explorer
npm install --legacy-peer-deps

# 2. Run the development server
npm run dev
```

### Explorer Architecture

The data explorer uses a client-server architecture:

1. **Server-side**: 
   - API endpoints under `/api/data` read CSV files from the filesystem
   - Serves data to the client for visualization and exploration

2. **Client-side**:
   - Interactive data tables with filtering and pagination
   - Data visualization tools (charts, plots, etc.)
   - Statistical analysis and summary views

The explorer provides:
- Interactive data tables with filtering
- Visualizations (box plots, bar charts, histograms, scatter plots)
- Statistical summaries and frequency distributions
- Data export functionality

## License

[MIT License](LICENSE)