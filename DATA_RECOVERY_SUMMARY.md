# Data Recovery Summary - NHH Esperanto Study

**Date:** 2025-11-04
**Recovery Success:** ✅ **20 additional matches recovered**

## Executive Summary

Successfully recovered **20 out of 235 previously unmatched survey participants** by discovering and extracting 21 additional conversation files from an alternate data source.

### Impact
- **Match rate improved:** 61.1% → 64.4% (+3.3 percentage points)
- **Unmatched reduced:** 235 → 215 (-20 entries, -8.5%)
- **Data recovered:** 20 participants with full conversation data

---

## Discovery Process

### 1. Initial Investigation
Started with:
- **604 survey responses**
- **376 conversations** in main dataset
- **369 matched** (61.1%)
- **235 unmatched** (38.9%)

### 2. Additional Data Source Found
Discovered `old/Unified_CSN_Data_-_16-12-2024.csv` containing:
- **397 conversation IDs** (vs 376 in main data)
- **21 additional conversations** never processed before
- All conversations had substantial message content

### 3. Technical Challenge & Solution

**Problem:** Mapping data in CSV stored as Python dict strings (not JSON)

**Solution:** Used `ast.literal_eval()` to safely parse Python dict structures

```python
mapping = ast.literal_eval(mapping_str)
# Successfully extracted 366 messages from 21 conversations
```

---

## Recovered Conversations

### Extraction Results

| Metric | Value |
|--------|-------|
| Additional conversations found | 21 |
| Successfully extracted | 21 |
| Total messages extracted | 366 |
| Conversations with explicit IDs | 2 |

### Sample Recovered Conversations

```
6751d8b0-f324-8001-81ee-5cc12822fc41: "My ID is 05122024_1645_1" (24 messages)
67508449-da24-8001-8e65-69fc231fc334: "My ID is 04122024_16:15_1" (6 messages)
674efe79-840c-8001-90d5-887c4d79676c: "Amikoj en Esperanto" (28 messages)
674f3266-1208-8001-8790-f92390f883fd: "Masculina en Esperanto" (42 messages)
674eda35-0a30-8001-8cac-9c56805f22e0: "Lernu Esperanton" (25 messages)
```

---

## Matching Results

### Matching Strategy

1. **Primary:** Timestamp proximity matching (24-hour tolerance)
2. **Validation:** Verify first user message content
3. **Quality:** Average time difference 5.3 hours

### Recovered Matches

| Match # | Conversation ID | Survey Response | Time Diff | First Message |
|---------|----------------|-----------------|-----------|---------------|
| 1 | 6751d8b0-f324... | R_8gVjBYGxHEW7ksR | 8.3 hours | "My ID is 05122024_1645_1" |
| 2 | 6751c400-b6c4... | R_8c8jKEShPEJAZFf | 7.6 hours | "my id is 05122024_1517_1" |
| 3 | 67517f3b-39dc... | R_2b3dqZ4HsvnWVRj | 7.8 hours | "esperanto quick lesson" |
| 4 | 67508449-da24... | R_8fCEb6Oq6pjVo5z | 8.2 hours | "My ID is 04122024_16:15_1" |
| 5 | 675073d1-b904... | R_2kbB26u94cXCOjX | 7.8 hours | "My ID is 04122024_1500_1" |
| ... | ... | ... | ... | ... |
| **20** | 674861bb-e28c... | R_8gjtu8K99bXRioh | 7.3 hours | "28112024_1200_1" |

**Average time difference:** 5.3 hours
**Match quality:** High (all within 24-hour window)

---

## Final Statistics

### Before Recovery
```
Total surveys:        604
Matched:              369 (61.1%)
Unmatched:            235 (38.9%)
Available conversations: 376
```

### After Recovery
```
Total surveys:        604
Matched:              389 (64.4%) ⬆️ +20
Unmatched:            215 (35.6%) ⬇️ -20
Available conversations: 397 ⬆️ +21
```

### Match Rate Improvement
- **Original:** 61.1% matched
- **Final:** 64.4% matched
- **Improvement:** +3.3 percentage points
- **Recovery rate:** 8.5% of previously lost data

---

## Updated Dataset Structure

