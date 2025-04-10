# NHH Esperanto Data Explorer

A Next.js application for exploring, visualizing, and analyzing conversation data from the NHH Esperanto experiment.

## Features

- Interactive data tables with filtering and pagination
- Multiple visualization types (box plots, bar charts, histograms, scatter plots)
- Statistical summaries and frequency distributions
- Grouped summary statistics by treatment and other variables
- Data export functionality

## Getting Started

1. **Install dependencies**
   ```
   npm install --legacy-peer-deps
   ```
   or
   ```
   pnpm install --no-strict-peer-dependencies
   ```

2. **Run the development server**
   ```
   npm run dev
   ```

3. **Build for production**
   ```
   npm run build
   npm start
   ```

## Application Structure

- `app/`: Next.js application entry point and pages
- `components/`: React components for data visualization and UI
- `lib/`: Utility functions and data loading logic
- `public/`: Static assets
- `styles/`: Global CSS styles

## Data Source

The application loads data from CSV files in the parent directory. The primary dataset used is:
`../aligned_unified_conversation_data.csv`