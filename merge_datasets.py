#!/usr/bin/env python3
"""
Esperanto Learning Dataset Alignment Script

This script aligns and merges survey data from iverdata.csv with conversation data 
from the unified_conversation_data CSV/JSON files, based on user IDs and timestamps.
It also creates a schedule_sessions.csv file if it doesn't exist.

The script performs the following tasks:
1. Loads survey data from iverdata.csv
2. Loads conversation data from unified_conversation_data.csv
3. Extracts UserIDs from conversation logs
4. Matches survey responses to conversations based on timestamps and IDs
5. Creates a schedule_sessions.csv file containing session dates
6. Outputs an enriched dataset with aligned data
"""

import os
import re
import json
import pandas as pd
import numpy as np
from datetime import datetime
import pytz
import logging
from typing import Dict, List, Tuple, Union, Optional

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define file paths
IVERDATA_PATH = 'iverdata.csv'
CONVERSATION_DATA_PATH = 'unified_conversation_data.csv'
OUTPUT_PATH = 'aligned_unified_conversation_data.csv'
SCHEDULE_SESSIONS_PATH = 'schedule_sessions.csv'

# Define constants
USER_ID_PATTERN = r'(\d{2})(\d{2})(\d{4})_(\d{4})_Participant(\d+)'
ALTERNATIVE_ID_PATTERN = r'ID(?:\s+is)?\s*(?::|-)?\s*(\d+)'
TIMESTAMP_TOLERANCE = 86400  # 24 hours in seconds


def convert_qualtrics_time_to_unix(time_str: str) -> float:
    """
    Convert Qualtrics timestamp to Unix timestamp.
    
    Args:
        time_str: Timestamp string from Qualtrics (format MM/DD/YYYY HH:MM)
        
    Returns:
        Unix timestamp (seconds since epoch)
    """
    try:
        # Parse Qualtrics timestamp format
        dt = datetime.strptime(time_str, '%m/%d/%Y %H:%M')
        # Convert to UTC
        dt_utc = pytz.timezone('UTC').localize(dt)
        # Convert to Unix timestamp
        return dt_utc.timestamp()
    except Exception as e:
        logger.error(f"Error converting time '{time_str}': {str(e)}")
        return float('nan')


def load_survey_data() -> pd.DataFrame:
    """
    Load survey data from iverdata.csv and prepare it for merging.
    
    Returns:
        DataFrame with survey data
    """
    logger.info(f"Loading survey data from {IVERDATA_PATH}")
    try:
        survey_data = pd.read_csv(IVERDATA_PATH)
        
        # Convert StartDate and EndDate to Unix timestamps
        survey_data['start_time_unix'] = survey_data['StartDate'].apply(convert_qualtrics_time_to_unix)
        survey_data['end_time_unix'] = survey_data['EndDate'].apply(convert_qualtrics_time_to_unix)
        
        logger.info(f"Loaded {len(survey_data)} survey responses")
        return survey_data
    except Exception as e:
        logger.error(f"Error loading survey data: {str(e)}")
        raise


def load_conversation_data() -> pd.DataFrame:
    """
    Load conversation data from unified_conversation_data.csv.
    
    Returns:
        DataFrame with conversation data
    """
    logger.info(f"Loading conversation data from {CONVERSATION_DATA_PATH}")
    try:
        conv_data = pd.read_csv(CONVERSATION_DATA_PATH)
        logger.info(f"Loaded {len(conv_data)} conversations")
        return conv_data
    except Exception as e:
        logger.error(f"Error loading conversation data: {str(e)}")
        raise


def extract_first_user_message(conversation_id: str, message_data: pd.DataFrame) -> Optional[str]:
    """
    Extract the first user message from the conversation data.
    
    Args:
        conversation_id: ID of the conversation
        message_data: DataFrame containing all messages
        
    Returns:
        First user message content or None if not found
    """
    try:
        # Filter messages for this conversation where author_role is 'user'
        user_messages = message_data[
            (message_data['conversation_id'] == conversation_id) & 
            (message_data['author_role'] == 'user')
        ]
        
        # Sort by create_time to get the first message
        if not user_messages.empty:
            # Return the content of the first user message
            first_msg = user_messages.iloc[0]['message_content']
            
            # Handle array-like content format (e.g., "['My ID is 05122024_1600_2']")
            if first_msg.startswith("['") and first_msg.endswith("']"):
                # Extract content between quotes
                return first_msg[2:-2]
            return first_msg
            
    except Exception as e:
        logger.debug(f"Could not extract first message for {conversation_id}: {str(e)}")
    
    return None


