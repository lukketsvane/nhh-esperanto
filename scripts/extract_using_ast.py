#!/usr/bin/env python3
"""
Extract additional conversations from CSN file using ast.literal_eval for mapping.
"""

import pandas as pd
import ast
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


def extract_messages_from_mapping(mapping_str):
    """Extract messages from the mapping field using ast.literal_eval."""
    messages = []

    try:
        # Use ast.literal_eval to safely evaluate Python literal structures
        mapping = ast.literal_eval(mapping_str)

        if not isinstance(mapping, dict):
            return messages

        for msg_id, msg_data in mapping.items():
            if not isinstance(msg_data, dict):
                continue

            message = msg_data.get('message')
            if not message or not isinstance(message, dict):
                continue

            # Extract message details
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
                    'message_id': msg_id,
                    'author_role': author_role,
                    'message_content': message_text,
                    'create_time': message.get('create_time', 0)
                })

    except Exception as e:
        logger.debug(f"Error parsing mapping: {str(e)[:100]}")

    return messages


def main():
    """Main execution."""
    logger.info("=" * 70)
    logger.info("EXTRACTING CONVERSATIONS USING AST")
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

    # Extract messages
    all_messages = []
    successful_count = 0

    for idx, row in additional_convs.iterrows():
        conv_id = row['conversation_id']
        title = row.get('title', '')
        create_time = row.get('create_time', 0)
        mapping_str = row.get('mapping', '')

        if not mapping_str or pd.isna(mapping_str) or not isinstance(mapping_str, str):
            continue

        messages = extract_messages_from_mapping(mapping_str)

        if messages:
            successful_count += 1
            logger.info(f"✓ {conv_id}: {len(messages)} messages ('{title}')")

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
        else:
            logger.info(f"✗ {conv_id}: No messages extracted")

    logger.info(f"\n=== EXTRACTION SUMMARY ===")
    logger.info(f"Successfully extracted: {successful_count}/{len(additional_convs)} conversations")
    logger.info(f"Total messages: {len(all_messages)}")

    if all_messages:
        # Save additional messages
        additional_msgs_df = pd.DataFrame(all_messages)
        output_path = PROCESSED_DIR / 'recovered_conversation_messages.csv'
        additional_msgs_df.to_csv(output_path, index=False)
        logger.info(f"Saved to {output_path}")

        # Merge with existing
        combined_conv = pd.concat([current_conv, additional_msgs_df], ignore_index=True)
        combined_output = RAW_DIR / 'unified_conversation_data_complete.csv'
        combined_conv.to_csv(combined_output, index=False)
        logger.info(f"Saved combined data to {combined_output}")
        logger.info(f"Total conversations: {combined_conv['conversation_id'].nunique()}")

        # Show sample first messages
        logger.info(f"\n=== SAMPLE RECOVERED CONVERSATIONS ===")
        for conv_id in additional_msgs_df['conversation_id'].unique()[:5]:
            conv_msgs = additional_msgs_df[additional_msgs_df['conversation_id'] == conv_id]
            user_msgs = conv_msgs[conv_msgs['author_role'] == 'user']

            if not user_msgs.empty:
                first_msg = user_msgs.iloc[0]['message_content']
                logger.info(f"\n{conv_id[:30]}...")
                logger.info(f"  Messages: {len(conv_msgs)}")
                logger.info(f"  First: {first_msg[:100]}")
    else:
        logger.warning("No messages extracted!")

    logger.info("\n" + "=" * 70)
    logger.info("EXTRACTION COMPLETE")
    logger.info("=" * 70)


if __name__ == '__main__':
    main()
