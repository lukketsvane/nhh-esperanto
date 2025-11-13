#!/usr/bin/env python3
"""
Zip the updated promptdata folder for download.
Includes all CSN folders with updated conversation files containing participant information.
"""

import zipfile
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
PROJECT_DIR = Path(__file__).parent.parent
PROMPTDATA_DIR = PROJECT_DIR / 'promptdata'
OUTPUT_DIR = PROJECT_DIR / 'exports'


def get_folder_size(folder_path: Path) -> int:
    """Calculate total size of folder in bytes."""
    total_size = 0
    for file in folder_path.rglob('*'):
        if file.is_file():
            total_size += file.stat().st_size
    return total_size


def format_size(size_bytes: int) -> str:
    """Format bytes to human readable string."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def zip_promptdata():
    """Zip the promptdata folder."""
    logger.info("=" * 80)
    logger.info("ZIPPING PROMPTDATA FOLDER")
    logger.info("=" * 80)

    # Create exports directory if it doesn't exist
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Generate output filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    zip_filename = f'nhh_esperanto_promptdata_updated_{timestamp}.zip'
    zip_path = OUTPUT_DIR / zip_filename

    logger.info(f"\nSource folder: {PROMPTDATA_DIR}")
    logger.info(f"Output file: {zip_path}")

    # Calculate source folder size
    source_size = get_folder_size(PROMPTDATA_DIR)
    logger.info(f"Source folder size: {format_size(source_size)}")

    # Create zip file
    logger.info(f"\nCreating zip archive...")
    file_count = 0
    folder_count = 0

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        # Walk through promptdata directory
        for item in PROMPTDATA_DIR.rglob('*'):
            if item.is_file():
                # Skip backup files unless specified
                if item.suffix == '.backup':
                    continue

                # Add file to zip
                arcname = item.relative_to(PROJECT_DIR)
                zipf.write(item, arcname)
                file_count += 1

                if file_count % 100 == 0:
                    logger.info(f"  Processed {file_count} files...")

            elif item.is_dir():
                folder_count += 1

    # Get zip file size
    zip_size = zip_path.stat().st_size
    compression_ratio = (1 - zip_size / source_size) * 100 if source_size > 0 else 0

    logger.info(f"\n{'='*80}")
    logger.info("ZIP COMPLETE")
    logger.info(f"{'='*80}")
    logger.info(f"Files archived: {file_count}")
    logger.info(f"Folders archived: {folder_count}")
    logger.info(f"Original size: {format_size(source_size)}")
    logger.info(f"Compressed size: {format_size(zip_size)}")
    logger.info(f"Compression ratio: {compression_ratio:.1f}%")
    logger.info(f"\nOutput file: {zip_path}")
    logger.info(f"{'='*80}")

    # Create a summary file
    summary_path = OUTPUT_DIR / f'promptdata_zip_summary_{timestamp}.txt'
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("NHH Esperanto Promptdata Archive Summary\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Archive Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Archive Name: {zip_filename}\n")
        f.write(f"Archive Size: {format_size(zip_size)}\n")
        f.write(f"Original Size: {format_size(source_size)}\n")
        f.write(f"Compression: {compression_ratio:.1f}%\n\n")
        f.write(f"Total Files: {file_count}\n")
        f.write(f"Total Folders: {folder_count}\n\n")
        f.write("Contents:\n")
        f.write("-" * 60 + "\n")
        f.write("- 22 CSN folders (CSN1-CSN22)\n")
        f.write("- Updated conversation JSON files with participant information\n")
        f.write("- User data, chat HTML, and conversation metadata\n")
        f.write("- 268 conversations matched to survey participants\n")
        f.write("- 397 total conversations available\n\n")
        f.write("Data Structure:\n")
        f.write("-" * 60 + "\n")
        f.write("promptdata/\n")
        f.write("  - CSN1/\n")
        f.write("    - csn1/conversations.json (updated with participant IDs)\n")
        f.write("    - user.json\n")
        f.write("    - chat.html\n")
        f.write("    - ...\n")
        f.write("  - CSN2/\n")
        f.write("    - ...\n")
        f.write("  - ...\n\n")
        f.write("Updated Conversation Fields:\n")
        f.write("-" * 60 + "\n")
        f.write("Each matched conversation now includes:\n")
        f.write("  - participant_id: Survey ResponseId\n")
        f.write("  - participant_user_id: User ID\n")
        f.write("  - participant_email: Email address\n")
        f.write("  - participant_name: Full name\n")
        f.write("  - match_method: How participant was matched\n")
        f.write("  - survey_start_time: Survey start timestamp\n")
        f.write("  - metadata: Additional matching information\n")

    logger.info(f"\nSummary saved to: {summary_path}")

    return zip_path


if __name__ == '__main__':
    zip_path = zip_promptdata()
    print(f"\n[SUCCESS] Promptdata folder successfully zipped!")
    print(f"[DOWNLOAD] Location: {zip_path}")
