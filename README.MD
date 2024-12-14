# NHH Esperanto Dataset

This repository hosts the **NHH Esperanto Dataset**, a unified collection of 10,158 messages across 425 conversations related to Esperanto learning and linguistic experiments. Designed for researchers and developers, the dataset is accessible in CSV and JSON formats for easy analysis.

## Direct Download Links

### Full Dataset
- [Download Full Dataset (CSV)](https://github.com/lukketsvane/nhh-esperanto/raw/main/unified_conversation_data.csv)
- [Download Full Dataset (JSON)](https://github.com/lukketsvane/nhh-esperanto/raw/main/unified_conversation_data.json)

### Samples
- **Sample of 5 Conversations**:
  - [CSV](https://github.com/lukketsvane/nhh-esperanto/raw/main/unified_sample_5.csv)  
  - [JSON](https://github.com/lukketsvane/nhh-esperanto/raw/main/unified_sample_5.json)
- **Sample of 10 Conversations**:
  - [CSV](https://github.com/lukketsvane/nhh-esperanto/raw/main/unified_sample_10.csv)  
  - [JSON](https://github.com/lukketsvane/nhh-esperanto/raw/main/unified_sample_10.json)
- **Sample of 100 Conversations**:
  - [CSV](https://github.com/lukketsvane/nhh-esperanto/raw/main/unified_sample_100.csv)  
  - [JSON](https://github.com/lukketsvane/nhh-esperanto/raw/main/unified_sample_100.json)

## Overview

- **Total Messages**: 10,158
- **Total Conversations**: 425
- **Unique Users**: 21
- **Earliest Message Time**: `1732796573.54373` (UNIX timestamp)
- **Latest Message Time**: `1733512640.880426` (UNIX timestamp)

## Data Structure

```json
{
    "conversation_id": "str",
    "conversation_title": "str",
    "create_time": "float",
    "update_time": "float",
    "message_id": "str",
    "author_role": "str",
    "author_name": "str",
    "message_content": ["str"],
    "message_status": "str",
    "recipient": "str",
    "channel": "str"
}
```

## License

This dataset is licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). Proper attribution to NHH, and the contributors is required.

---

For questions or feedback, contact [lukketsvane](https://github.com/lukketsvane).
