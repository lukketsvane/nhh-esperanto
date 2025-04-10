# NHH Esperanto Dataset - Data Processing & Explorer

This repository contains a dataset from an Esperanto language learning experiment with AI assistance, along with tools for processing and exploring the data.

## Dataset Overview

The dataset comprises information from language learning experiments where participants were assigned to different treatment groups:

- **Control**: No AI assistance
- **AI-assisted**: Basic AI assistance 
- **AI-guided**: Enhanced AI assistance with structured guidance

For each participant, the dataset includes demographic information, language learning performance metrics, and conversation data with AI assistants.

## Data Processing Pipeline

### 1. Data Collection

The raw data consists of two primary sources:
- **Survey data**: Participant demographics and test scores collected via Qualtrics
- **Conversation data**: Logs of participant interactions with AI assistants

### 2. Data Merging

The `merge_datasets.py` script performs the following steps:
- Loads survey data from `iverdata.csv`
- Loads conversation data from `unified_conversation_data.csv`
- Matches participants between datasets using:
  - Participant IDs where available
  - Session IDs and timestamps where direct ID matching isn't possible
- Creates a unified dataset with both survey responses and conversation metrics

### 3. Data Enhancement

The `enhance_dataset.py` script improves the dataset quality through:
1. **Data Cleaning**
   - Normalization of categorical variables
   - Treatment of missing values
   - Conversion of data types
   - Standardization of Esperanto text

2. **Feature Engineering**
   - Creating derived metrics:
     - `ConversationDurationMinutes`: Duration in minutes
     - `MessageRatio`: Ratio of user to AI messages
     - `AverageMessageLength`: Characters per message

3. **Confidence Scoring**
   - Added `match_confidence` to indicate certainty of user identification
   - Flagged potentially problematic matches

4. **Data Stratification**
   - Aligned data by treatment group
   - Computed treatment effects

### 4. Output Datasets

The processing pipeline produces several output files:

1. **Unified Datasets**:
   - `aligned_unified_conversation_data.csv`: Complete dataset with all matched records
   - `aligned_unified_conversation_data_matched_only.csv`: Only high-confidence matches
   - `aligned_unified_conversation_data_unmatched_conversations.csv`: Conversations without participant matches

2. **Normalized Relational Data**:
   - `nhh_esperanto_participants.csv`: Participant demographic data
   - `nhh_esperanto_conversations.csv`: Conversation metadata
   - `nhh_esperanto_messages.csv`: Individual messages
   - `nhh_esperanto_data_dictionary.csv`: Data dictionary explaining all variables

## Key Variables

### Participant Variables
- `final_id`: Participant ID
- `treatment_clean`: Treatment group (Control, AI-assisted, AI-guided)
- `gender`: Participant gender
- `highgpa`: Binary indicator for high GPA
- `testscore`: Score on Esperanto language test
- `index_confidence`, `index_motivation`, `index_complement`, `index_cheating`: Psychological indices

### Conversation Metrics
- `MessageCount`: Total number of messages exchanged
- `UserMessageCount`: Number of messages from the user
- `AIMessageCount`: Number of messages from the AI
- `ConversationDurationMinutes`: Duration of conversation
- `AverageUserMessageLength`: Average characters per user message
- `AverageAIMessageLength`: Average characters per AI message

## Data Explorer Application

The repository includes a Next.js application for exploring and visualizing the dataset:

### Features
- **Data Table View**: Browse and filter records
- **Visualization Tools**: Create bar charts, box plots, histograms, and scatter plots
- **Summary Statistics**: View distributions and relationships between variables
- **Export Functionality**: Download filtered data or charts

### Technical Details
- **Framework**: Next.js 15
- **UI Library**: React 19
- **Styling**: Tailwind CSS
- **Components**: shadcn/ui
- **Charts**: Chart.js with BoxPlot extension
- **Data Parsing**: Papa Parse

## Getting Started

1. **Clone the repository**
   ```
   git clone https://github.com/lukketsvane/nhh-esperanto.git
   cd nhh-esperanto
   ```

2. **Install dependencies**
   ```
   npm install --legacy-peer-deps
   ```

3. **Run the development server**
   ```
   npm run dev
   ```

4. **Open your browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

## Data Processing Scripts

If you want to re-run the data processing steps:

```python
# Merge datasets
python merge_datasets.py

# Enhance and clean data
python enhance_dataset.py
```

## License

[MIT License](LICENSE)