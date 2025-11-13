# NHH Esperanto Promptdata - All Participants

## Overview

This folder contains conversation data for the NHH Esperanto study.

**Total Study Participants**: 604
**With Conversation Data**: 329 (54.5%)
**Without Conversation Data**: 275 (45.5%)

## Participant Index

All 604 participants are documented in:
- `PARTICIPANT_INDEX.json` - Full participant data with conversation status
- `PARTICIPANT_INDEX.csv` - CSV version for easy viewing

## Folder Structure

```
promptdata/
├── PARTICIPANT_INDEX.json      ← ALL 604 participants listed here
├── PARTICIPANT_INDEX.csv        ← CSV version
├── README.md                    ← This file
├── CSN1/                        ← Conversation data folders
├── CSN2/
├── ...
└── CSN22/
```

## Data Coverage

### Participants by Data Status

| Status | Count | Percentage |
|--------|-------|------------|
| No conversation data | 257 | 42.5% |
| Recovered from promptdata | 197 | 32.6% |
| Duplicate | 83 | 13.7% |
| Complete | 29 | 4.8% |
| Recovered | 20 | 3.3% |
| Missing conversation | 18 | 3.0% |

## Using the Participant Index

### Python Example

```python
import json
import pandas as pd

# Load all participants
with open('promptdata/PARTICIPANT_INDEX.json', 'r') as f:
    data = json.load(f)

participants = data['participants']
print(f"Total participants: {data['metadata']['total_participants']}")

# Get participants with conversations
with_convs = [p for p in participants if p['has_conversation']]
print(f"With conversations: {len(with_convs)}")

# Get participants without conversations
without_convs = [p for p in participants if not p['has_conversation']]
print(f"Without conversations: {len(without_convs)}")
```

### CSV Example

```python
import pandas as pd

# Load participant index
df = pd.read_csv('promptdata/PARTICIPANT_INDEX.csv')

print(f"Total participants: {len(df)}")
print(f"With conversations: {df['has_conversation'].sum()}")
print(f"Without conversations: {(~df['has_conversation']).sum()}")
```

## Conversation Data by Folder

| Folder | Conversations | Matched | Match Rate |
|--------|---------------|---------|------------|
| CSN1   | 21 | 20 | 95.2% |
| CSN10  | 17 | 17 | 100.0% |
| CSN11  | 16 | 16 | 100.0% |
| CSN13-18 | - | - | 100.0% |
| Others | - | - | Variable |

See `PARTICIPANT_INDEX.json` for complete mapping of all 604 participants.

## Integration with Main Dataset

The participant index links to the main dataset via `ResponseId`:

```python
# Load main dataset
main_df = pd.read_csv('../data/processed/nhh_esperanto_complete_unified.csv')

# Load participant index
index_df = pd.read_csv('PARTICIPANT_INDEX.csv')

# Join on ResponseId
merged = main_df.merge(index_df, on='ResponseId', how='left')
```

---

**Last Updated**: 2025-11-13
**Dataset Version**: nhh_esperanto_complete_unified.csv
**Total Participants**: 604
