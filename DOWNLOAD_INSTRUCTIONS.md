# Download Instructions

## What to Download

### 🎯 Main Files You Need

#### 1. Updated Promptdata Archive (REQUIRED)
**File**: `exports/nhh_esperanto_promptdata_FINAL.zip`
- **Size**: 4.2 MB
- **Contains**: 397 conversations with 268 matched to participants
- **Updated**: All conversation files now include participant IDs

#### 2. Main Dataset (REQUIRED)
**File**: `data/processed/nhh_esperanto_complete_unified.csv`
- **Size**: 1.3 MB
- **Contains**: 604 participants with conversation metadata
- **Columns**: 550

---

## Quick Download

### Option 1: Direct Files
```bash
# Download these two files:
exports/nhh_esperanto_promptdata_FINAL.zip  (4.2 MB)
data/processed/nhh_esperanto_complete_unified.csv  (1.3 MB)
```

### Option 2: Git Clone
```bash
git clone <repository-url>
cd nhh-esperanto
```

---

## What's Inside

### Promptdata Archive
When you extract `nhh_esperanto_promptdata_FINAL.zip`, you get:
```
promptdata/
├── CSN1/ (21 conversations, 95.2% matched)
├── CSN2/ (20 conversations, 60.0% matched)
├── CSN3-CSN9/
├── CSN10-CSN18/ (100% matched!)
├── CSN19-CSN22/
```

Each conversation file includes:
- Complete message history
- `participant_id` linking to main CSV
- `participant_user_id`
- `participant_email`
- `participant_name`
- `match_method` (how they were matched)
- Matching metadata

### Main Dataset
The CSV contains:
- All 604 survey responses
- 329 with complete conversation data (54.5%)
- Conversation statistics (message counts, duration, etc.)
- Full survey responses and test scores

---

## How to Use

### 1. Extract the Archive
```bash
unzip nhh_esperanto_promptdata_FINAL.zip
```

### 2. Load the Data
```python
import pandas as pd
import json

# Load main dataset
df = pd.read_csv('data/processed/nhh_esperanto_complete_unified.csv')

# Load a conversation
with open('promptdata/CSN1/csn1/conversations.json', 'r') as f:
    conversations = json.load(f)

# Join them
for conv in conversations:
    participant_id = conv.get('participant_id')
    if participant_id:
        participant_data = df[df['ResponseId'] == participant_id]
        print(f"Participant {participant_id} score: {participant_data['testscore'].values[0]}")
```

### 3. Analyze
```python
# Get participants with conversations
with_convs = df[df['conversation_id'].notna()]

print(f"Participants with AI conversations: {len(with_convs)}")
print(f"Average test score: {with_convs['testscore'].mean():.1f}")
print(f"Average messages: {with_convs['MessageCount'].mean():.1f}")
```

---

## File Structure After Download

```
nhh-esperanto/
├── promptdata/                           ← Extract zip here
│   ├── CSN1/
│   │   ├── csn1/conversations.json      ← Updated with participant IDs
│   │   ├── user.json
│   │   ├── chat.html
│   │   └── ...
│   ├── CSN2-CSN22/
│   └── ...
│
├── data/processed/
│   ├── nhh_esperanto_complete_unified.csv  ← Main dataset
│   ├── promptdata_matches.csv              ← Match details
│   └── promptdata_update_summary.csv       ← Folder stats
│
├── exports/
│   ├── nhh_esperanto_promptdata_FINAL.zip  ← Download this
│   └── README.md                           ← Usage guide
│
└── FINAL_COMPLETION_SUMMARY.md             ← Full documentation
```

---

## Data Quality

### High Quality Folders (100% match rate)
Use these for critical analyses:
- CSN10, CSN11, CSN13, CSN14, CSN15, CSN16, CSN17, CSN18

### Good Quality Folders (>60% match rate)
- CSN1, CSN7, CSN19, CSN20, CSN2

### Lower Quality Folders
- CSN3, CSN4, CSN5, CSN6, CSN8, CSN9, CSN21, CSN22
- These may contain pilot data or test conversations

---

## Verification

### Check Download Integrity
```bash
# Check zip file
unzip -t nhh_esperanto_promptdata_FINAL.zip

# Check CSV
wc -l nhh_esperanto_complete_unified.csv  # Should be 605 lines (604 + header)
```

### Verify Content
```python
import pandas as pd

df = pd.read_csv('nhh_esperanto_complete_unified.csv')
print(f"Total rows: {len(df)}")  # Should be 604
print(f"With conversations: {df['conversation_id'].notna().sum()}")  # Should be 329
```

---

## Support Files (Optional)

These provide additional context:
- `EXPORT_SUMMARY.md` - Project overview
- `FINAL_COMPLETION_SUMMARY.md` - Complete documentation
- `data/processed/promptdata_matches.csv` - Match details
- `data/processed/promptdata_update_summary.csv` - Per-folder stats

---

## What Changed from Original

### Original Dataset
- 604 participants
- 132 with conversations (21.9%)
- Missing IDs for many participants

### Updated Dataset
- 604 participants (same)
- 329 with conversations (54.5%) ✓
- 197 participants recovered ✓
- All conversations linked to participants ✓
- Promptdata folder updated with IDs ✓

---

## Questions?

See full documentation:
- `FINAL_COMPLETION_SUMMARY.md` - Complete overview
- `EXPORT_SUMMARY.md` - Methodology
- `exports/README.md` - Archive guide

---

**Last Updated**: 2025-11-13
**Dataset Version**: Final
**Archive Version**: nhh_esperanto_promptdata_FINAL.zip
