# NHH Esperanto Learning Dataset

This repository contains data from an experiment on Esperanto language learning with AI assistance. The dataset includes survey responses, test scores, and conversation logs between participants and AI assistants.

## Dataset Overview

The dataset comprises information from language learning experiments where participants were assigned to different treatment groups:

- **Control**: No AI assistance
- **AI-assisted**: Basic AI assistance 
- **AI-guided**: Enhanced AI assistance with structured guidance

For each participant, the dataset includes demographic information, language learning performance metrics, and conversation data with AI assistants.

## Available Files

### Original Data Files
- `iverdata.csv`: Original survey data
- `unified_conversation_data.csv`: Raw conversation data
- `unified_conversation_data.json`: JSON version of conversation data
- `nhh_esperanto_finalized_dataset.csv`: Merged and cleaned dataset

### Enhanced Dataset Files
- `nhh_esperanto_enhanced_dataset.csv`: Enhanced version with improved data quality
- `nhh_esperanto_participants.csv`: Normalized participant demographic data
- `nhh_esperanto_conversations.csv`: Structured conversation metadata
- `nhh_esperanto_messages.csv`: Individual conversation messages
- `nhh_esperanto_data_dictionary.csv`: Data dictionary explaining all variables

### Processing Scripts
- `merge_datasets.py`: Script to merge survey and conversation data
- `enhance_dataset.py`: Script to enhance the dataset quality

## Data Structure

### Participant Data
Key demographic variables for each participant:
- `participant_id`: Unique identifier for each participant
- `gender`: Participant gender
- `age`: Age range of participant
- `yearincollege`: Year in college
- `faculty`: Academic faculty/department
- `languages`: Number of languages known
- `AIfamiliar`: Familiarity with AI
- `AIsubscription`: Whether participant has an AI subscription

### Experimental Data
Key experimental variables:
- `treatment_clean`: Treatment group (Control, AI-assisted, AI-guided)
- `Session`: Experimental session identifier
- `testscore`: Score on Esperanto language test
- `esperanto_accuracy`: Accuracy on practice questions
- `esperanto_practice_count`: Number of practice questions attempted

### Conversation Data
Conversation metrics and content:
- `conversation_id`: Unique identifier for each conversation
- `MessageCount`: Total number of messages exchanged
- `UserMessageCount`: Number of messages from the user
- `AIMessageCount`: Number of messages from the AI
- `ConversationDuration`: Duration of conversation in seconds
- `conversation_turn_count`: Number of user-AI exchanges
- `esperanto_usage_score`: Score for Esperanto usage (0-100)
- `ai_helpfulness_score`: Measure of AI helpfulness (0-100)
- `conversation_focus`: Primary focus of the conversation

## Data Quality Enhancements

The enhanced dataset improves upon the original in several ways:

1. **Improved User Identification**: Better matching between survey responses and conversations with confidence scores

2. **Esperanto Language Cleanup**: Standardized spelling and formatting of Esperanto text

3. **Enhanced Metrics**: New computed variables for deeper analysis:
   - Esperanto usage scores
   - Conversation complexity measures
   - AI helpfulness metrics
   - Conversation turn analysis

4. **Structured Format**: Normalized relational structure with participant, conversation, and message tables

5. **Data Dictionary**: Comprehensive documentation of all variables

## Using the Dataset

For most analyses, the enhanced dataset files provide the most usable data:

```python
import pandas as pd

# Load enhanced dataset
enhanced_data = pd.read_csv('nhh_esperanto_enhanced_dataset.csv')

# Load participant data
participants = pd.read_csv('nhh_esperanto_participants.csv')

# Load conversation data
conversations = pd.read_csv('nhh_esperanto_conversations.csv')
messages = pd.read_csv('nhh_esperanto_messages.csv')

# Example: Compare test scores across treatment groups
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10, 6))
sns.boxplot(x='treatment_clean', y='testscore', data=enhanced_data)
plt.title('Test Scores by Treatment Group')
plt.xlabel('Treatment')
plt.ylabel('Test Score')
plt.show()
```

## Citation

Please cite this dataset as:

```
[Citation information to be added by repository owner]
```

## License

[License information to be added by repository owner]