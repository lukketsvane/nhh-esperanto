import Papa from "papaparse"
import fs from 'fs/promises';
import path from 'path';

type DataRow = Record<string, any>

// Use the local file paths
const CSV_PATH = path.join(process.cwd(), '..', 'data', 'processed', 'nhh_esperanto_enhanced_dataset.csv');
const CONVERSATIONS_PATH = path.join(process.cwd(), '..', 'data', 'processed', 'nhh_esperanto_conversations.csv');
const PARTICIPANTS_PATH = path.join(process.cwd(), '..', 'data', 'processed', 'nhh_esperanto_participants.csv');

export async function loadData(): Promise<{ data: DataRow[]; columns: string[] }> {
  console.log(`Attempting to load data from: ${CSV_PATH}`)
  try {
    // Read the file from the local filesystem
    const csvText = await fs.readFile(CSV_PATH, 'utf8');

    return new Promise((resolve, reject) => {
      Papa.parse<DataRow>(csvText, {
        header: true,
        skipEmptyLines: "greedy",
        dynamicTyping: true,
        transformHeader: (header) => header.trim(),
        complete: (results) => {
          if (results.errors.length > 0) {
            console.error("CSV Parsing Errors:", results.errors)
            console.warn("CSV parsing encountered errors, data might be incomplete or incorrect.")
          }
          if (!results.meta.fields || results.meta.fields.length === 0) {
            console.error("CSV Parsing Error: No headers found or empty file.")
            return resolve({ data: [], columns: [] })
          }

          console.log(`Successfully parsed ${results.data.length} rows from URL.`)

          // Clean and process the data
          const cleanedData = results.data.map((row) => {
            const cleanedRow = { ...row }

            // Handle boolean values
            for (const key in cleanedRow) {
              if (typeof cleanedRow[key] === "string") {
                const lowerVal = cleanedRow[key].toLowerCase()
                if (lowerVal === "true") cleanedRow[key] = true
                else if (lowerVal === "false") cleanedRow[key] = false
              }

              // Ensure numeric columns are numbers
              const numericCols = ["testscore", "MessageCount", "ConversationDurationMinutes"]
              if (numericCols.includes(key) && typeof cleanedRow[key] === "string" && !isNaN(Number(cleanedRow[key]))) {
                cleanedRow[key] = Number(cleanedRow[key])
              }
            }

            // Clean treatment variable
            if (cleanedRow.treatment === "Control") cleanedRow.treatment_clean = "Control"
            else if (cleanedRow.treatment === "AI-assisted") cleanedRow.treatment_clean = "AI-assisted"
            else if (cleanedRow.treatment === "AI-guided") cleanedRow.treatment_clean = "AI-guided"
            else if (cleanedRow.control === 1) cleanedRow.treatment_clean = "Control"
            else if (cleanedRow.ai_assist === 1) cleanedRow.treatment_clean = "AI-assisted"
            else if (cleanedRow.ai_guided === 1) cleanedRow.treatment_clean = "AI-guided"
            else cleanedRow.treatment_clean = "Unknown"

            return cleanedRow
          })

          // Add treatment_clean to columns if not already present
          const finalColumns = results.meta.fields.includes("treatment_clean")
            ? results.meta.fields
            : [...results.meta.fields, "treatment_clean"]

          resolve({ data: cleanedData, columns: finalColumns })
        },
        error: (error) => {
          console.error("CSV Parsing Fatal Error:", error)
          reject(error)
        },
      })
    })
  } catch (error) {
    console.error(`Error loading or parsing CSV from URL ${CSV_URL}:`, error)
    return { data: [], columns: [] }
  }
}
