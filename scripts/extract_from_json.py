#!/usr/bin/env python3
"""
Extract additional conversations from JSON file (cleaner format).
"""

import pandas as pd
import json
import logging
from pathlib import Path
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# File paths
DATA_DIR = Path(__file__).parent.parent / 'data'
RAW_DIR = DATA_DIR / 'raw'
PROCESSED_DIR = DATA_DIR / 'processed'
OLD_DIR = Path(__file__).parent.parent / 'old'


def extract_messages_from_conversation(conv_data):
    """Extract all messages from a conversation's mapping."""
    messages = []

    mapping = conv_data.get('mapping', {})
    conv_id = conv_data.get('conversation_id') or conv_data.get('id')
    title = conv_data.get('title', '')
    conv_create_time = conv_data.get('create_time', 0)

    if not mapping:
        return messages

    for msg_id, msg_info in mapping.items():
        if not isinstance(msg_info, dict):
            continue

        message = msg_info.get('message')
        if not message or not isinstance(message, dict):
            continue

        author = message.get('author', {})
        if not isinstance(author, dict):
            continue

        author_role = author.get('role', '')
        content = message.get('content', {})

        if isinstance(content, dict):
            parts = content.get('parts', [])
        else:
            parts = []

        # Join content parts
        message_text = ''
        for part in parts:
            if part and isinstance(part, str):
                message_text += part + ' '

        message_text = message_text.strip()

        if message_text and author_role:
            messages.append({
                'conversation_id': conv_id,
                'conversation_title': title,
                'create_time': conv_create_time,
                'update_time': conv_data.get('update_time', conv_create_time),
                'message_id': msg_id,
                'author_role': author_role,
                'author_name': author.get('name', ''),
                'message_content': f"['{message_text}']",
                'message_status': 'finished_successfully',
                'recipient': 'all',
                'channel': ''
            })

    return messages


def main():
    """Main execution."""
    logger.info("=" * 70)
    logger.info("EXTRACTING CONVERSATIONS FROM JSON FILE")
    logger.info("=" * 70)

    # Load JSON file
    json_path = OLD_DIR / 'unified_conversation_data.json'

    all_conversations = []
    with open(json_path, 'r') as f:
        for i, line in enumerate(f):
            try:
                conv = json.loads(line)
                all_conversations.append(conv)
            except Exception as e:
                logger.warning(f"Error parsing line {i}: {e}")

    logger.info(f"Loaded {len(all_conversations)} conversations from JSON")

    # Load current conversation data
    current_conv = pd.read_csv(RAW_DIR / 'unified_conversation_data.csv')
    current_ids = set(current_conv['conversation_id'].unique())
    logger.info(f"Current conversation IDs: {len(current_ids)}")

    # Find additional conversations
    additional_convs = []
    for conv in all_conversations:
        conv_id = conv.get('conversation_id') or conv.get('id')
        if conv_id and conv_id not in current_ids and pd.notna(conv_id):
            additional_convs.append(conv)

    logger.info(f"Additional conversations in JSON: {len(additional_convs)}")

    # Extract messages from additional conversations
    all_messages = []
    successful_convs = []

    for conv in additional_convs:
        conv_id = conv.get('conversation_id') or conv.get('id')

        if not pd.notna(conv_id):
            continue

        messages = extract_messages_from_conversation(conv)

        if messages:
            all_messages.extend(messages)
            successful_convs.append(conv_id)
            logger.info(f"Extracted {len(messages)} messages from {conv_id}")

    logger.info(f"\n=== EXTRACTION SUMMARY ===")
    logger.info(f"Successfully extracted {len(successful_convs)} conversations")
    logger.info(f"Total messages: {len(all_messages)}")

    if all_messages:
        # Save additional messages
        additional_msgs_df = pd.DataFrame(all_messages)
        output_path = PROCESSED_DIR / 'additional_conversation_messages_from_json.csv'
        additional_msgs_df.to_csv(output_path, index=False)
        logger.info(f"Saved to {output_path}")

        # Merge with existing
        combined_conv = pd.concat([current_conv, additional_msgs_df], ignore_index=True)
        combined_output = RAW_DIR / 'unified_conversation_data_complete.csv'
        combined_conv.to_csv(combined_output, index=False)
        logger.info(f"Saved combined data to {combined_output}")
        logger.info(f"Total conversations: {combined_conv['conversation_id'].nunique()}")

        # Show samples
        logger.info(f"\n=== SAMPLE ADDITIONAL CONVERSATIONS ===")
        for conv_id in successful_convs[:5]:
            conv_msgs = additional_msgs_df[additional_msgs_df['conversation_id'] == conv_id]
            user_msgs = conv_msgs[conv_msgs['author_role'] == 'user']

            if not user_msgs.empty:
                first_msg = user_msgs.iloc[0]['message_content']
                logger.info(f"\n{conv_id}:")
                logger.info(f"  First message: {first_msg[:100]}")

    logger.info("\n" + "=" * 70)
    logger.info("EXTRACTION COMPLETE")
    logger.info("=" * 70)


if __name__ == '__main__':
    main()
