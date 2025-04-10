#!/usr/bin/env python3
"""
Esperanto Learning Dataset Enhancement Script

This script improves the finalized dataset by:
1. Fixing encoding and formatting issues
2. Improving user identification and deduplication
3. Cleaning up Esperanto text fields 
4. Creating additional metrics for analysis
5. Restructuring the dataset to be more analysis-friendly
6. Adding documentation for variables

The script outputs multiple files:
- Enhanced full dataset
- Participant metadata file
- Conversation data in structured format
- Data dictionary
"""

import pandas as pd
import numpy as np
import re
import json
import logging
from datetime import datetime
import difflib
from typing import Dict, List, Optional, Tuple, Union

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# File paths
INPUT_PATH = 'nhh_esperanto_finalized_dataset.csv'
OUTPUT_PATH = 'nhh_esperanto_enhanced_dataset.csv'
PARTICIPANTS_PATH = 'nhh_esperanto_participants.csv'
CONVERSATIONS_PATH = 'nhh_esperanto_conversations.csv'
MESSAGES_PATH = 'nhh_esperanto_messages.csv'
DATA_DICTIONARY_PATH = 'nhh_esperanto_data_dictionary.csv'

# Constants
ESPERANTO_COMMON_WORDS = {
    'estas': 'is',
    'lernas': 'learns',
    'flugas': 'flies',
    'dormas': 'sleeps',
    'viro': 'man',
    'virino': 'woman',
    'kato': 'cat',
    'hundo': 'dog',
    'knabo': 'boy',
    'granda': 'big',
    'malgranda': 'small',
    'bona': 'good',
    'malbona': 'bad',
    'rapida': 'fast',
    'bela': 'beautiful',
    'la': 'the',
    'kaj': 'and',
    'ne': 'not',
    'sed': 'but',
    'aŭ': 'or',
    'en': 'in',
    'sur': 'on',
    'sub': 'under',
    'antaŭ': 'before',
    'post': 'after',
    'al': 'to',
    'de': 'from',
    'kun': 'with',
    'mi': 'I',
    'vi': 'you',
    'li': 'he',
    'ŝi': 'she',
    'ĝi': 'it',
    'ni': 'we',
    'ili': 'they',
    'mia': 'my',
    'via': 'your',
    'lia': 'his',
    'ŝia': 'her',
    'ĝia': 'its',
    'nia': 'our',
    'ilia': 'their',
    'birdo': 'bird',
    'instruisto': 'teacher',
    'lernanto': 'student',
    'amiko': 'friend',
    'amikoj': 'friends',
    'libro': 'book',
    'tablo': 'table',
    'seĝo': 'chair',
    'domo': 'house',
    'urbo': 'city',
    'lando': 'country',
    'akvo': 'water',
    'pano': 'bread',
    'manĝi': 'to eat',
    'trinki': 'to drink',
    'paroli': 'to speak',
    'skribi': 'to write',
    'legi': 'to read',
    'vidi': 'to see',
    'aŭdi': 'to hear',
    'ami': 'to love',
    'diri': 'to say',
    'fari': 'to do/make',
    'iri': 'to go',
    'veni': 'to come',
    'scii': 'to know',
    'voli': 'to want',
    'povi': 'can/to be able to',
    'devi': 'must/to have to',
    'mateno': 'morning',
    'tago': 'day',
    'vespero': 'evening',
    'nokto': 'night',
    'suno': 'sun',
    'luno': 'moon',
    'stelo': 'star',
    'papero': 'paper',
    'plumo': 'pen',
    'telefono': 'telephone',
    'apartamento': 'apartment',
}

