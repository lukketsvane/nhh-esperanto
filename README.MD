# NHH Esperanto Dataset

Welcome to the **NHH Esperanto Dataset** repository! This project hosts a meticulously unified dataset of conversations related to Esperanto learning and linguistic experiments. The dataset is intended for researchers, developers, and language enthusiasts interested in studying interaction patterns, language learning dynamics, or natural language processing applications.

## Repository Contents

### Datasets
- **Full Unified Dataset**: A complete dataset containing 10,158 messages across 425 conversations.
- **Sample Sets**:
  - Sample of 5 conversations
  - Sample of 10 conversations
  - Sample of 100 conversations

### Data Formats
Each dataset is available in:
- **CSV**: Suitable for spreadsheet tools and quick data exploration.
- **JSON**: Ideal for programmatic access and detailed analysis.

### Files
| Filename                         | Description                                   |
|----------------------------------|-----------------------------------------------|
| `unified_conversation_data.csv`  | Full dataset in CSV format.                  |
| `unified_conversation_data.json` | Full dataset in JSON format.                 |
| `unified_sample_5.csv`           | Sample of 5 conversations in CSV format.     |
| `unified_sample_5.json`          | Sample of 5 conversations in JSON format.    |
| `unified_sample_10.csv`          | Sample of 10 conversations in CSV format.    |
| `unified_sample_10.json`         | Sample of 10 conversations in JSON format.   |
| `unified_sample_100.csv`         | Sample of 100 conversations in CSV format.   |
| `unified_sample_100.json`        | Sample of 100 conversations in JSON format.  |

## Dataset Overview

### Quick Facts
- **Total Messages**: 10,158
- **Total Conversations**: 425
- **Unique Users**: 21
- **Earliest Message Time**: `1732796573.54373` (UNIX timestamp)
- **Latest Message Time**: `1733512640.880426` (UNIX timestamp)

### Data Structure
The dataset follows this structure:
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

### Sample Entry (JSON)
```json
{
    "conversation_id": "674f4589-ca74-8008-8b23-e25b8c6526f5",
    "conversation_title": "Esperanto Learning Tips",
    "create_time": 1732796573.54373,
    "update_time": 1732796590.12345,
    "message_id": "abc12345",
    "author_role": "user",
    "author_name": null,
    "message_content": ["How do you say 'good morning' in Esperanto?"],
    "message_status": "finished_successfully",
    "recipient": "assistant",
    "channel": null
}
```

## How to Use the Dataset

1. **Download the Dataset**:
   Clone the repository or download individual files directly.

   ```bash
   git clone https://github.com/lukketsvane/nhh-esperanto.git
   ```

2. **Access Files**:
   - Navigate to the `datasets` folder.
   - Use your preferred tools or programming languages to load and analyze the data.

3. **Explore and Analyze**:
   - Use Python, R, or SQL for in-depth analysis.
   - Visualize patterns in conversations or linguistic phenomena.

## Direct Download Links

### Full Dataset
- [CSV Format](https://github.com/lukketsvane/nhh-esperanto/raw/main/unified_conversation_data.csv)
- [JSON Format](https://github.com/lukketsvane/nhh-esperanto/raw/main/unified_conversation_data.json)

### Samples
- **Sample of 5 Conversations**:
  - [CSV Format](https://github.com/lukketsvane/nhh-esperanto/raw/main/unified_sample_5.csv)
  - [JSON Format](https://github.com/lukketsvane/nhh-esperanto/raw/main/unified_sample_5.json)
- **Sample of 10 Conversations**:
  - [CSV Format](https://github.com/lukketsvane/nhh-esperanto/raw/main/unified_sample_10.csv)
  - [JSON Format](https://github.com/lukketsvane/nhh-esperanto/raw/main/unified_sample_10.json)
- **Sample of 100 Conversations**:
  - [CSV Format](https://github.com/lukketsvane/nhh-esperanto/raw/main/unified_sample_100.csv)
  - [JSON Format](https://github.com/lukketsvane/nhh-esperanto/raw/main/unified_sample_100.json)

## License

This dataset is licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). This acknowledges the contributions of NHH, Harvard University, and other collaborators while ensuring the data is freely accessible with proper attribution.

## Contributions

Contributions are welcome! Feel free to open an issue or submit a pull request for improvements or additional features.

## Acknowledgements

This dataset is a collaborative effort between:
- **Norwegian School of Economics (NHH)**
- Researchers Catalina Franco, Natalie Irmert, and Siri Isakson

---
