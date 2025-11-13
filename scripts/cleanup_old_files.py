#!/usr/bin/env python3
"""
Clean up old files, outdated scripts, and temporary CSVs.
Keep only the essential, updated files.
"""

import shutil
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

PROJECT_DIR = Path(__file__).parent.parent

# Files and folders to remove
TO_REMOVE = [
    # Old data folders
    'old',
    'data/raw',

    # Outdated CSV files in processed
    'data/processed/esperanto_sample_100.csv',
    'data/processed/nhh_esperanto_conversations.csv',
    'data/processed/nhh_esperanto_data_dictionary.csv',
    'data/processed/nhh_esperanto_enhanced_dataset.csv',
    'data/processed/nhh_esperanto_final_analysis.csv',
    'data/processed/nhh_esperanto_finalized_dataset.csv',
    'data/processed/nhh_esperanto_main_study_only.csv',
    'data/processed/nhh_esperanto_matched_participants.csv',
    'data/processed/nhh_esperanto_messages.csv',
    'data/processed/nhh_esperanto_participants.csv',
    'data/processed/nhh_esperanto_pilot_study_only.csv',
    'data/processed/recovered_conversation_messages.csv',
    'data/processed/nhh_esperanto_complete_unified_updated.csv',
    'data/processed/nhh_esperanto_finalized_dataset_with_recovered.csv',

    # Old scripts
    'scripts/aggressive_rematching.py',
    'scripts/apply_corrected_ids.py',
    'scripts/build_clean_dataset_from_scratch.py',
    'scripts/create_clean_analysis_dataset_v2.py',
    'scripts/create_final_clean_dataset.py',
    'scripts/create_unified_complete_dataset.py',
    'scripts/enhance_dataset.py',
    'scripts/extract_additional_conversations.py',
    'scripts/extract_from_json.py',
    'scripts/extract_using_ast.py',
    'scripts/fix_cross_date_mismatches.py',
    'scripts/match_missing_ids.py',
    'scripts/match_recovered_conversations.py',
    'scripts/merge_datasets.py',
    'scripts/regenerate_ids_and_verify.py',
    'scripts/rematch_with_unix_time.py',

    # Duplicate export summaries
    'exports/promptdata_zip_summary_20251113_231904.txt',
    'exports/promptdata_zip_summary_20251113_231928.txt',
]

# Files to KEEP (important!)
KEEP_FILES = [
    'data/processed/nhh_esperanto_complete_unified.csv',
    'data/processed/nhh_esperanto_complete_unified_backup.csv',
    'data/processed/promptdata_matches.csv',
    'data/processed/promptdata_update_summary.csv',
    'data/processed/recovered_matches.csv',
    'exports/nhh_esperanto_promptdata_FINAL.zip',
    'exports/README.md',
    'exports/promptdata_zip_summary_20251113_231943.txt',
    'scripts/process_promptdata_and_export.py',
    'scripts/update_promptdata_with_ids.py',
    'scripts/zip_promptdata.py',
    'scripts/verify_final_dataset.py',
    'scripts/verify_promptdata_updates.py',
    'EXPORT_SUMMARY.md',
    'FINAL_COMPLETION_SUMMARY.md',
]


def main():
    logger.info("=" * 80)
    logger.info("CLEANING UP OLD FILES")
    logger.info("=" * 80)

    removed_count = 0
    failed_count = 0

    for item_path in TO_REMOVE:
        full_path = PROJECT_DIR / item_path

        if not full_path.exists():
            logger.debug(f"Skipping (not found): {item_path}")
            continue

        try:
            if full_path.is_dir():
                shutil.rmtree(full_path)
                logger.info(f"✓ Removed folder: {item_path}")
            else:
                full_path.unlink()
                logger.info(f"✓ Removed file: {item_path}")
            removed_count += 1
        except Exception as e:
            logger.error(f"✗ Failed to remove {item_path}: {e}")
            failed_count += 1

    logger.info(f"\n{'='*80}")
    logger.info(f"CLEANUP COMPLETE")
    logger.info(f"{'='*80}")
    logger.info(f"Files/folders removed: {removed_count}")
    logger.info(f"Failed: {failed_count}")

    logger.info(f"\n{'='*80}")
    logger.info("ESSENTIAL FILES KEPT")
    logger.info(f"{'='*80}")
    for keep_file in KEEP_FILES:
        full_path = PROJECT_DIR / keep_file
        if full_path.exists():
            size = full_path.stat().st_size
            if size > 1024 * 1024:
                size_str = f"{size / (1024*1024):.1f} MB"
            elif size > 1024:
                size_str = f"{size / 1024:.1f} KB"
            else:
                size_str = f"{size} B"
            logger.info(f"✓ {keep_file} ({size_str})")
        else:
            logger.warning(f"⚠ {keep_file} (NOT FOUND)")


if __name__ == '__main__':
    main()