def extract_user_id_from_message(message: str) -> Optional[str]:
    """
    Extract user ID from message text.
    
    Args:
        message: Message text to search for user ID
        
    Returns:
        User ID string or None if not found
    """
    if not message:
        return None
    
    # Try standard format: DDMMYYYY_HHMM_Participant#
    match = re.search(USER_ID_PATTERN, message)
    if match:
        day, month, year, time, participant = match.groups()
        return f"{day}{month}{year}_{time}_Participant{participant}"
    
    # Try alternative format: "ID is 12345", "my ID: 12345", etc.
    alt_match = re.search(ALTERNATIVE_ID_PATTERN, message)
    if alt_match:
        return alt_match.group(1)
    
    # Try to find any mention of Participant followed by a number
    participant_match = re.search(r'[Pp]articipant\s*(\d+)', message)
    if participant_match:
        return f"Participant{participant_match.group(1)}"
    
    # Look for common date formats that might indicate a session time
    date_match = re.search(r'(\d{1,2})[-/](\d{1,2})[-/](\d{2,4}).*?(\d{1,2})[:.h](\d{1,2})', message, re.IGNORECASE)
    if date_match:
        day, month, year, hour, minute = date_match.groups()
        if len(year) == 2:
            year = f"20{year}"  # Assume 21st century
        return f"{day}{month}{year}_{hour}{minute}"
    
    # Try to find any decimal number that could be an ID
    id_match = re.search(r'\b(\d{1,4})\b', message)
    if id_match:
        return id_match.group(1)
    
    return None


def create_schedule_sessions() -> pd.DataFrame:
    """
    Create or load schedule_sessions.csv mapping session times to dates.
    
    Returns:
        DataFrame with session schedule information
    """
    if os.path.exists(SCHEDULE_SESSIONS_PATH):
        logger.info(f"Loading existing session schedule from {SCHEDULE_SESSIONS_PATH}")
        return pd.read_csv(SCHEDULE_SESSIONS_PATH)
    
    logger.info("Creating new session schedule file")
    
    # Load survey data to extract session dates
    survey_data = pd.read_csv(IVERDATA_PATH)
    
    # Extract unique dates
    dates = pd.to_datetime(survey_data['StartDate'].apply(
        lambda x: x.split(' ')[0]), format='%m/%d/%Y').unique()
    
    # Create session mapping
    sessions = []
    for i, date in enumerate(sorted(dates)):
        session_id = f"Session {i+1}"
        sessions.append({
            'SessionID': session_id,
            'Date': date.strftime('%m/%d/%Y'),
            'StartTime': '09:00',  # Default start time
            'EndTime': '17:00'     # Default end time
        })
    
    # Create DataFrame and save
    schedule_df = pd.DataFrame(sessions)
    schedule_df.to_csv(SCHEDULE_SESSIONS_PATH, index=False)
    logger.info(f"Created session schedule with {len(sessions)} sessions")
    
    return schedule_df


def assign_session_to_response(response_time: str, schedule: pd.DataFrame) -> str:
    """
    Assign a session ID to a survey response based on its timestamp.
    
    Args:
        response_time: StartDate from survey response
        schedule: DataFrame with session schedule
        
    Returns:
        Session ID string
    """
    response_date = response_time.split(' ')[0]
    
    # Find matching session
    matching_sessions = schedule[schedule['Date'] == response_date]
    
    if len(matching_sessions) > 0:
        return matching_sessions.iloc[0]['SessionID']
    else:
        return "Unknown Session"


