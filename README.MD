# NHH Esperanto Learning and Interaction Dataset

## Introduction

This repository contains the **NHH Esperanto Dataset**, a comprehensive collection of data from linguistic experiments focused on learning Esperanto. It integrates survey responses with corresponding ChatGPT conversation logs, providing a rich resource for researchers studying language acquisition, human-computer interaction, and AI-assisted learning. The dataset includes:

*   **Survey Data:** Participant demographics, experimental conditions (control, AI-assisted, AI-guided), test scores, and self-reported metrics.
*   **Conversation Logs:** Full interaction history between participants and ChatGPT during the learning/testing phases.
*   **Session Information:** Mapping of participation times to specific experimental sessions.

The data is available in both CSV and JSON formats.

## Dataset Overview

*   **Total Survey Responses:** 604
*   **Total Conversations:** 376
*   **Total Messages:** 10,158
*   **Unique Participants:** ~21-30
*   **Data Collection Period:** 28 Nov 2024 to 05 Dec 2024
*   **Time Range (UNIX):** `1732762620.0` to `1733512640.880426`

## Data Sources

The unified dataset is compiled from the following sources:

1.  **`iverdata.csv`**: Contains survey responses collected via Qualtrics, including participant details, test performance, and experimental group assignments.
2.  **`schedule_sessions.csv`**: Provides the schedule mapping session times to dates.
3.  **`unified_conversation_data.csv`**: Contains the full ChatGPT conversation logs for all participants. Sample files (`unified_sample_*.csv`/`.json`) are also provided.

The merged and enriched data is available as:

1.  **`aligned_unified_conversation_data.csv`**: The complete merged dataset with all survey responses.
2.  **`aligned_unified_conversation_data_matched_only.csv`**: A filtered version containing only the 369 matched records.
3.  **`aligned_unified_conversation_data_unmatched_conversations.csv`**: A reference file with the 7 conversations that could not be matched to any survey response.

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
*   **[Recommended] Download Merged & Enriched Survey Data (CSV):** [Download Aligned Data](https://github.com/lukketsvane/nhh-esperanto/raw/main/aligned_unified_conversation_data.csv)

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

The unified dataset was created by merging the data sources based on participant identifiers and timestamps. A Python script (`merge_datasets.py`) was used to implement the matching algorithm.

1.  **UserID Extraction:** Participant IDs (typically in the format `DDMMYYYY_HHMM_Participant#`) were extracted from the initial user messages within the conversation logs where available. The script also looked for other ID formats like "Participant X", date/time references, or simple numerical IDs.
2.  **Timestamp Matching:** For participants who did not explicitly state their ID in the chat, survey responses (`iverdata.csv`) were matched to conversations (`unified_conversation_data.csv`) based on the proximity of the survey `StartDate` and the conversation `create_time`. A tolerance window of 24 hours was used, with matching prioritized by session date to ensure participants were matched within their actual experimental session.
3.  **Session Mapping:** The `schedule_sessions.csv` file was generated to map each participant's start time to a specific experimental session number.
4.  **Conversation Metrics:** For each matched conversation, metrics were calculated including message counts, average message lengths, and conversation duration.
5.  **Consolidation:** The final dataset (`aligned_unified_conversation_data.csv`) links each survey response to its corresponding session, conversation ID, extracted/inferred UserID, and includes the full text of the conversation.

**Matching Results:**
- Total survey responses: 604
- Matches via explicit ID: 8
- Matches via timestamp: 361 
- Total matched: 369 (61.09% match rate)
- Unmatched: 235
- Match confidence: 95.54% average (98.6% of matches have high confidence)

The matching algorithm achieved a good match rate by using both ID extraction and timestamp-based matching with a 24-hour tolerance window, prioritizing matches within the same session day.

## Usage Notes

*   **Timestamp Accuracy:** Matching based on timestamps might introduce minor inaccuracies if multiple participants started their sessions very close together. The `MatchMethod` column indicates how each link was established. We used a 24-hour tolerance window for matching, with a confidence score to measure match quality. The `match_confidence` field provides a 0-100 score based on how close the timestamps are.
*   **Missing Data:** Some survey responses may not have a corresponding conversation log, or vice-versa, due to technical issues or participants not completing all parts. For easier analysis, we provide a filtered version containing only the matched records (`aligned_unified_conversation_data_matched_only.csv`).
*   **Data Enrichment:** The aligned dataset includes additional columns with conversation metrics:
    * `MessageCount`: Total number of messages in the conversation
    * `UserMessageCount`: Number of messages sent by the participant
    * `AIMessageCount`: Number of messages sent by ChatGPT
    * `MessageRatio`: Ratio of user messages to AI messages
    * `AverageUserMessageLength`: Average length of user messages in characters
    * `AverageAIMessageLength`: Average length of AI messages in characters
    * `ConversationDuration`: Duration of the conversation in seconds
    * `ConversationDurationMinutes`: Duration of the conversation in minutes
    * `HasMatch`: Flag indicating whether this survey response was matched to a conversation
    * `timestamp_diff`: The difference between survey start time and conversation start time (seconds)
    * `timestamp_diff_minutes`: The difference between survey start time and conversation start time (minutes)
    * `match_confidence`: Confidence score (0-100%) for the match, based on timestamp proximity
    * `treatment_clean`: Standardized treatment group designation (Control, AI-assisted, AI-guided)
*   **Anonymization:** While participant emails might be present in the raw survey data (`iverdata.csv`), ensure compliance with privacy regulations and ethical guidelines when using this data. User IDs provided are intended for linking purposes within the dataset context.

## License

This dataset is made available under the **Creative Commons Attribution 4.0 International License (CC BY 4.0)**.

[![CC BY 4.0](https://licensebuttons.net/l/by/4.0/88x31.png)](https://creativecommons.org/licenses/by/4.0/)

You are free to:
*   Share — copy and redistribute the material in any medium or format
*   Adapt — remix, transform, and build upon the material

Under the following terms:
*   **Attribution** — You must give appropriate credit to NHH Norwegian School of Economics and the contributors, provide a link to the license, and indicate if changes were made.
