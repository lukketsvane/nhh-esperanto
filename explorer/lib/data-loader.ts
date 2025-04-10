import Papa from "papaparse"

type DataRow = Record<string, any>

function parseCSV(csvText: string): Promise<{ data: DataRow[]; columns: string[] }> {
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

        console.log(`Successfully parsed ${results.data.length} rows from CSV.`)

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
}

// Empty sample header - will show empty UI until client loads
const SAMPLE_DATA = `final_id,treatment_clean,gender,highgpa,testscore,index_confidence,index_motivation,index_complement,index_cheating,MessageCount,ConversationDurationMinutes`;

export async function loadData(): Promise<{ data: DataRow[]; columns: string[] }> {
  console.log('Loading data from public directory');
  try {
    // Check if window is defined (client-side only)
    if (typeof window === 'undefined') {
      console.log('Running on server, using sample data');
      return parseCSV(SAMPLE_DATA);
    }

    // Fetch the CSV file from the public directory (client-side)
    console.log('Fetching CSV from', '/data/nhh_esperanto_finalized_dataset.csv');
    try {
      // Use dynamic import to ensure fetch happens on client
      const response = await fetch('/data/nhh_esperanto_finalized_dataset.csv');
      if (!response.ok) {
        console.error(`HTTP error! status: ${response.status}`);
        // Try alternate datasets if primary fails
        const alternateResponse = await fetch('/data/nhh_esperanto_enhanced_dataset.csv');
        if (!alternateResponse.ok) {
          throw new Error(`Failed to load any dataset files`);
        }
        const csvText = await alternateResponse.text();
        return parseCSV(csvText);
      }
      const csvText = await response.text();
      return parseCSV(csvText);
    } catch (fetchError) {
      console.error('Error fetching CSV:', fetchError);
      throw fetchError;
    }
  } catch (error) {
    console.error(`Error parsing CSV sample data:`, error)
    return { data: [], columns: [] }
  }
}
