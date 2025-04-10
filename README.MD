# NHH Esperanto Learning and Interaction Dataset

## Introduction

This repository contains the **NHH Esperanto Dataset**, a comprehensive collection of data from linguistic experiments focused on learning Esperanto. It integrates survey responses with corresponding ChatGPT conversation logs, providing a rich resource for researchers studying language acquisition, human-computer interaction, and AI-assisted learning. The dataset includes:

*   **Survey Data:** Participant demographics, experimental conditions (control, AI-assisted, AI-guided), test scores, and self-reported metrics.
*   **Conversation Logs:** Full interaction history between participants and ChatGPT during the learning/testing phases.
*   **Session Information:** Mapping of participation times to specific experimental sessions.

The data is available in both CSV and JSON formats.

## Dataset Overview

*   **Total Survey Responses:** [Number, e.g., 425 based on your description]
*   **Total Conversations:** 425
*   **Total Messages:** 10,158
*   **Unique Participants:** [Number, e.g., ~21-30 based on context]
*   **Data Collection Period:** [Start Date, e.g., 28 Nov 2024] to [End Date, e.g., 05 Dec 2024]
*   **Time Range (UNIX):** `1732796573.54373` to `1733512640.880426`

## Data Sources

The unified dataset is compiled from the following sources:

1.  **`iverdata.csv`**: Contains survey responses collected via Qualtrics, including participant details, test performance, and experimental group assignments.
2.  **`schedule_sessions.csv`**: Provides the schedule mapping session times to dates.
3.  **`unified_conversation_data.csv`**: Contains the full ChatGPT conversation logs for all participants. Sample files (`unified_sample_*.csv`/`.json`) are also provided.

## Data Structure (Merged Output Example)

The primary output is an enriched version of `iverdata.csv`, linking survey responses to conversation and session data. Key fields include:

| Field Name        | Type    | Description                                                                 | Origin                     |
| :---------------- | :------ | :-------------------------------------------------------------------------- | :------------------------- |
| `ResponseId`      | str     | Unique identifier for each survey response.                                 | `iverdata.csv`             |
| `StartDate`       | str     | Timestamp when the participant started the survey/experiment.             | `iverdata.csv`             |
| `EndDate`         | str     | Timestamp when the participant finished the survey/experiment.            | `iverdata.csv`             |
| `UserID`          | str     | Participant identifier, often in `DDMMYYYY_HHMM_Participant#` format.       | Extracted/Inferred         |
| `Session`         | str     | Experimental session identifier (e.g., "Session 1").                       | `schedule_sessions.csv`    |
| `conversation_id` | str     | Unique identifier for the associated ChatGPT conversation.                  | `unified_..._data.csv`     |
| `create_time`     | float   | UNIX timestamp when the associated ChatGPT conversation was created.        | `unified_..._data.csv`     |
| `treatment`       | str     | Experimental group (e.g., 'Control', 'AI-assisted', 'AI-guided').           | `iverdata.csv`             |
| `testscore`       | float   | Participant's score on the Esperanto test.                                  | `iverdata.csv`             |
| ...               | ...     | Other fields from `iverdata.csv` (demographics, questions, etc.)            | `iverdata.csv`             |
| `StatedChatID`    | str/None| The ID explicitly stated by the user in the chat, if found.                 | `unified_..._data.csv`     |
| `MatchMethod`     | str     | How the conversation was matched ('ExplicitID' or 'Timestamp').             | Processing Script          |

*(Note: This is an illustrative schema. The final merged file will contain all original columns from `iverdata.csv` plus the added/matched columns.)*

## Download Links

### Full Dataset
*The full conversation dataset is large.*
*   [Download Full Conversation Data (CSV)](https://github.com/lukketsvane/nhh-esperanto/raw/main/unified_conversation_data.csv)
*   [Download Full Conversation Data (JSON)](https://github.com/lukketsvane/nhh-esperanto/raw/main/unified_conversation_data.json)
*   [Download Survey Data (`iverdata.csv`)](https://github.com/lukketsvane/nhh-esperanto/raw/main/iverdata.csv)
*   [Download Session Schedule (`schedule_sessions.csv`)](https://github.com/lukketsvane/nhh-esperanto/raw/main/schedule_sessions.csv)
*   **[Recommended] Download Merged & Enriched Survey Data (CSV):** [Link to the final merged CSV file once created]

### Samples (Conversation Data Only)
*   **Sample of 5 Conversations**:
    *   [CSV](https://github.com/lukketsvane/nhh-esperanto/raw/main/unified_sample_5.csv)
    *   [JSON](https://github.com/lukketsvane/nhh-esperanto/raw/main/unified_sample_5.json)
*   **Sample of 10 Conversations**:
    *   [CSV](https://github.com/lukketsvane/nhh-esperanto/raw/main/unified_sample_10.csv)
    *   [JSON](https://github.com/lukketsvane/nhh-esperanto/raw/main/unified_sample_10.json)
*   **Sample of 100 Conversations**:
    *   [CSV](https://github.com/lukketsvane/nhh-esperanto/raw/main/unified_sample_100.csv)
    *   [JSON](https://github.com/lukketsvane/nhh-esperanto/raw/main/unified_sample_100.json)

## Data Processing and Matching

The unified dataset was created by merging the data sources based on participant identifiers and timestamps.

1.  **UserID Extraction:** Participant IDs (typically in the format `DDMMYYYY_HHMM_Participant#`) were extracted from the initial user messages within the conversation logs where available.
2.  **Timestamp Matching:** For participants who did not explicitly state their ID in the chat, survey responses (`iverdata.csv`) were matched to conversations (`unified_conversation_data.csv`) based on the proximity of the survey `StartDate` and the conversation `create_time`. A tolerance window was used to account for minor timing discrepancies. *Note: This matching assumes participants started their survey and conversation around the same time.*
3.  **Session Mapping:** The `schedule_sessions.csv` file was used to map each participant's start time to a specific experimental session number.
4.  **Consolidation:** The final dataset links each survey response to its corresponding session, conversation ID, and extracted/inferred UserID.

## Usage Notes

*   **Timestamp Accuracy:** Matching based on timestamps might introduce minor inaccuracies if multiple participants started their sessions very close together. The `MatchMethod` column indicates how each link was established.
*   **Missing Data:** Some survey responses may not have a corresponding conversation log, or vice-versa, due to technical issues or participants not completing all parts.
*   **Anonymization:** While participant emails might be present in the raw survey data (`iverdata.csv`), ensure compliance with privacy regulations and ethical guidelines when using this data. User IDs provided are intended for linking purposes within the dataset context.

## License

This dataset is made available under the **Creative Commons Attribution 4.0 International License (CC BY 4.0)**.

[![CC BY 4.0](https://licensebuttons.net/l/by/4.0/88x31.png)](https://creativecommons.org/licenses/by/4.0/)

You are free to:
*   Share — copy and redistribute the material in any medium or format
*   Adapt — remix, transform, and build upon the material

Under the following terms:
*   **Attribution** — You must give appropriate credit to NHH Norwegian School of Economics and the contributors, provide a link to the license, and indicate if changes were made.
