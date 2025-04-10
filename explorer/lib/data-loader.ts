import Papa from "papaparse"

type DataRow = Record<string, any>

// Hardcoded sample data for this demo (this would normally come from an API)
const SAMPLE_DATA = `final_id,treatment_clean,gender,highgpa,testscore,index_confidence,index_motivation,index_complement,index_cheating,MessageCount,ConversationDurationMinutes
1,Control,Female,1,75,3.5,4.2,2.8,1.5,15,18.3
2,AI-assisted,Male,0,82,4.1,4.5,3.2,1.2,25,22.1
3,AI-guided,Female,1,89,4.4,4.7,3.7,1.1,32,25.8
4,Control,Male,0,71,3.2,3.9,2.5,1.7,12,15.4
5,AI-assisted,Female,1,84,4.2,4.6,3.3,1.3,27,23.2
6,AI-guided,Male,1,91,4.6,4.8,3.9,1.0,35,28.1
7,Control,Female,0,73,3.3,4.0,2.7,1.6,14,17.2
8,AI-assisted,Male,1,85,4.3,4.6,3.4,1.2,29,24.5
9,AI-guided,Female,0,88,4.5,4.7,3.6,1.1,33,26.3
10,Control,Male,1,72,3.4,4.1,2.6,1.8,13,16.8`;

export async function loadData(): Promise<{ data: DataRow[]; columns: string[] }> {
  console.log('Loading data from public directory');
  try {
    // Fetch the CSV file from the public directory
    const response = await fetch('/data/nhh_esperanto_finalized_dataset.csv');
    const csvText = await response.text();

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

          console.log(`Successfully parsed ${results.data.length} rows from CSV file.`)

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
    console.error(`Error parsing CSV sample data:`, error)
    return { data: [], columns: [] }
  }
}