def match_by_explicit_id(survey_data: pd.DataFrame, conv_data: pd.DataFrame, 
                       unique_conversation_ids: list) -> pd.DataFrame:
    """
    Match survey responses to conversations based on explicit user IDs.
    
    Args:
        survey_data: DataFrame with survey responses
        conv_data: DataFrame with conversation data
        unique_conversation_ids: List of unique conversation IDs
        
    Returns:
        DataFrame with matched survey data
    """
    logger.info("Matching by explicit ID")
    id_matches = 0
    
    # Create copy to avoid modifying original
    result_data = survey_data.copy()
    
    # Initialize match columns
    result_data['conversation_id'] = None
    result_data['create_time'] = None
    result_data['UserID'] = None
    result_data['MatchMethod'] = None
    
    # Process each unique conversation ID
    for conv_id in unique_conversation_ids:
        # Get first user message for this conversation
        first_message = extract_first_user_message(conv_id, conv_data)
        
        # Extract user ID from message
        stated_id = extract_user_id_from_message(first_message)
        
        if not stated_id:
            continue
            
        # Get create time for this conversation
        create_time = conv_data[conv_data['conversation_id'] == conv_id]['create_time'].iloc[0]
        
        # Try to find matching survey response
        for idx, row in result_data.iterrows():
            # Check if ID appears in ResponseId or vice versa
            if (row['ResponseId'] and stated_id and 
                (stated_id in row['ResponseId'] or row['ResponseId'] in stated_id)):
                
                result_data.at[idx, 'conversation_id'] = conv_id
                result_data.at[idx, 'create_time'] = create_time
                result_data.at[idx, 'UserID'] = stated_id
                result_data.at[idx, 'MatchMethod'] = 'ExplicitID'
                id_matches += 1
                break
    
    logger.info(f"Matched {id_matches} responses by explicit ID")
    return result_data


