#!/usr/bin/env python3
"""
Update promptdata conversation files with matched participant IDs.
This ensures all participants (including those who forgot to mention their ID)
are properly identified in the conversation data.
"""

import json
import logging
from pathlib import Path
from datetime import datetime
import pandas as pd

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# File paths
PROJECT_DIR = Path(__file__).parent.parent
PROMPTDATA_DIR = PROJECT_DIR / 'promptdata'
DATA_DIR = PROJECT_DIR / 'data'
PROCESSED_DIR = DATA_DIR / 'processed'


def update_conversation_file(conv_file_path: Path, participant_info: dict) -> bool:
    """Update a conversation JSON file with participant information."""
    try:
        # Read the conversation file
        with open(conv_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Handle both list and dict formats
        conversations = data if isinstance(data, list) else [data]
        updated = False

        for conv in conversations:
            if not isinstance(conv, dict):
                continue

            # Check if this is the conversation we're looking for
            if conv.get('id') == participant_info['conversation_id']:
                # Update conversation with participant info
                conv['participant_id'] = participant_info['ResponseId']
                conv['participant_user_id'] = participant_info['UserID']
                conv['participant_email'] = participant_info.get('RecipientEmail', '')
                conv['participant_name'] = f"{participant_info.get('RecipientFirstName', '')} {participant_info.get('RecipientLastName', '')}".strip()
                conv['match_method'] = participant_info['MatchMethod']
                conv['survey_start_time'] = participant_info['start_time_unix']
                conv['time_difference_hours'] = participant_info.get('time_diff_hours', 0)

                # Add metadata
                if 'metadata' not in conv:
                    conv['metadata'] = {}

                conv['metadata']['matched_participant'] = True
                conv['metadata']['match_timestamp'] = datetime.now().isoformat()
                conv['metadata']['unified_participant_id'] = participant_info.get('unified_participant_id', '')

                updated = True
                logger.info(f"  Updated conversation with participant: {participant_info['ResponseId']}")

        if updated:
            # Save updated data back to file
            output_data = conversations[0] if not isinstance(data, list) and len(conversations) == 1 else conversations

            # Create backup first
            backup_path = conv_file_path.with_suffix('.json.backup')
            if not backup_path.exists():
                with open(backup_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

            # Write updated data
            with open(conv_file_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)

            return True

    except Exception as e:
        logger.error(f"Error updating {conv_file_path}: {e}")
        return False

    return False


def find_conversation_file(conversation_id: str) -> Path:
    """Find the conversation file containing the given conversation ID."""
    # Search all CSN folders for the conversation
    for csn_folder in sorted(PROMPTDATA_DIR.glob('CSN*')):
        if not csn_folder.is_dir():
            continue

        # Check both root and subdirectory
        conv_files = list(csn_folder.rglob('conversations.json'))

        for conv_file in conv_files:
            try:
                with open(conv_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                conversations = data if isinstance(data, list) else [data]

                for conv in conversations:
                    if isinstance(conv, dict) and conv.get('id') == conversation_id:
                        return conv_file

            except Exception as e:
                logger.warning(f"Error reading {conv_file}: {e}")
                continue

    return None


def main():
    """Main execution."""
    logger.info("=" * 80)
    logger.info("UPDATING PROMPTDATA FILES WITH MATCHED PARTICIPANT IDs")
    logger.info("=" * 80)

    # Load the unified dataset
    unified_df = pd.read_csv(PROCESSED_DIR / 'nhh_esperanto_complete_unified.csv')
    logger.info(f"\nLoaded unified dataset: {len(unified_df)} participants")

    # Get all participants with conversation data
    matched_df = unified_df[unified_df['conversation_id'].notna()].copy()
    logger.info(f"Participants with conversations: {len(matched_df)}")

    # Calculate time difference if needed
    if 'time_diff_hours' not in matched_df.columns and 'create_time' in matched_df.columns:
        matched_df['time_diff_hours'] = abs(
            pd.to_numeric(matched_df['create_time'], errors='coerce') -
            pd.to_numeric(matched_df['start_time_unix'], errors='coerce')
        ) / 3600

    # Process each matched participant
    logger.info(f"\n{'='*80}")
    logger.info("UPDATING CONVERSATION FILES")
    logger.info(f"{'='*80}")

    updated_count = 0
    not_found_count = 0
    error_count = 0

    for idx, row in matched_df.iterrows():
        conversation_id = row['conversation_id']

        # Skip if invalid conversation_id
        if pd.isna(conversation_id) or str(conversation_id).strip() == '':
            continue

        logger.info(f"\nProcessing {conversation_id[:30]}...")

        # Find the conversation file
        conv_file = find_conversation_file(conversation_id)

        if conv_file is None:
            logger.warning(f"  Conversation file not found for {conversation_id}")
            not_found_count += 1
            continue

        logger.info(f"  Found in: {conv_file.parent.name}/{conv_file.name}")

        # Prepare participant info
        participant_info = {
            'conversation_id': conversation_id,
            'ResponseId': row['ResponseId'],
            'UserID': row.get('UserID', ''),
            'RecipientEmail': row.get('RecipientEmail', ''),
            'RecipientFirstName': row.get('RecipientFirstName', ''),
            'RecipientLastName': row.get('RecipientLastName', ''),
            'MatchMethod': row.get('MatchMethod', ''),
            'start_time_unix': row.get('start_time_unix', 0),
            'time_diff_hours': row.get('time_diff_hours', 0),
            'unified_participant_id': row.get('unified_participant_id', '')
        }

        # Update the conversation file
        if update_conversation_file(conv_file, participant_info):
            updated_count += 1
        else:
            error_count += 1

    # Summary
    logger.info(f"\n{'='*80}")
    logger.info("UPDATE SUMMARY")
    logger.info(f"{'='*80}")
    logger.info(f"Total matched participants: {len(matched_df)}")
    logger.info(f"Successfully updated: {updated_count}")
    logger.info(f"Conversation files not found: {not_found_count}")
    logger.info(f"Errors during update: {error_count}")
    logger.info(f"Update rate: {updated_count / len(matched_df) * 100:.1f}%")

    # Create summary CSV
    summary_data = []
    for csn_folder in sorted(PROMPTDATA_DIR.glob('CSN*')):
        if not csn_folder.is_dir():
            continue

        conv_files = list(csn_folder.rglob('conversations.json'))
        total_convs = 0
        matched_convs = 0

        for conv_file in conv_files:
            try:
                with open(conv_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                conversations = data if isinstance(data, list) else [data]
                total_convs += len(conversations)

                for conv in conversations:
                    if isinstance(conv, dict) and conv.get('participant_id'):
                        matched_convs += 1

            except Exception:
                continue

        summary_data.append({
            'folder': csn_folder.name,
            'total_conversations': total_convs,
            'matched_conversations': matched_convs,
            'unmatched_conversations': total_convs - matched_convs,
            'match_rate': f"{matched_convs / total_convs * 100:.1f}%" if total_convs > 0 else "0%"
        })

    summary_df = pd.DataFrame(summary_data)
    summary_output = PROCESSED_DIR / 'promptdata_update_summary.csv'
    summary_df.to_csv(summary_output, index=False)
    logger.info(f"\nSaved summary to: {summary_output}")

    # Display summary by folder
    logger.info(f"\n{'='*80}")
    logger.info("CONVERSATIONS BY FOLDER")
    logger.info(f"{'='*80}")
    for _, row in summary_df.iterrows():
        logger.info(f"{row['folder']:6s}: {row['matched_conversations']:3d}/{row['total_conversations']:3d} matched ({row['match_rate']})")

    total_convs = summary_df['total_conversations'].sum()
    total_matched = summary_df['matched_conversations'].sum()
    logger.info(f"\n{'TOTAL':6s}: {total_matched:3d}/{total_convs:3d} matched ({total_matched / total_convs * 100:.1f}%)")

    logger.info(f"\n{'='*80}")
    logger.info("PROMPTDATA UPDATE COMPLETE")
    logger.info(f"{'='*80}")


if __name__ == '__main__':
    main()
