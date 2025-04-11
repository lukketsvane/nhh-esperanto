import Papa from "papaparse";

export type DataRow = Record<string, any>;

// Sample data for fallback
export const SAMPLE_DATA_ROWS: DataRow[] = [
  {
    final_id: "sample-1",
    treatment_clean: "Control",
    gender: "Male",
    highgpa: 1,
    testscore: 85.5,
    index_complement: 4.2,
    index_confidence: 3.8,
    index_cheating: 1.5,
    index_motivation: 4.0,
    MessageCount: 0,
    ConversationDurationMinutes: 0
  },
  {
    final_id: "sample-2",
    treatment_clean: "AI-assisted",
    gender: "Female",
    highgpa: 0,
    testscore: 82.0,
    index_complement: 4.5,
    index_confidence: 4.1,
    index_cheating: 1.2,
    index_motivation: 4.2,
    MessageCount: 12,
    ConversationDurationMinutes: 15.5
  },
  {
    final_id: "sample-3",
    treatment_clean: "AI-guided",
    gender: "Female",
    highgpa: 1,
    testscore: 88.5,
    index_complement: 4.7,
    index_confidence: 4.3,
    index_cheating: 1.0,
    index_motivation: 4.5,
    MessageCount: 18,
    ConversationDurationMinutes: 22.3
  },
  {
    final_id: "sample-4",
    treatment_clean: "Control",
    gender: "Male",
    highgpa: 0,
    testscore: 79.0,
    index_complement: 3.8,
    index_confidence: 3.5,
    index_cheating: 1.8,
    index_motivation: 3.7,
    MessageCount: 0,
    ConversationDurationMinutes: 0
  },
  {
    final_id: "sample-5",
    treatment_clean: "AI-assisted",
    gender: "Female",
    highgpa: 1,
    testscore: 90.0,
    index_complement: 4.9,
    index_confidence: 4.6,
    index_cheating: 1.1,
    index_motivation: 4.8,
    MessageCount: 15,
    ConversationDurationMinutes: 18.2
  }
];

// Default column set for fallback
export const DEFAULT_COLUMNS: string[] = [
  "final_id", "treatment_clean", "gender", "highgpa", "testscore", 
  "index_complement", "index_confidence", "index_cheating", "index_motivation", 
  "MessageCount", "ConversationDurationMinutes"
];