def match_by_timestamp(unmatched_data: pd.DataFrame, conv_data: pd.DataFrame, 
                       unique_conversation_ids: list) -> pd.DataFrame:
    """
    Match survey responses to conversations based on timestamp proximity.
    
    Args:
        unmatched_data: DataFrame with unmatched survey responses
        conv_data: DataFrame with conversation data
        unique_conversation_ids: List of unique conversation IDs
        
    Returns:
        DataFrame with matched survey data
    """
    logger.info("Matching by timestamp")
    time_matches = 0
    
    # Create copy to avoid modifying original
    result_data = unmatched_data.copy()
    
    # Get unmatched surveys and sort by start time
    unmatched_surveys = result_data[result_data['conversation_id'].isna()].copy()
    unmatched_surveys = unmatched_surveys.sort_values('start_time_unix')
    
    # Get conversations not already matched and sort by create time
    matched_conv_ids = set(result_data[result_data['conversation_id'].notna()]['conversation_id'])
    unmatched_conv_ids = [conv_id for conv_id in unique_conversation_ids 
                         if conv_id not in matched_conv_ids]
    
    # Group conversations by session date
    # This allows us to prioritize matching within the same session
    conv_data_with_times = conv_data.drop_duplicates(subset=['conversation_id']).copy()
    conv_data_with_times['create_time'] = conv_data_with_times['create_time'].astype(float)
    conv_data_with_times['create_date'] = conv_data_with_times['create_time'].apply(
        lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d')
    )
    
    # Get the sessions directly from the survey data
    survey_sessions = {}
    for idx, row in unmatched_surveys.iterrows():
        if not pd.isna(row['start_time_unix']):
            date_str = datetime.fromtimestamp(row['start_time_unix']).strftime('%Y-%m-%d')
            if date_str not in survey_sessions:
                survey_sessions[date_str] = []
            survey_sessions[date_str].append(idx)
    
    # For each session date, match conversations to surveys
    for date_str, survey_indices in survey_sessions.items():
        # Get conversations from this date
        date_conversations = conv_data_with_times[
            conv_data_with_times['create_date'] == date_str
        ]
        
        # Get unmatched conversation IDs for this date
        date_conv_ids = [
            conv_id for conv_id in date_conversations['conversation_id'].tolist()
            if conv_id in unmatched_conv_ids
        ]
        
        # Create a dictionary of conversation times for this date
        conv_times = {}
        for conv_id in date_conv_ids:
            conv_subset = date_conversations[date_conversations['conversation_id'] == conv_id]
            if not conv_subset.empty:
                conv_times[conv_id] = float(conv_subset['create_time'].iloc[0])
        
        # For each survey in this session, find the best matching conversation
        for idx in survey_indices:
            if idx not in unmatched_surveys.index:
                continue
                
            survey_row = unmatched_surveys.loc[idx]
            survey_start = survey_row['start_time_unix']
            
            # Find the closest conversation by time
            best_match_id = None
            best_match_diff = float('inf')
            
            for conv_id, conv_time in conv_times.items():
                time_diff = abs(survey_start - conv_time)
                if time_diff <= TIMESTAMP_TOLERANCE and time_diff < best_match_diff:
                    best_match_id = conv_id
                    best_match_diff = time_diff
            
            # If we found a match, update the result
            if best_match_id:
                result_data.at[idx, 'conversation_id'] = best_match_id
                result_data.at[idx, 'create_time'] = conv_times[best_match_id]
                
                # Get first user message to try deriving an ID
                first_message = extract_first_user_message(best_match_id, conv_data)
                stated_id = extract_user_id_from_message(first_message)
                
                # Generate a UserID if not available from message
                if stated_id:
                    user_id = stated_id
                else:
                    # Create ID from survey timestamp
                    dt = datetime.fromtimestamp(survey_start)
                    user_id = f"{dt.day:02d}{dt.month:02d}{dt.year}_{dt.hour:02d}{dt.minute:02d}_Derived"
                
                result_data.at[idx, 'UserID'] = user_id
                result_data.at[idx, 'MatchMethod'] = 'Timestamp'
                
                # Remove the matched conversation ID
                if best_match_id in unmatched_conv_ids:
                    unmatched_conv_ids.remove(best_match_id)
                if best_match_id in conv_times:
                    del conv_times[best_match_id]
                    
                time_matches += 1
                
    # If we still have unmatched surveys, try to match them with any remaining conversations
    still_unmatched = result_data[result_data['conversation_id'].isna()]
    if not still_unmatched.empty and unmatched_conv_ids:
        logger.info(f"Attempting to match {len(still_unmatched)} remaining surveys")
        
        # Create a dictionary of all remaining conversation times
        all_conv_times = {}
        for conv_id in unmatched_conv_ids:
            conv_subset = conv_data_with_times[conv_data_with_times['conversation_id'] == conv_id]
            if not conv_subset.empty:
                all_conv_times[conv_id] = float(conv_subset['create_time'].iloc[0])
                
        # For each remaining survey, find the best match
        for idx, survey_row in still_unmatched.iterrows():
            survey_start = survey_row['start_time_unix']
            
            # Find the closest conversation by time
            best_match_id = None
            best_match_diff = float('inf')
            
            for conv_id, conv_time in all_conv_times.items():
                time_diff = abs(survey_start - conv_time)
                if time_diff <= TIMESTAMP_TOLERANCE and time_diff < best_match_diff:
                    best_match_id = conv_id
                    best_match_diff = time_diff
            
            # If we found a match, update the result
            if best_match_id:
                result_data.at[idx, 'conversation_id'] = best_match_id
                result_data.at[idx, 'create_time'] = all_conv_times[best_match_id]
                
                # Get first user message to try deriving an ID
                first_message = extract_first_user_message(best_match_id, conv_data)
                stated_id = extract_user_id_from_message(first_message)
                
                # Generate a UserID if not available from message
                if stated_id:
                    user_id = stated_id
                else:
                    # Create ID from survey timestamp
                    dt = datetime.fromtimestamp(survey_start)
                    user_id = f"{dt.day:02d}{dt.month:02d}{dt.year}_{dt.hour:02d}{dt.minute:02d}_Derived"
                
                result_data.at[idx, 'UserID'] = user_id
                result_data.at[idx, 'MatchMethod'] = 'Timestamp'
                
                # Remove the matched conversation ID
                del all_conv_times[best_match_id]
                if best_match_id in unmatched_conv_ids:
                    unmatched_conv_ids.remove(best_match_id)
                    
                time_matches += 1
    
    logger.info(f"Matched {time_matches} responses by timestamp")
    return result_data


