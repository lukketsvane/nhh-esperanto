#!/usr/bin/env python3
"""
Extract and process 21 additional conversations found in CSN file.
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


def extract_messages_from_mapping(mapping_json):
    """Extract messages from the mapping field in CSN data."""
    messages = []

    try:
        if isinstance(mapping_json, str):
            # Replace single quotes with double quotes for JSON parsing
            mapping_str = mapping_json.replace("'", '"').replace('None', 'null').replace('True', 'true').replace('False', 'false')
            mapping = json.loads(mapping_str)
        elif isinstance(mapping_json, dict):
            mapping = mapping_json
        else:
            return messages

        for msg_id, msg_data in mapping.items():
            if not isinstance(msg_data, dict):
                continue

            message = msg_data.get('message')
            if not message or not isinstance(message, dict):
                continue

            # Extract message details
            author_role = message.get('author', {}).get('role', '')
            content_parts = message.get('content', {}).get('parts', [])
            create_time = message.get('create_time', 0)

            # Join content parts
            message_content = ' '.join([str(p) for p in content_parts if p])

            if message_content and author_role:
                messages.append({
                    'message_id': msg_id,
                    'author_role': author_role,
                    'message_content': message_content,
                    'create_time': create_time
                })

    except Exception as e:
        logger.warning(f"Error extracting messages from mapping: {e}")

    return messages


def main():
    """Main execution."""
    logger.info("=" * 70)
    logger.info("EXTRACTING ADDITIONAL CONVERSATIONS FROM CSN FILE")
    logger.info("=" * 70)

    # Load current conversation data
    current_conv = pd.read_csv(RAW_DIR / 'unified_conversation_data.csv')
    current_ids = set(current_conv['conversation_id'].unique())
    logger.info(f"Current conversations: {len(current_ids)}")

    # Load CSN data
    csn_df = pd.read_csv(OLD_DIR / 'Unified_CSN_Data_-_16-12-2024.csv')
    logger.info(f"CSN file conversations: {csn_df['conversation_id'].nunique()}")

    # Find additional conversations
    csn_ids = set(csn_df['conversation_id'].dropna().unique())
    additional_ids = csn_ids - current_ids
    logger.info(f"Additional conversations found: {len(additional_ids)}")

    # Extract additional conversations
    additional_convs = csn_df[csn_df['conversation_id'].isin(additional_ids)].copy()

    logger.info(f"\n=== PROCESSING {len(additional_convs)} ADDITIONAL CONVERSATIONS ===")

    # Extract messages from each conversation
    all_messages = []

    for idx, row in additional_convs.iterrows():
        conv_id = row['conversation_id']
        create_time = row.get('create_time', 0)
        title = row.get('title', '')
        mapping = row.get('mapping', '{}')

        logger.info(f"Processing {conv_id}")

        # Extract messages from mapping
        messages = extract_messages_from_mapping(mapping)

        for msg in messages:
            all_messages.append({
                'conversation_id': conv_id,
                'conversation_title': title,
                'create_time': create_time,
                'update_time': row.get('update_time', create_time),
                'message_id': msg['message_id'],
                'author_role': msg['author_role'],
                'author_name': '',
                'message_content': f"['{msg['message_content']}']",
                'message_status': 'finished_successfully',
                'recipient': 'all',
                'channel': ''
            })

    logger.info(f"\nExtracted {len(all_messages)} messages from additional conversations")

    # Create DataFrame
    additional_msgs_df = pd.DataFrame(all_messages)

    # Save additional messages
    output_path = PROCESSED_DIR / 'additional_conversation_messages.csv'
    additional_msgs_df.to_csv(output_path, index=False)
    logger.info(f"Saved additional messages to {output_path}")

    # Merge with existing conversation data
    logger.info("\n=== MERGING WITH EXISTING DATA ===")
    combined_conv = pd.concat([current_conv, additional_msgs_df], ignore_index=True)

    # Save combined data
    combined_output = RAW_DIR / 'unified_conversation_data_with_additional.csv'
    combined_conv.to_csv(combined_output, index=False)
    logger.info(f"Saved combined conversation data to {combined_output}")

    logger.info(f"\nTotal conversations in combined data: {combined_conv['conversation_id'].nunique()}")

    # Show sample of additional conversations
    if not additional_msgs_df.empty:
        logger.info(f"\n=== SAMPLE ADDITIONAL CONVERSATIONS ===")
        for conv_id in list(additional_ids)[:5]:
            conv_msgs = additional_msgs_df[additional_msgs_df['conversation_id'] == conv_id]
            user_msgs = conv_msgs[conv_msgs['author_role'] == 'user']

            if not user_msgs.empty:
                first_msg = user_msgs.iloc[0]['message_content']
                create_time = conv_msgs.iloc[0]['create_time']
                if pd.notna(create_time):
                    dt = datetime.fromtimestamp(float(create_time))
                    logger.info(f"\n{conv_id[:20]}...")
                    logger.info(f"  Time: {dt}")
                    logger.info(f"  First msg: {first_msg[:100]}")
    else:
        logger.warning("No messages extracted from additional conversations")

    logger.info("\n" + "=" * 70)
    logger.info("EXTRACTION COMPLETE")
    logger.info("=" * 70)


if __name__ == '__main__':
    main()