# Data dictionary for key columns
COLUMN_DESCRIPTIONS = {
    # Identifiers
    'final_id': 'Unique identifier for each record in the dataset',
    'participant_id': 'Consistent identifier for each participant',
    'UserID': 'Original user identifier from various sources',
    'UserID_Source': 'Source of the user identifier (Explicit, Timestamp, Auto-generated)',
    'ResponseId': 'Original survey response identifier',
    'conversation_id': 'Identifier for the conversation (if matched)',
    'MatchMethod': 'Method used to match survey to conversation (ExplicitID, Timestamp)',
    'match_confidence': 'Confidence score (0-100) for matched records based on timestamp proximity',
    
    # Demographics
    'gender': 'Participant gender',
    'age': 'Participant age range',
    'yearincollege': 'Participant year in college',
    'faculty': 'Participant faculty/department',
    'gpa': 'Participant GPA range',
    'AIfamiliar': 'Participant familiarity with AI',
    'AIsubscription': 'Whether participant has an AI subscription',
    'languages': 'Number of languages participant knows',
    'language_text': 'Languages participant knows (text)',
    
    # Experiment details
    'StartDate': 'Time when participant started the survey',
    'EndDate': 'Time when participant completed the survey',
    'Durationinseconds': 'Duration of survey completion in seconds',
    'Session': 'Session identifier',
    'treatment': 'Experiment treatment group',
    'treatment_clean': 'Standardized treatment group (Control, AI-assisted, AI-guided)',
    'testscore': 'Test score in the Esperanto task',
    
    # Conversation metrics
    'MessageCount': 'Total number of messages in the conversation',
    'UserMessageCount': 'Number of messages from the user',
    'AIMessageCount': 'Number of messages from the AI',
    'AverageUserMessageLength': 'Average length of user messages in characters',
    'AverageAIMessageLength': 'Average length of AI messages in characters',
    'ConversationDuration': 'Duration of conversation in seconds',
    'ConversationDurationMinutes': 'Duration of conversation in minutes',
    'MessageRatio': 'Ratio of user messages to AI messages',
    
    # Data quality flags
    'HasMatch': 'Whether survey has a matching conversation',
    'is_duplicate': 'Whether record is a suspected duplicate',
    'data_status': 'Status of record (Complete, Missing conversation, Duplicate)',
    
    # Enhanced fields
    'esperanto_practice_count': 'Count of Esperanto practice questions attempted',
    'esperanto_correct_count': 'Count of correct Esperanto practice questions',
    'esperanto_accuracy': 'Accuracy rate on Esperanto practice questions',
    'conversation_turn_count': 'Number of conversation turns (user-AI exchanges)',
    'conversation_complexity': 'Estimated complexity of conversation (1-5 scale)',
    'esperanto_usage_score': 'Score for Esperanto usage in conversation (0-100)',
    'ai_helpfulness_score': 'Score for AI helpfulness in the conversation (0-100)',
    'conversation_focus': 'Primary focus of the conversation (vocabulary, grammar, practice, etc.)',
}


def load_dataset() -> pd.DataFrame:
    """
    Load the finalized dataset for enhancement.
    
    Returns:
        DataFrame with the finalized dataset
    """
    logger.info(f"Loading dataset from {INPUT_PATH}")
    try:
        data = pd.read_csv(INPUT_PATH, low_memory=False)
        logger.info(f"Loaded {len(data)} records")
        return data
    except Exception as e:
        logger.error(f"Error loading dataset: {str(e)}")
        raise


