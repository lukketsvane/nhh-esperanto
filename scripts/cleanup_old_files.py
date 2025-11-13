#!/usr/bin/env python3
"""
Clean up old and unnecessary files.
Keep only essential files for the final dataset.
"""

import os
import shutil
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def cleanup_old_files():
    """Delete old and unnecessary files."""

    logger.info("=" * 80)
    logger.info("CLEANING UP OLD FILES")
    logger.info("=" * 80)

    # Files to keep in old/ directory (critical source data)
    old_files_to_keep = [
        'old/Unified_CSN_Data_-_16-12-2024.csv'  # Source of recovered data
    ]

    # Delete entire old/ directory contents except for critical files
    logger.info("\nCleaning old/ directory...")
    if os.path.exists('old'):
        for item in os.listdir('old'):
            item_path = os.path.join('old', item)
            full_path = f'old/{item}'

            if full_path not in old_files_to_keep:
                try:
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                        logger.info(f"  Deleted: {item}")
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                        logger.info(f"  Deleted directory: {item}")
                except Exception as e:
                    logger.error(f"  Error deleting {item}: {e}")
            else:
                logger.info(f"  Kept: {item} (critical source data)")

    # Delete backup files (we have the final dataset now)
    logger.info("\nCleaning data/processed/backups/...")
    backup_dir = 'data/processed/backups'
    if os.path.exists(backup_dir):
        try:
            shutil.rmtree(backup_dir)
            logger.info("  Deleted entire backups/ directory")
        except Exception as e:
            logger.error(f"  Error deleting backups: {e}")

    # Delete intermediate files (we have the final dataset now)
    logger.info("\nCleaning data/processed/intermediate/...")
    intermediate_dir = 'data/processed/intermediate'
    if os.path.exists(intermediate_dir):
        try:
            shutil.rmtree(intermediate_dir)
            logger.info("  Deleted entire intermediate/ directory")
        except Exception as e:
            logger.error(f"  Error deleting intermediate: {e}")

    # Delete old finalized dataset (replaced by consolidated version)
    logger.info("\nDeleting old dataset versions...")
    old_datasets = [
        'data/processed/nhh_esperanto_finalized_dataset.csv',
        'data/processed/nhh_esperanto_enhanced_dataset.csv',
        'data/processed/esperanto_sample_100.csv',
    ]

    for dataset in old_datasets:
        if os.path.exists(dataset):
            try:
                os.remove(dataset)
                logger.info(f"  Deleted: {dataset}")
            except Exception as e:
                logger.error(f"  Error deleting {dataset}: {e}")

    # Keep essential files
    essential_files = [
        'data/processed/nhh_esperanto_final_consolidated_dataset.csv',  # Main dataset
        'data/processed/nhh_esperanto_participants.csv',  # Participant table
        'data/processed/nhh_esperanto_conversations.csv',  # Conversation table
        'data/processed/nhh_esperanto_messages.csv',  # Message table
        'data/processed/nhh_esperanto_data_dictionary.csv',  # Data dictionary
        'data/processed/recovered_conversation_messages.csv',  # Recovery documentation
        'data/processed/recovered_matches.csv',  # Recovery documentation
        'data/processed/DATASET_SUMMARY.txt',  # Summary
    ]

    logger.info("\n" + "=" * 80)
    logger.info("ESSENTIAL FILES RETAINED")
    logger.info("=" * 80)

    for filepath in essential_files:
        if os.path.exists(filepath):
            size = os.path.getsize(filepath) / (1024 * 1024)  # MB
            logger.info(f"  ✓ {filepath} ({size:.2f} MB)")
        else:
            logger.warning(f"  ✗ {filepath} (not found)")

    logger.info("\n" + "=" * 80)
    logger.info("CLEANUP COMPLETE!")
    logger.info("=" * 80)

if __name__ == '__main__':
    cleanup_old_files()
