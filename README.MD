# NHH Esperanto - Data Explorer

A Next.js application for exploring, visualizing, and analyzing conversation data from the NHH Esperanto experiment.

## Overview

This application provides a comprehensive interface for researchers to:

- View and filter tabular data
- Create visualizations including bar charts, box plots, histograms, and scatter plots
- Generate statistical summaries and frequency distributions
- Export data for further analysis

## Features

### Data Table View
- View records with pagination
- Filter by any column
- Toggle visibility of columns
- Export filtered data as CSV

### Data Visualization
- Multiple chart types:
  - Box plots: Show distributions with quartiles
  - Bar charts: Compare means across categories
  - Histograms: Visualize value distributions
  - Scatter plots: Explore relationships between variables
- Group data by categories
- Download chart images

### Data Summary
- Column statistics (count, unique values, min/max, mean, median, std dev)
- Grouped summary statistics by any categorical variable
- Frequency distributions
- Missing value analysis

## Dataset Overview

The dataset comprises information from language learning experiments where participants were assigned to different treatment groups:

- **Control**: No AI assistance
- **AI-assisted**: Basic AI assistance 
- **AI-guided**: Enhanced AI assistance with structured guidance

For each participant, the dataset includes demographic information, language learning performance metrics, and conversation data with AI assistants.

## Technical Details

### Tech Stack
- **Framework**: Next.js 15
- **UI Library**: React 19
- **Styling**: Tailwind CSS
- **Components**: shadcn/ui
- **Charts**: Chart.js with BoxPlot extension
- **Data Parsing**: Papa Parse

### Data Processing
The application loads CSV data from a GitHub repository URL and processes it client-side:
- CSV parsing with Papa Parse
- Data cleaning and type normalization
- Treatment group categorization
- Statistical calculations

## Getting Started

1. **Clone the repository**
   ```
   git clone https://github.com/lukketsvane/nhh-esperanto.git
   cd nhh-esperanto
   ```

2. **Install dependencies**
   ```
   npm install --legacy-peer-deps
   ```
   or
   ```
   pnpm install --no-strict-peer-dependencies
   ```

3. **Run the development server**
   ```
   npm run dev
   ```
   or
   ```
   pnpm dev
   ```

4. **Open your browser**
   
   Navigate to [http://localhost:3000](http://localhost:3000)

## Data Files

The primary dataset is loaded from:
`aligned_unified_conversation_data.csv`

Key variables include:
- `final_id`: Participant ID
- `treatment_clean`: Treatment group (Control, AI-assisted, AI-guided)
- `gender`: Participant gender
- `highgpa`: Binary indicator for high GPA
- `testscore`: Score on Esperanto language test
- `index_confidence`, `index_motivation`, `index_complement`, `index_cheating`: Psychological indices
- `MessageCount`: Total messages in conversation
- `ConversationDurationMinutes`: Duration of conversation

## Deployment

The application can be built for production using:
```
npm run build
npm start
```
or
```
pnpm build
pnpm start
```

## License

[MIT License](LICENSE)