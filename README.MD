# NHH Esperanto - Language Learning Experiment Dataset

This repository contains a dataset and analysis tools from an experiment on Esperanto language learning with AI assistance.

## Repository Structure

```
nhh-esperanto/
├── data/
│   ├── raw/              # Raw input data files
│   │   ├── iverdata.csv  # Survey responses
│   │   └── unified_conversation_data.csv  # Conversation logs
│   │
│   └── processed/        # Processed and enhanced datasets
│       ├── aligned_unified_conversation_data*.csv  # Matched datasets
│       └── nhh_esperanto_*.csv  # Enhanced analysis datasets
│
├── scripts/              # Data processing scripts
│   ├── merge_datasets.py  # Merges survey and conversation data
│   └── enhance_dataset.py # Enhances the dataset for analysis
│
├── explorer/             # Data exploration application (Next.js)
│   └── explorer-clean.tar.gz  # Archived code for the explorer app
│
└── old/                  # Archive of original data files
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

## Data Processing Pipeline

Our data processing involves two main steps:

### 1. Data Merging (`merge_datasets.py`)

This script merges survey responses with conversation logs:
- Matches participants across datasets using ID patterns and timestamps
- Extracts conversation metrics
- Identifies unmatched records for review
- Computes match confidence scores

### 2. Data Enhancement (`enhance_dataset.py`)

This script improves the merged dataset:
- Fixes encoding issues and standardizes formats
- Improves user identification
- Creates derived metrics
- Splits the data into normalized tables
- Generates a data dictionary

## Running the Data Processing Scripts

```bash
# Create necessary directories if they don't exist
mkdir -p data/raw data/processed

# 1. Merge survey data with conversation logs
python scripts/merge_datasets.py

# 2. Enhance the merged dataset
python scripts/enhance_dataset.py
```

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