def extract_conversation_metrics(matched_data: pd.DataFrame, conv_data: pd.DataFrame) -> pd.DataFrame:
    """
    Extract metrics from conversation data for analysis.
    
    Args:
        matched_data: DataFrame with matched survey and conversation data
        conv_data: DataFrame with raw conversation data
        
    Returns:
        DataFrame with extracted metrics
    """
    logger.info("Extracting conversation metrics")
    result_data = matched_data.copy()
    
    # Initialize metrics columns
    result_data['MessageCount'] = 0
    result_data['UserMessageCount'] = 0
    result_data['AIMessageCount'] = 0
    result_data['AverageUserMessageLength'] = 0
    result_data['AverageAIMessageLength'] = 0
    result_data['ConversationDuration'] = 0
    
    # Process each conversation
    for idx, row in result_data.iterrows():
        if pd.isna(row['conversation_id']):
            continue
            
        try:
            # Get messages for this conversation
            conv_messages = conv_data[conv_data['conversation_id'] == row['conversation_id']]
            
            if conv_messages.empty:
                continue
                
            # Filter messages by type
            user_msgs = conv_messages[conv_messages['author_role'] == 'user']['message_content'].tolist()
            ai_msgs = conv_messages[conv_messages['author_role'] == 'assistant']['message_content'].tolist()
            
            # Extract message times
            msg_times = conv_messages['create_time'].astype(float).tolist()
            
            # Process message contents to clean up formatting
            user_msgs = [msg[2:-2] if msg.startswith("['") and msg.endswith("']") else msg for msg in user_msgs]
            ai_msgs = [msg[2:-2] if msg.startswith("['") and msg.endswith("']") else msg for msg in ai_msgs]
            
            # Calculate metrics
            result_data.at[idx, 'MessageCount'] = len(user_msgs) + len(ai_msgs)
            result_data.at[idx, 'UserMessageCount'] = len(user_msgs)
            result_data.at[idx, 'AIMessageCount'] = len(ai_msgs)
            
            if user_msgs:
                avg_user_len = sum(len(msg) for msg in user_msgs) / len(user_msgs)
                result_data.at[idx, 'AverageUserMessageLength'] = avg_user_len
            
            if ai_msgs:
                avg_ai_len = sum(len(msg) for msg in ai_msgs) / len(ai_msgs)
                result_data.at[idx, 'AverageAIMessageLength'] = avg_ai_len
            
            if msg_times and len(msg_times) > 1:
                duration = max(msg_times) - min(msg_times)
                result_data.at[idx, 'ConversationDuration'] = duration
                
        except Exception as e:
            logger.error(f"Error processing conversation {row['conversation_id']}: {str(e)}")
    
    return result_data


def align_datasets() -> pd.DataFrame:
    """
    Align survey data with conversation data and create merged dataset.
    
    Returns:
        DataFrame with aligned and merged data
    """
    # Load datasets
    survey_data = load_survey_data()
    conv_data = load_conversation_data()
    
    # Create or load session schedule
    schedule = create_schedule_sessions()
    
    # Get unique conversation IDs
    unique_conversation_ids = conv_data['conversation_id'].unique().tolist()
    logger.info(f"Found {len(unique_conversation_ids)} unique conversations")
    
    # Assign session to each survey response
    logger.info("Assigning sessions to survey responses")
    survey_data['Session'] = survey_data['StartDate'].apply(
        lambda x: assign_session_to_response(x, schedule))
    
    # Match by explicit ID
    matched_data = match_by_explicit_id(survey_data, conv_data, unique_conversation_ids)
    
    # Match remaining by timestamp
    matched_data = match_by_timestamp(matched_data, conv_data, unique_conversation_ids)
    
    # Extract conversation metrics
    enriched_data = extract_conversation_metrics(matched_data, conv_data)
    
    # Calculate match statistics
    total_surveys = len(survey_data)
    matched_surveys = len(enriched_data[enriched_data['conversation_id'].notna()])
    match_percentage = (matched_surveys / total_surveys) * 100
    
    logger.info(f"Total matched: {matched_surveys} out of {total_surveys} responses ({match_percentage:.2f}%)")
    
    return enriched_data