function parseCSV(csvText: string): Promise<{ data: DataRow[]; columns: string[] }> {
  if (typeof csvText !== 'string') {
    console.error("ParseCSV Error: Input is not a string. Received:", typeof csvText);
    return Promise.resolve({ data: [], columns: [] });
  }
  
  if (!csvText.trim()) {
    console.warn("ParseCSV Warning: Input string is empty or whitespace.");
    return Promise.resolve({ data: [], columns: [] });
  }

  return new Promise((resolve, reject) => {
    Papa.parse<DataRow>(csvText, {
      header: true,
      skipEmptyLines: "greedy",
      dynamicTyping: true,
      transformHeader: (header) => header ? header.trim() : '',
      complete: (results) => {
        if (results.errors.length > 0) {
          console.warn("CSV parsing encountered errors, attempting to return partial data.", results.errors);
        }

        let finalColumns = (results.meta.fields || []).filter(col => col && typeof col === 'string' && col.trim() !== '');

        if (finalColumns.length === 0) {
          if (results.data.length > 0 && Object.keys(results.data[0]).length > 0) {
            finalColumns = Object.keys(results.data[0]).filter(col => col && typeof col === 'string' && col.trim() !== '');
          } else {
            return resolve({ data: [], columns: [] });
          }
        }

        const cleanedData = results.data.map((row) => {
          const cleanedRow = { ...row };

          for (const key in cleanedRow) {
            if (typeof cleanedRow[key] === "string") {
              const lowerVal = cleanedRow[key].toLowerCase().trim();
              if (lowerVal === "true") cleanedRow[key] = true;
              else if (lowerVal === "false") cleanedRow[key] = false;
            }

            const numericCols = ["testscore", "MessageCount", "ConversationDurationMinutes", "index_confidence", "index_motivation", "index_complement", "index_cheating", "control", "ai_assist", "ai_guided", "highgpa", "age", "gpa"];
            if (numericCols.includes(key) && typeof cleanedRow[key] === "string") {
              const trimmedVal = cleanedRow[key].trim();
              if (trimmedVal !== "" && !isNaN(Number(trimmedVal))) {
                cleanedRow[key] = Number(trimmedVal);
              } else if (trimmedVal === "") {
                cleanedRow[key] = null;
              }
            }
          }

          cleanedRow.treatment_clean = "Unknown";
          if (typeof cleanedRow.treatment === 'string' && cleanedRow.treatment.trim() !== '') {
            const treatmentLower = cleanedRow.treatment.trim().toLowerCase();
            if (treatmentLower === "control") cleanedRow.treatment_clean = "Control";
            else if (treatmentLower === "ai-assisted" || treatmentLower === "ai_assisted") cleanedRow.treatment_clean = "AI-assisted";
            else if (treatmentLower === "ai-guided" || treatmentLower === "ai_guided") cleanedRow.treatment_clean = "AI-guided";
          }
          if (cleanedRow.treatment_clean === "Unknown") {
            if (Number(cleanedRow.control) === 1) cleanedRow.treatment_clean = "Control";
            else if (Number(cleanedRow.ai_assist) === 1) cleanedRow.treatment_clean = "AI-assisted";
            else if (Number(cleanedRow.ai_guided) === 1) cleanedRow.treatment_clean = "AI-guided";
          }
          return cleanedRow;
        });

        if (!finalColumns.includes("treatment_clean") && cleanedData.length > 0) {
          if (cleanedData.some(row => typeof row.treatment_clean === 'string' && row.treatment_clean !== "Unknown")) {
            finalColumns = [...finalColumns, "treatment_clean"];
          }
        }

        resolve({ data: cleanedData, columns: finalColumns });
      },
      error: (error) => {
        console.error("CSV Parsing Fatal Error:", error);
        reject(error);
      },
    });
  });
}

export async function loadData(): Promise<{ data: DataRow[]; columns: string[] }> {
  console.log('Loading data...');
  
  try {
    // On the client side, we need to use a different approach
    // First check if we're in the browser
    const isBrowser = typeof window !== 'undefined';
    
    if (isBrowser) {
      // Browser-specific code using relative URLs
      const dataSources = [
        { path: './data/esperanto_final_matched_dataset.csv', name: 'Main dataset' },
        { path: './data/esperanto_sample_100.csv', name: 'Sample dataset' }
      ];
      
      let loadedData: { data: DataRow[]; columns: string[] } | null = null;
      
      // Try each data source in order
      for (const source of dataSources) {
        try {
          console.log(`Attempting to load data from ${source.name} (${source.path})...`);
          const response = await fetch(source.path);
          
          if (!response.ok) {
            console.warn(`Failed to load ${source.name}: ${response.status} ${response.statusText}`);
            continue; // Try next source
          }
          
          const csvText = await response.text();
          if (!csvText || csvText.trim().length === 0) {
            console.warn(`${source.name} file was empty`);
            continue; // Try next source
          }
          
          loadedData = await parseCSV(csvText);
          console.log(`Successfully loaded ${loadedData.data.length} rows from ${source.name}`);
          break; // Successfully loaded data, exit the loop
        } catch (sourceError) {
          console.warn(`Error loading from ${source.name}:`, sourceError);
          // Continue to next source
        }
      }
      
      // If we still don't have data, use hardcoded sample data
      if (!loadedData || !loadedData.data.length) {
        console.log('Using hardcoded sample data as client-side fallback');
        return {
          data: SAMPLE_DATA_ROWS,
          columns: DEFAULT_COLUMNS
        };
      }
      
      return loadedData;
    } else {
      // We're in a server component - use hardcoded sample data
      console.log('Server-side rendering, using sample data');
      return {
        data: SAMPLE_DATA_ROWS,
        columns: DEFAULT_COLUMNS
      };
    }
    
  } catch (error) {
    console.error('Data loading failed:', error);
    console.log('Using hardcoded sample data as ultimate fallback');
    
    // Return hardcoded sample data as final fallback
    return {
      data: SAMPLE_DATA_ROWS,
      columns: DEFAULT_COLUMNS
    };
  }
}