def fix_encoding_issues(data: pd.DataFrame) -> pd.DataFrame:
    """
    Fix encoding issues in the dataset.
    
    Args:
        data: DataFrame with the dataset
        
    Returns:
        DataFrame with fixed encoding
    """
    logger.info("Fixing encoding issues")
    fixed_data = data.copy()
    
    # Identify columns likely to have text content
    text_columns = []
    for col in fixed_data.columns:
        if fixed_data[col].dtype == 'object':
            # Sample non-null values
            sample = fixed_data[col].dropna().head(10).astype(str)
            # Check if column contains text content
            if any(len(val) > 3 for val in sample):
                text_columns.append(col)
    
    logger.info(f"Found {len(text_columns)} text columns")
    
    # Fix common encoding issues in text columns
    for col in text_columns:
        if col in fixed_data.columns:
            # Fix only string columns
            if fixed_data[col].dtype == 'object':
                # Replace common escape sequences
                fixed_data[col] = fixed_data[col].astype(str).apply(
                    lambda x: x.replace('\\ue203', 'ĉ')
                     .replace('\\ue204', 'ĝ')
                     .replace('\\ue205', 'ĥ')
                     .replace('\\ue206', 'ĵ')
                     .replace('\\ue209', 'ŝ')
                     .replace('\\ue20d', 'ŭ')
                     .replace('\\n', '\n')
                     .replace('\\r', '')
                     .replace('\\t', '    ')
                     .replace('\\"', '"')
                     .replace("\\'", "'")
                     .replace('nan', '')
                     if x and not pd.isna(x) else ''
                )
    
    # Special treatment for conversation messages
    if 'conversation_messages' in fixed_data.columns:
        fixed_data['conversation_messages'] = fixed_data['conversation_messages'].apply(
            lambda x: re.sub(r'\\u[0-9a-f]{4}', lambda m: chr(int(m.group(0)[2:], 16)), str(x))
            if not pd.isna(x) else ''
        )
    
    return fixed_data


def clean_esperanto_text(text: str) -> str:
    """
    Clean and standardize Esperanto text.
    
    Args:
        text: Esperanto text to clean
        
    Returns:
        Cleaned text
    """
    if pd.isna(text) or not text:
        return ""
    
    # Convert to string if not already
    text = str(text)
    
    # Replace common misspellings
    corrections = {
        'Eseranto': 'Esperanto',
        'rspida': 'rapida',
        'bele bele': 'bele',
        'juan': 'juna',
        'pero': 'sed',
    }
    
    for wrong, correct in corrections.items():
        text = text.replace(wrong, correct)
    
    # Fix capitalization for sentence starts
    text = re.sub(r'^([a-z])', lambda m: m.group(1).upper(), text)
    text = re.sub(r'([.!?]\s+)([a-z])', lambda m: m.group(1) + m.group(2).upper(), text)
    
    # Fix spacing around punctuation
    text = re.sub(r'\s+([.,;:!?])', r'\1', text)
    
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def enhance_user_identification(data: pd.DataFrame) -> pd.DataFrame:
    """
    Improve user identification by cross-referencing different ID fields.
    
    Args:
        data: DataFrame with the dataset
        
    Returns:
        DataFrame with enhanced user identification
    """
    logger.info("Enhancing user identification")
    enhanced_data = data.copy()
    
    # Create a more robust participant_id field
    id_sources = ['UserID', 'ResponseId', 'IPAddress']
    
    # Normalize existing participant_id
    if 'participant_id' in enhanced_data.columns:
        enhanced_data['participant_id_original'] = enhanced_data['participant_id']
    
    # Create a combined ID source string for fuzzy matching
    enhanced_data['id_composite'] = enhanced_data.apply(
        lambda row: ' '.join([str(row[col]) for col in id_sources 
                             if col in row and not pd.isna(row[col])]),
        axis=1
    )
    
    # Group by id_composite to identify potential matches
    id_groups = {}
    for idx, row in enhanced_data.iterrows():
        composite = row['id_composite']
        if not composite:
            continue
            
        # Check if this composite ID is similar to any existing group
        best_match = None
        best_score = 0
        
        for existing_id in id_groups.keys():
            # Use difflib to find similarity score
            score = difflib.SequenceMatcher(None, composite, existing_id).ratio()
            if score > 0.8 and score > best_score:  # 80% similarity threshold
                best_match = existing_id
                best_score = score
        
        if best_match:
            id_groups[best_match].append(idx)
        else:
            id_groups[composite] = [idx]
    
    # Assign consistent participant IDs
    enhanced_data['participant_id_enhanced'] = None
    participant_counter = 1
    
    for _, indices in id_groups.items():
        # Create a new participant ID
        participant_id = f"P{participant_counter:03d}"
        
        # Assign to all rows in this group
        for idx in indices:
            enhanced_data.at[idx, 'participant_id_enhanced'] = participant_id
            
        participant_counter += 1
    
    # For rows that didn't get assigned, create a unique ID
    unassigned = enhanced_data[pd.isna(enhanced_data['participant_id_enhanced'])].index
    for idx in unassigned:
        enhanced_data.at[idx, 'participant_id_enhanced'] = f"P{participant_counter:03d}"
        participant_counter += 1
    
    # Update duplicate flag based on enhanced identification
    enhanced_data['is_duplicate_enhanced'] = False
    
    # Find duplicates within each participant
    for participant_id in enhanced_data['participant_id_enhanced'].unique():
        participant_rows = enhanced_data[enhanced_data['participant_id_enhanced'] == participant_id]
        
        if len(participant_rows) <= 1:
            continue
            
        # Sort by timestamp if available
        if 'start_time_unix' in participant_rows.columns:
            participant_rows = participant_rows.sort_values('start_time_unix')
            
        # Mark all but the first occurrence as duplicates
        for idx in participant_rows.index[1:]:
            enhanced_data.at[idx, 'is_duplicate_enhanced'] = True
    
    # Add a confidence score for the enhanced ID
    enhanced_data['participant_id_confidence'] = enhanced_data.apply(
        lambda row: 100 if row['UserID_Source'] == 'Explicit' else
                   80 if row['UserID_Source'] == 'Timestamp' else
                   60 if not pd.isna(row['ResponseId']) else
                   40,
        axis=1
    )
    
    # Set the final participant_id to the enhanced one
    enhanced_data['participant_id'] = enhanced_data['participant_id_enhanced']
    
    # Drop temporary columns
    enhanced_data = enhanced_data.drop(columns=['id_composite', 'participant_id_enhanced'])
    
    return enhanced_data