def clean_dataset(data: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the aligned dataset by fixing data types and computing additional metrics.
    
    Args:
        data: DataFrame with aligned data
        
    Returns:
        Cleaned DataFrame
    """
    logger.info("Cleaning and finalizing dataset")
    
    # Create a copy to avoid modifying the original
    cleaned_data = data.copy()
    
    # Fix data types for numeric columns
    numeric_cols = [
        'AverageUserMessageLength', 
        'AverageAIMessageLength', 
        'ConversationDuration',
        'MessageCount',
        'UserMessageCount',
        'AIMessageCount'
    ]
    
    for col in numeric_cols:
        if col in cleaned_data.columns:
            # Convert to float to avoid integer type errors
            cleaned_data[col] = pd.to_numeric(cleaned_data[col], errors='coerce')
    
    # Calculate additional metrics
    if 'UserMessageCount' in cleaned_data.columns and 'AIMessageCount' in cleaned_data.columns:
        # Avoid division by zero
        cleaned_data['MessageRatio'] = cleaned_data.apply(
            lambda row: row['UserMessageCount'] / row['AIMessageCount'] 
            if row['AIMessageCount'] > 0 else 0, 
            axis=1
        )
    
    if 'ConversationDuration' in cleaned_data.columns:
        # Convert duration to minutes for better readability
        cleaned_data['ConversationDurationMinutes'] = cleaned_data['ConversationDuration'] / 60
    
    # Flag rows where we have a match
    cleaned_data['HasMatch'] = ~cleaned_data['conversation_id'].isna()
    
    # Make treatment variable more consistent
    if 'treatment' in cleaned_data.columns:
        # Create a clean treatment variable
        treatment_map = {
            'control': 'Control',
            'Control': 'Control', 
            'assist': 'AI-assisted',
            'AI-assisted': 'AI-assisted',
            'guided': 'AI-guided',
            'AI-guided': 'AI-guided'
        }
        
        cleaned_data['treatment_clean'] = cleaned_data['treatment'].map(treatment_map)
    
    # Clean up nullable fields
    for col in cleaned_data.columns:
        # Remove null indicator strings like 'nan' or 'None' that might be in string columns
        if cleaned_data[col].dtype == 'object':
            cleaned_data[col] = cleaned_data[col].apply(
                lambda x: None if pd.isna(x) or str(x).lower() in ['nan', 'none', ''] else x
            )
    
    # Add a match quality score based on timestamp difference
    if 'start_time_unix' in cleaned_data.columns and 'create_time' in cleaned_data.columns:
        cleaned_data['timestamp_diff'] = cleaned_data.apply(
            lambda row: abs(row['start_time_unix'] - float(row['create_time'])) 
            if not pd.isna(row['create_time']) else None,
            axis=1
        )
        
        # Convert to minutes for better readability
        cleaned_data['timestamp_diff_minutes'] = cleaned_data['timestamp_diff'] / 60
        
        # Calculate a match confidence score (0-100)
        cleaned_data['match_confidence'] = cleaned_data.apply(
            lambda row: 100 - min(99, (row['timestamp_diff'] / (TIMESTAMP_TOLERANCE / 10)))
            if not pd.isna(row['timestamp_diff']) else 0,
            axis=1
        )
        
        # Round to 2 decimal places
        cleaned_data['match_confidence'] = cleaned_data['match_confidence'].apply(
            lambda x: round(max(0, x), 2) if not pd.isna(x) else 0
        )
    
    return cleaned_data


def create_unmatched_conversations_file(conv_data: pd.DataFrame, matched_conv_ids: list) -> None:
    """
    Create a CSV file with unmatched conversations for reference.
    
    Args:
        conv_data: DataFrame with all conversation data
        matched_conv_ids: List of conversation IDs that were matched
    """
    # Get unique conversation IDs
    unique_conv_ids = conv_data['conversation_id'].unique().tolist()
    
    # Find unmatched conversation IDs
    unmatched_conv_ids = [conv_id for conv_id in unique_conv_ids if conv_id not in matched_conv_ids]
    
    if not unmatched_conv_ids:
        logger.info("All conversations have been matched")
        return
        
    # Create a dataframe with unmatched conversations
    unmatched_conv_data = []
    for conv_id in unmatched_conv_ids:
        conv_msgs = conv_data[conv_data['conversation_id'] == conv_id]
        if not conv_msgs.empty:
            first_msg = conv_msgs.iloc[0]
            create_time = first_msg['create_time']
            
            # Try to extract useful information
            user_msgs = conv_msgs[conv_msgs['author_role'] == 'user']
            first_user_msg = ""
            if not user_msgs.empty:
                content = user_msgs.iloc[0]['message_content']
                if content.startswith("['") and content.endswith("']"):
                    first_user_msg = content[2:-2]
                else:
                    first_user_msg = content
            
            # Add to the list
            unmatched_conv_data.append({
                'conversation_id': conv_id,
                'create_time': create_time,
                'create_date': datetime.fromtimestamp(float(create_time)).strftime('%Y-%m-%d %H:%M'),
                'first_user_message': first_user_msg
            })
    
    # Create dataframe and save
    if unmatched_conv_data:
        unmatched_df = pd.DataFrame(unmatched_conv_data)
        unmatched_df = unmatched_df.sort_values('create_time')
        output_path = OUTPUT_PATH.replace('.csv', '_unmatched_conversations.csv')
        unmatched_df.to_csv(output_path, index=False)
        logger.info(f"Saved {len(unmatched_df)} unmatched conversations to {output_path}")


def main():
    """Main function to run the alignment process"""
    logger.info("Starting alignment process")
    
    try:
        # Align datasets
        aligned_data = align_datasets()
        
        # Add a conversation_messages column with all messages concatenated
        logger.info("Adding conversation content")
        aligned_data['conversation_messages'] = None
        
        # Load conversation data again to avoid memory issues
        conv_data = load_conversation_data()
        
        # For each matched survey response, extract and store conversation content
        for idx, row in aligned_data.iterrows():
            if pd.isna(row['conversation_id']):
                continue
                
            conv_id = row['conversation_id']
            conv_messages = conv_data[conv_data['conversation_id'] == conv_id]
            
            if not conv_messages.empty:
                # Sort by create_time
                conv_messages = conv_messages.sort_values('create_time')
                
                # Format messages as a single string
                formatted_msgs = []
                for _, msg in conv_messages.iterrows():
                    role = msg['author_role']
                    content = msg['message_content']
                    
                    # Clean up content format
                    if content.startswith("['") and content.endswith("']"):
                        content = content[2:-2]
                        
                    formatted_msgs.append(f"{role.upper()}: {content}")
                
                # Join all messages with newlines
                all_msgs = "\n\n".join(formatted_msgs)
                aligned_data.at[idx, 'conversation_messages'] = all_msgs
        
        # Clean and finalize the dataset
        cleaned_data = clean_dataset(aligned_data)
        
        # Save to CSV
        cleaned_data.to_csv(OUTPUT_PATH, index=False)
        logger.info(f"Aligned data saved to {OUTPUT_PATH}")
        
        # Print summary
        id_matches = len(cleaned_data[cleaned_data['MatchMethod'] == 'ExplicitID'])
        time_matches = len(cleaned_data[cleaned_data['MatchMethod'] == 'Timestamp'])
        unmatched = len(cleaned_data[cleaned_data['MatchMethod'].isna()])
        total_matched = id_matches + time_matches
        
        logger.info(f"Match summary:")
        logger.info(f"  - Explicit ID matches: {id_matches}")
        logger.info(f"  - Timestamp matches: {time_matches}")
        logger.info(f"  - Unmatched: {unmatched}")
        logger.info(f"  - Match rate: {(total_matched / len(cleaned_data)) * 100:.2f}%")
        
        # Create a CSV with just the matched records for easier analysis
        matched_data = cleaned_data[cleaned_data['HasMatch'] == True].copy()
        matched_data.to_csv(OUTPUT_PATH.replace('.csv', '_matched_only.csv'), index=False)
        logger.info(f"Saved {len(matched_data)} matched records to {OUTPUT_PATH.replace('.csv', '_matched_only.csv')}")
        
        # Create a file with unmatched conversations
        matched_conv_ids = matched_data['conversation_id'].tolist()
        create_unmatched_conversations_file(conv_data, matched_conv_ids)
        
        # Show match confidence statistics if available
        if 'match_confidence' in matched_data.columns:
            avg_confidence = matched_data['match_confidence'].mean()
            high_conf = len(matched_data[matched_data['match_confidence'] >= 80])
            med_conf = len(matched_data[(matched_data['match_confidence'] >= 50) & (matched_data['match_confidence'] < 80)])
            low_conf = len(matched_data[matched_data['match_confidence'] < 50])
            
            logger.info(f"Match confidence statistics:")
            logger.info(f"  - Average confidence: {avg_confidence:.2f}%")
            logger.info(f"  - High confidence (80%+): {high_conf} ({high_conf/total_matched*100:.1f}%)")
            logger.info(f"  - Medium confidence (50-80%): {med_conf} ({med_conf/total_matched*100:.1f}%)")
            logger.info(f"  - Low confidence (<50%): {low_conf} ({low_conf/total_matched*100:.1f}%)")
        
    except Exception as e:
        logger.error(f"Error in alignment process: {str(e)}")
        raise


if __name__ == "__main__":
    main()