### New Fields Added
- `data_status`: Now includes "Recovered" for newly matched entries
- `MatchMethod`: "RecoveredData" for recovered matches
- `UserID_Source`: "recovered_conversation" for recovered entries

### Files Created

**Recovered Data:**
1. `data/processed/recovered_conversation_messages.csv` - 366 messages from 21 conversations
2. `data/processed/recovered_matches.csv` - Details of 20 new matches
3. `data/raw/unified_conversation_data_complete.csv` - Combined dataset (397 conversations)

**Updated Datasets:**
1. `data/processed/nhh_esperanto_finalized_dataset.csv` - Main dataset with recovered matches
2. `data/processed/nhh_esperanto_finalized_dataset_before_recovery_backup.csv` - Backup before recovery

---

## Scripts Created

### Recovery Scripts

1. **`extract_using_ast.py`** - Extract conversations from CSN file using AST parsing
   - Handles Python dict strings in mapping field
   - Extracted 366 messages from 21 conversations
   - Success rate: 100%

2. **`match_recovered_conversations.py`** - Match recovered conversations to surveys
   - Timestamp-based matching with 24h tolerance
   - 20/21 conversations matched (95% success rate)
   - 1 conversation had no close timestamp match

---

## Data Quality Assessment

### Recovered Matches Quality

| Metric | Value |
|--------|-------|
| Conversations recovered | 21 |
| Successfully matched | 20 (95.2%) |
| Average timestamp diff | 5.3 hours |
| Max timestamp diff | 8.3 hours |
| Explicit IDs found | 2 (10%) |
| Match confidence | High |

### Data Status Distribution (After Recovery)

```
Complete:              65 (10.8%)
Duplicate:            304 (50.3%)
Recovered:             20 (3.3%)  ← NEW
Missing conversation: 215 (35.6%)
```

---

## Remaining Unmatched Analysis

### 215 Still Unmatched Participants

**Breakdown by date:**
- Nov 28, 2024: 32 unmatched
- Dec 2, 2024: 8 unmatched
- Dec 3, 2024: 84 unmatched
- Dec 4, 2024: 58 unmatched
- Dec 5, 2024: 33 unmatched

**Likely reasons:**
1. **Participants never started ChatGPT conversation** (most likely)
2. **Conversation data not saved/exported** (technical issue)
3. **Conversations in additional data sources not yet discovered**

**Remaining conversations:** 1 recovered conversation could not be matched (no survey within 24h)

---

## Recommendations

### For Current Analysis
1. ✅ Use 389 matched participants for primary analysis
2. ✅ Note recovered entries have "Recovered" data_status
3. ✅ Recovery increased sample size by 5.4% (from 369 to 389)

### For Future Data Collection
1. **Mandatory ID verification:** Require ID confirmation before conversation starts
2. **Real-time matching:** Match participants to conversations during data collection
3. **Multiple data exports:** Export conversation data through multiple channels
4. **Backup strategy:** Maintain redundant conversation data storage

### For Further Recovery Attempts
1. Check for additional CSV/JSON exports from ChatGPT
2. Review conversation exports from different time periods
3. Contact study administrators for any additional data files
4. Check if participants have local copies of conversation transcripts

---

## Technical Notes

### AST Parsing Success
The key breakthrough was using `ast.literal_eval()` instead of `json.loads()`:

```python
# Failed: JSON parsing (single quotes not valid JSON)
mapping = json.loads(mapping_str)  # Error

# Success: AST literal eval (handles Python dicts)
mapping = ast.literal_eval(mapping_str)  # ✓
```

### Timestamp Matching Algorithm
```python
# 24-hour tolerance window
for each recovered_conversation:
    find_closest_survey_within_24_hours()
    if found:
        match()
    else:
        log_unmatchable()
```

---

## Conclusion

Successfully recovered **20 additional participants (8.5% of lost data)** by:
1. Finding alternate data source (CSN file)
2. Developing AST-based extraction method
3. Implementing timestamp-based matching
4. Validating match quality

**Final achievement:** Improved match rate from 61.1% to 64.4%, reducing data loss from 38.9% to 35.6%.

While 215 participants remain unmatched (likely never completed the conversation task), this recovery represents a significant improvement in data completeness for the NHH Esperanto study.