def parse_conversations(data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Parse conversation data into a structured format.
    
    Args:
        data: DataFrame with the dataset
        
    Returns:
        Tuple of (conversations_df, messages_df)
    """
    logger.info("Parsing conversations into structured format")
    
    # Extract conversations
    conversations = []
    messages = []
    
    for idx, row in data.iterrows():
        if pd.isna(row['conversation_id']) or not row['conversation_id']:
            continue
            
        # Create conversation record
        conv_data = {
            'conversation_id': row['conversation_id'],
            'participant_id': row['participant_id'],
            'create_time': row['create_time'] if 'create_time' in row else None,
            'message_count': row['MessageCount'] if 'MessageCount' in row else 0,
            'user_message_count': row['UserMessageCount'] if 'UserMessageCount' in row else 0,
            'ai_message_count': row['AIMessageCount'] if 'AIMessageCount' in row else 0,
            'conversation_duration': row['ConversationDuration'] if 'ConversationDuration' in row else 0,
            'treatment': row['treatment_clean'] if 'treatment_clean' in row else row['treatment'] if 'treatment' in row else None,
        }
        
        conversations.append(conv_data)
        
        # Parse individual messages
        if 'conversation_messages' in row and not pd.isna(row['conversation_messages']):
            message_text = str(row['conversation_messages'])
            
            # Split into individual messages
            message_pattern = r'(USER|ASSISTANT|SYSTEM):\s*(.*?)(?=(?:USER|ASSISTANT|SYSTEM):|$)'
            message_matches = re.findall(message_pattern, message_text, re.DOTALL)
            
            msg_id = 0
            for role, content in message_matches:
                # Skip empty messages
                content = content.strip()
                if not content:
                    continue
                    
                # Create message record
                msg_data = {
                    'message_id': f"{row['conversation_id']}_{msg_id:03d}",
                    'conversation_id': row['conversation_id'],
                    'participant_id': row['participant_id'],
                    'message_index': msg_id,
                    'role': role.lower(),
                    'content': content.strip(),
                    'content_length': len(content.strip()),
                    'is_esperanto': is_esperanto_text(content),
                }
                
                messages.append(msg_data)
                msg_id += 1
    
    # Create DataFrames
    conversations_df = pd.DataFrame(conversations)
    messages_df = pd.DataFrame(messages)
    
    return conversations_df, messages_df


def is_esperanto_text(text: str) -> bool:
    """
    Determine if text is likely to be in Esperanto.
    
    Args:
        text: Text to analyze
        
    Returns:
        True if text is likely Esperanto, False otherwise
    """
    if pd.isna(text) or not text:
        return False
        
    # Convert to lowercase and split into words
    words = re.findall(r'\b\w+\b', text.lower())
    
    if not words:
        return False
        
    # Count Esperanto words
    esperanto_word_count = sum(1 for word in words if word in ESPERANTO_COMMON_WORDS)
    
    # Check for Esperanto-specific characters
    esperanto_chars = sum(1 for c in text if c in 'ĉĝĥĵŝŭĈĜĤĴŜŬ')
    
    # Calculate score based on word match and special characters
    score = (esperanto_word_count / len(words)) + (esperanto_chars > 0) * 0.3
    
    return score > 0.2  # 20% threshold for identification


def compute_enhanced_metrics(data: pd.DataFrame, messages_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute enhanced metrics for analysis.
    
    Args:
        data: DataFrame with the dataset
        messages_df: DataFrame with structured message data
        
    Returns:
        DataFrame with enhanced metrics
    """
    logger.info("Computing enhanced metrics")
    enhanced_data = data.copy()
    
    # Count Esperanto practice questions attempted and correct
    esperanto_cols = [col for col in enhanced_data.columns if re.match(r'Q\d+_c$', col)]
    
    # Initialize columns
    enhanced_data['esperanto_practice_count'] = 0
    enhanced_data['esperanto_correct_count'] = 0
    enhanced_data['esperanto_accuracy'] = 0.0
    
    # Count non-missing values and correct answers (1.0)
    for idx, row in enhanced_data.iterrows():
        attempted = 0
        correct = 0
        
        for col in esperanto_cols:
            if col in row and not pd.isna(row[col]):
                attempted += 1
                if row[col] == 1.0:
                    correct += 1
        
        enhanced_data.at[idx, 'esperanto_practice_count'] = attempted
        enhanced_data.at[idx, 'esperanto_correct_count'] = correct
        
        if attempted > 0:
            enhanced_data.at[idx, 'esperanto_accuracy'] = correct / attempted
    
    # Compute conversation turn count and complexity
    if not messages_df.empty:
        # Group messages by conversation_id
        conversation_metrics = {}
        
        for conv_id, group in messages_df.groupby('conversation_id'):
            # Count turns (user message followed by AI message)
            user_messages = group[group['role'] == 'user'].sort_values('message_index')
            ai_messages = group[group['role'] == 'assistant'].sort_values('message_index')
            
            # A turn is a user message that gets an AI response
            turns = 0
            for i, user_msg in user_messages.iterrows():
                # Find AI messages that follow this user message
                follow_ai = ai_messages[ai_messages['message_index'] > user_msg['message_index']]
                if not follow_ai.empty:
                    turns += 1
            
            # Calculate average message length as a proxy for complexity
            avg_message_length = group['content_length'].mean()
            
            # Calculate percentage of messages with Esperanto content
            esperanto_msg_count = group['is_esperanto'].sum()
            esperanto_percentage = (esperanto_msg_count / len(group)) * 100 if len(group) > 0 else 0
            
            # Estimate conversation complexity (1-5 scale)
            # Based on turn count, message length, and variety of content
            unique_words = set()
            for content in group['content']:
                words = re.findall(r'\b\w+\b', str(content).lower())
                unique_words.update(words)
                
            vocabulary_size = len(unique_words)
            
            # Calculate complexity score
            complexity = 1.0
            complexity += min(2.0, turns / 5)  # Up to 2 points for turns
            complexity += min(1.0, avg_message_length / 200)  # Up to 1 point for message length
            complexity += min(1.0, vocabulary_size / 100)  # Up to 1 point for vocabulary
            
            # Store metrics
            conversation_metrics[conv_id] = {
                'conversation_turn_count': turns,
                'conversation_complexity': min(5.0, complexity),
                'esperanto_usage_score': esperanto_percentage,
            }
        
        # Add metrics to the main dataframe
        for idx, row in enhanced_data.iterrows():
            if pd.isna(row['conversation_id']):
                continue
                
            conv_id = row['conversation_id']
            if conv_id in conversation_metrics:
                for metric, value in conversation_metrics[conv_id].items():
                    enhanced_data.at[idx, metric] = value
    
    # Analyze AI helpfulness based on conversation metrics
    enhanced_data['ai_helpfulness_score'] = 0.0
    
    for idx, row in enhanced_data.iterrows():
        if pd.isna(row['conversation_id']):
            continue
            
        # Factors that indicate helpfulness
        score = 50.0  # Start with a neutral score
        
        # Adjust based on conversation metrics
        if not pd.isna(row.get('conversation_turn_count')):
            # More turns indicate more interaction
            score += min(20, row['conversation_turn_count'] * 2)
            
        if not pd.isna(row.get('AverageAIMessageLength')) and row['AverageAIMessageLength'] > 0:
            # Longer AI messages may indicate more helpful explanations
            # But penalize extremely long messages
            length_factor = min(row['AverageAIMessageLength'] / 100, 2)
            score += length_factor * 10
            
        if not pd.isna(row.get('MessageRatio')) and row['MessageRatio'] > 0:
            # Lower ratio (more AI messages per user message) may indicate helpfulness
            if row['MessageRatio'] < 1:
                score += 10
            elif row['MessageRatio'] > 2:
                score -= 10
                
        if not pd.isna(row.get('esperanto_usage_score')):
            # Higher Esperanto usage indicates more on-task interaction
            score += row['esperanto_usage_score'] * 0.2
                
        # Cap score at 0-100
        enhanced_data.at[idx, 'ai_helpfulness_score'] = max(0, min(100, score))
    
    # Determine the primary focus of each conversation
    enhanced_data['conversation_focus'] = None
    
    for idx, row in enhanced_data.iterrows():
        if pd.isna(row['conversation_id']) or 'conversation_messages' not in row or pd.isna(row['conversation_messages']):
            continue
            
        # Extract keywords from conversation
        text = str(row['conversation_messages']).lower()
        
        # Check for common focus areas
        focus_indicators = {
            'vocabulary': ['word', 'vocabulary', 'vortoj', 'vortaro', 'mean', 'define', 'definition', 'translate'],
            'grammar': ['grammar', 'grammatical', 'sentence', 'structure', 'verb', 'noun', 'adjective', 'adverb', 'tense'],
            'practice': ['practice', 'exercise', 'quiz', 'question', 'answer', 'correct', 'wrong', 'test'],
            'conversation': ['speak', 'talk', 'chat', 'conversation', 'dialogue', 'example'],
            'pronunciation': ['pronounce', 'pronunciation', 'sound', 'accent', 'speak'],
            'explanation': ['explain', 'explanation', 'understand', 'meaning', 'why', 'how'],
            'clarification': ['confused', 'unclear', 'clarify', 'help', 'I don\'t understand'],
        }
        
        # Count indicators for each focus area
        focus_counts = {focus: 0 for focus in focus_indicators}
        for focus, indicators in focus_indicators.items():
            for indicator in indicators:
                focus_counts[focus] += text.count(indicator)
        
        # Determine primary focus
        primary_focus = max(focus_counts, key=focus_counts.get)
        
        # Only assign if we have a meaningful signal
        if focus_counts[primary_focus] > 1:
            enhanced_data.at[idx, 'conversation_focus'] = primary_focus
    
    return enhanced_data


def create_data_dictionary() -> pd.DataFrame:
    """
    Create a data dictionary for the enhanced dataset.
    
    Returns:
        DataFrame with data dictionary
    """
    logger.info("Creating data dictionary")
    
    # Prepare data dictionary entries
    dictionary_entries = []
    
    for column, description in COLUMN_DESCRIPTIONS.items():
        dictionary_entries.append({
            'column_name': column,
            'description': description,
            'category': column.split('_')[0] if '_' in column else 'Other',
        })
    
    # Create DataFrame
    dictionary_df = pd.DataFrame(dictionary_entries)
    
    # Sort by category and column name
    dictionary_df = dictionary_df.sort_values(['category', 'column_name'])
    
    return dictionary_df


def split_dataset(data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split the dataset into participant and experimental data.
    
    Args:
        data: Enhanced DataFrame
        
    Returns:
        Tuple of (participants_df, experiments_df)
    """
    logger.info("Splitting dataset into participant and experimental data")
    
    # Define demographic columns to include in participant data
    demographic_cols = [
        'participant_id', 'gender', 'age', 'yearincollege', 'faculty', 'gpa',
        'AIfamiliar', 'AIsubscription', 'languages', 'language_text',
    ]
    
    # Create participant data
    participants_df = data[demographic_cols].drop_duplicates(subset=['participant_id']).copy()
    
    # Keep only the first occurrence for each participant
    participants_df = participants_df.groupby('participant_id').first().reset_index()
    
    # Ensure experiments_df still has participant_id but not the other demographic data
    experiments_df = data.drop(columns=[col for col in demographic_cols if col != 'participant_id']).copy()
    
    return participants_df, experiments_df


def main():
    """Main function to run the enhancement process"""
    logger.info("Starting dataset enhancement")
    
    try:
        # Load dataset
        data = load_dataset()
        
        # Fix encoding issues
        data = fix_encoding_issues(data)
        
        # Enhance user identification
        data = enhance_user_identification(data)
        
        # Parse conversations
        conversations_df, messages_df = parse_conversations(data)
        
        # Compute enhanced metrics
        enhanced_data = compute_enhanced_metrics(data, messages_df)
        
        # Create data dictionary
        dictionary_df = create_data_dictionary()
        
        # Split into participant and experimental data
        participants_df, experiments_df = split_dataset(enhanced_data)
        
        # Save outputs
        enhanced_data.to_csv(OUTPUT_PATH, index=False)
        participants_df.to_csv(PARTICIPANTS_PATH, index=False)
        conversations_df.to_csv(CONVERSATIONS_PATH, index=False)
        messages_df.to_csv(MESSAGES_PATH, index=False)
        dictionary_df.to_csv(DATA_DICTIONARY_PATH, index=False)
        
        logger.info(f"Enhanced dataset saved to {OUTPUT_PATH}")
        logger.info(f"Participant data saved to {PARTICIPANTS_PATH}")
        logger.info(f"Conversation data saved to {CONVERSATIONS_PATH}")
        logger.info(f"Message data saved to {MESSAGES_PATH}")
        logger.info(f"Data dictionary saved to {DATA_DICTIONARY_PATH}")
        
        # Print summary
        logger.info("Enhancement summary:")
        logger.info(f"  - Records in enhanced dataset: {len(enhanced_data)}")
        logger.info(f"  - Unique participants identified: {len(participants_df)}")
        logger.info(f"  - Conversations processed: {len(conversations_df)}")
        logger.info(f"  - Individual messages extracted: {len(messages_df)}")
        
    except Exception as e:
        logger.error(f"Error in enhancement process: {str(e)}")
        raise


if __name__ == "__main__":
    main()