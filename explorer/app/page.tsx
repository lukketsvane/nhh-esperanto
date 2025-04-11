"use client";
import { loadData } from '@/lib/data-loader';
import { Info } from 'lucide-react';
import DataExplorer from '@/components/data-explorer';
export default async function Page() {
  try {
    const { data, columns } = await loadData();
    
    console.log(`Data loaded in Page: ${data?.length} rows, ${columns?.length} columns.`);

    // Handle case where loader returns empty columns
    if (!columns || columns.length === 0) {
      console.error("Page received no columns from loadData.");
      return (
        <div className="flex flex-col items-center justify-center min-h-screen p-4 text-center text-destructive">
          <Info className="h-10 w-10 mb-4"/>
          <p className="text-lg font-semibold">Failed to Load Data</p>
          <p>Could not load or parse the dataset. Please check the file path and ensure the CSV format is valid.</p>
          <p className="text-sm mt-2">(Check browser console and server logs for more details)</p>
        </div>
      );
    }

    // Pass the loaded data to the client component
    return <DataExplorer initialData={data} initialColumns={columns} />;

  } catch (error) {
    console.error("Fatal error loading data in Page component:", error);
    return (
      <div className="flex flex-col items-center justify-center h-screen text-destructive p-4 text-center">
         <Info className="h-10 w-10 mb-4"/>
         <p className="text-lg font-semibold">Error Loading Application Data</p>
         <p>An unexpected error occurred while trying to load the initial data.</p>
         <p className="text-sm mt-2">{error instanceof Error ? error.message : 'Unknown error'}</p>
      </div>
    );
  }
}