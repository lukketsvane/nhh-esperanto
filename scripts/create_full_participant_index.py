#!/usr/bin/env python3
"""
Create a comprehensive participant index for promptdata folder.
This ensures all 604 participants are represented, even those without conversations.
"""

import json
import logging
from pathlib import Path
import pandas as pd

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

PROJECT_DIR = Path(__file__).parent.parent
PROMPTDATA_DIR = PROJECT_DIR / 'promptdata'
PROCESSED_DIR = PROJECT_DIR / 'data' / 'processed'


def main():
    logger.info("=" * 80)
    logger.info("CREATING COMPREHENSIVE PARTICIPANT INDEX")
    logger.info("=" * 80)

    # Load main dataset
    unified_df = pd.read_csv(PROCESSED_DIR / 'nhh_esperanto_complete_unified.csv')
    logger.info(f"\nLoaded {len(unified_df)} participants from main dataset")

    # Create comprehensive participant index
    participant_index = []

    for idx, row in unified_df.iterrows():
        participant_info = {
            'participant_number': idx + 1,
            'ResponseId': row['ResponseId'],
            'has_conversation': pd.notna(row.get('conversation_id')),
            'conversation_id': row.get('conversation_id') if pd.notna(row.get('conversation_id')) else None,
            'UserID': row.get('UserID') if pd.notna(row.get('UserID')) else None,
            'MatchMethod': row.get('MatchMethod') if pd.notna(row.get('MatchMethod')) else None,
            'data_status': row.get('data_status') if pd.notna(row.get('data_status')) else 'No conversation data',
            'treatment': row.get('treatment') if pd.notna(row.get('treatment')) else None,
            'testscore': row.get('testscore') if pd.notna(row.get('testscore')) else None,
            'MessageCount': row.get('MessageCount') if pd.notna(row.get('MessageCount')) else 0,
            'ConversationDurationMinutes': row.get('ConversationDurationMinutes') if pd.notna(row.get('ConversationDurationMinutes')) else 0,
            'Session': row.get('Session') if pd.notna(row.get('Session')) else None,
            'start_time_unix': row.get('start_time_unix') if pd.notna(row.get('start_time_unix')) else None,
        }

        participant_index.append(participant_info)

    # Save to promptdata folder
    index_path = PROMPTDATA_DIR / 'PARTICIPANT_INDEX.json'
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump({
            'metadata': {
                'total_participants': len(unified_df),
                'participants_with_conversations': sum(1 for p in participant_index if p['has_conversation']),
                'participants_without_conversations': sum(1 for p in participant_index if not p['has_conversation']),
                'created': pd.Timestamp.now().isoformat(),
                'dataset_version': 'nhh_esperanto_complete_unified.csv',
                'description': 'Complete index of all 604 study participants with conversation status'
            },
            'participants': participant_index
        }, f, indent=2, ensure_ascii=False)

    logger.info(f"✓ Saved comprehensive index to: {index_path}")

    # Create CSV version
    index_df = pd.DataFrame(participant_index)
    csv_path = PROMPTDATA_DIR / 'PARTICIPANT_INDEX.csv'
    index_df.to_csv(csv_path, index=False)
    logger.info(f"✓ Saved CSV version to: {csv_path}")

    # Create README for promptdata
    readme_path = PROMPTDATA_DIR / 'README.md'
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write("# NHH Esperanto Promptdata - All Participants\n\n")
        f.write("## Overview\n\n")
        f.write(f"This folder contains conversation data for the NHH Esperanto study.\n\n")
        f.write(f"**Total Study Participants**: 604\n")
        f.write(f"**With Conversation Data**: {sum(1 for p in participant_index if p['has_conversation'])} ({sum(1 for p in participant_index if p['has_conversation'])/len(participant_index)*100:.1f}%)\n")
        f.write(f"**Without Conversation Data**: {sum(1 for p in participant_index if not p['has_conversation'])} ({sum(1 for p in participant_index if not p['has_conversation'])/len(participant_index)*100:.1f}%)\n\n")

        f.write("## Participant Index\n\n")
        f.write("All 604 participants are documented in:\n")
        f.write("- `PARTICIPANT_INDEX.json` - Full participant data with conversation status\n")
        f.write("- `PARTICIPANT_INDEX.csv` - CSV version for easy viewing\n\n")

        f.write("## Folder Structure\n\n")
        f.write("```\n")
        f.write("promptdata/\n")
        f.write("├── PARTICIPANT_INDEX.json      ← ALL 604 participants listed here\n")
        f.write("├── PARTICIPANT_INDEX.csv        ← CSV version\n")
        f.write("├── README.md                    ← This file\n")
        f.write("├── CSN1/                        ← Conversation data folders\n")
        f.write("├── CSN2/\n")
        f.write("├── ...\n")
        f.write("└── CSN22/\n")
        f.write("```\n\n")

        f.write("## Data Coverage\n\n")

        # Group by data status
        status_counts = {}
        for p in participant_index:
            status = p['data_status']
            status_counts[status] = status_counts.get(status, 0) + 1

        f.write("### Participants by Data Status\n\n")
        f.write("| Status | Count | Percentage |\n")
        f.write("|--------|-------|------------|\n")
        for status, count in sorted(status_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = count / len(participant_index) * 100
            f.write(f"| {status} | {count} | {percentage:.1f}% |\n")

        f.write("\n## Using the Participant Index\n\n")
        f.write("### Python Example\n\n")
        f.write("```python\n")
        f.write("import json\n")
        f.write("import pandas as pd\n\n")
        f.write("# Load all participants\n")
        f.write("with open('promptdata/PARTICIPANT_INDEX.json', 'r') as f:\n")
        f.write("    data = json.load(f)\n\n")
        f.write("participants = data['participants']\n")
        f.write("print(f\"Total participants: {data['metadata']['total_participants']}\")\n\n")
        f.write("# Get participants with conversations\n")
        f.write("with_convs = [p for p in participants if p['has_conversation']]\n")
        f.write("print(f\"With conversations: {len(with_convs)}\")\n\n")
        f.write("# Get participants without conversations\n")
        f.write("without_convs = [p for p in participants if not p['has_conversation']]\n")
        f.write("print(f\"Without conversations: {len(without_convs)}\")\n")
        f.write("```\n\n")

        f.write("### CSV Example\n\n")
        f.write("```python\n")
        f.write("import pandas as pd\n\n")
        f.write("# Load participant index\n")
        f.write("df = pd.read_csv('promptdata/PARTICIPANT_INDEX.csv')\n\n")
        f.write("print(f\"Total participants: {len(df)}\")\n")
        f.write("print(f\"With conversations: {df['has_conversation'].sum()}\")\n")
        f.write("print(f\"Without conversations: {(~df['has_conversation']).sum()}\")\n")
        f.write("```\n\n")

        f.write("## Conversation Data by Folder\n\n")
        f.write("| Folder | Conversations | Matched | Match Rate |\n")
        f.write("|--------|---------------|---------|------------|\n")
        f.write("| CSN1   | 21 | 20 | 95.2% |\n")
        f.write("| CSN10  | 17 | 17 | 100.0% |\n")
        f.write("| CSN11  | 16 | 16 | 100.0% |\n")
        f.write("| CSN13-18 | - | - | 100.0% |\n")
        f.write("| Others | - | - | Variable |\n\n")

        f.write("See `PARTICIPANT_INDEX.json` for complete mapping of all 604 participants.\n\n")

        f.write("## Integration with Main Dataset\n\n")
        f.write("The participant index links to the main dataset via `ResponseId`:\n\n")
        f.write("```python\n")
        f.write("# Load main dataset\n")
        f.write("main_df = pd.read_csv('../data/processed/nhh_esperanto_complete_unified.csv')\n\n")
        f.write("# Load participant index\n")
        f.write("index_df = pd.read_csv('PARTICIPANT_INDEX.csv')\n\n")
        f.write("# Join on ResponseId\n")
        f.write("merged = main_df.merge(index_df, on='ResponseId', how='left')\n")
        f.write("```\n\n")

        f.write("---\n\n")
        f.write("**Last Updated**: 2025-11-13\n")
        f.write("**Dataset Version**: nhh_esperanto_complete_unified.csv\n")
        f.write("**Total Participants**: 604\n")

    logger.info(f"✓ Created README at: {readme_path}")

    # Create summary statistics file
    stats_path = PROMPTDATA_DIR / 'STATISTICS.txt'
    with open(stats_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("NHH ESPERANTO STUDY - COMPLETE PARTICIPANT STATISTICS\n")
        f.write("=" * 80 + "\n\n")

        f.write(f"TOTAL PARTICIPANTS: {len(participant_index)}\n\n")

        f.write("CONVERSATION DATA:\n")
        f.write(f"  With conversations: {sum(1 for p in participant_index if p['has_conversation'])}\n")
        f.write(f"  Without conversations: {sum(1 for p in participant_index if not p['has_conversation'])}\n")
        f.write(f"  Coverage rate: {sum(1 for p in participant_index if p['has_conversation'])/len(participant_index)*100:.1f}%\n\n")

        f.write("DATA STATUS BREAKDOWN:\n")
        for status, count in sorted(status_counts.items(), key=lambda x: x[1], reverse=True):
            f.write(f"  {status}: {count} ({count/len(participant_index)*100:.1f}%)\n")

        f.write("\n" + "=" * 80 + "\n")
        f.write(f"Generated: {pd.Timestamp.now()}\n")
        f.write("=" * 80 + "\n")

    logger.info(f"✓ Created statistics file at: {stats_path}")

    logger.info("\n" + "=" * 80)
    logger.info("INDEX CREATION COMPLETE")
    logger.info("=" * 80)
    logger.info(f"Total participants indexed: {len(participant_index)}")
    logger.info(f"With conversation data: {sum(1 for p in participant_index if p['has_conversation'])}")
    logger.info(f"Without conversation data: {sum(1 for p in participant_index if not p['has_conversation'])}")
    logger.info("\nFiles created:")
    logger.info(f"  - {index_path}")
    logger.info(f"  - {csv_path}")
    logger.info(f"  - {readme_path}")
    logger.info(f"  - {stats_path}")
    logger.info("=" * 80)


if __name__ == '__main__':
    main()
