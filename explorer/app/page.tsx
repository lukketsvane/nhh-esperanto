"use client";
import Papa from 'papaparse';
import React, { useState, useMemo, useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';
import { BoxPlotController, BoxAndWiskers } from '@sgratzl/chartjs-chart-boxplot';

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Checkbox } from "@/components/ui/checkbox";
import { DropdownMenu, DropdownMenuCheckboxItem, DropdownMenuContent, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogClose } from "@/components/ui/dialog";
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { Info, Loader2, Download, Search, Filter, BarChart, PieChart, LineChart, TableIcon, Columns, AreaChart, MessageSquare, TrendingUp, Box } from "lucide-react";

Chart.register(BoxPlotController, BoxAndWiskers);

function calculateBoxPlotStats(data: number[]): { min: number; q1: number; median: number; q3: number; max: number; mean: number; count: number; stdDev: number } | null {
    if (!data || data.length === 0) return null;
    const sortedData = [...data].sort((a, b) => a - b);
    const n = sortedData.length;
    const q1Index = Math.floor(n / 4);
    const medianIndex = Math.floor(n / 2);
    const q3Index = Math.floor((3 * n) / 4);

    const q1 = n % 4 === 0 ? (sortedData[q1Index - 1] + sortedData[q1Index]) / 2 : sortedData[q1Index];
    const median = n % 2 === 0 ? (sortedData[medianIndex - 1] + sortedData[medianIndex]) / 2 : sortedData[medianIndex];
    const q3 = n % 4 === 0 ? (sortedData[q3Index - 1] + sortedData[q3Index]) / 2 : sortedData[q3Index];

    const iqr = q3 - q1;
    const lowerFence = q1 - 1.5 * iqr;
    const upperFence = q3 + 1.5 * iqr;

    const outliers = sortedData.filter(d => d < lowerFence || d > upperFence);
    const nonOutliers = sortedData.filter(d => d >= lowerFence && d <= upperFence);

    const min = nonOutliers.length > 0 ? Math.min(...nonOutliers) : sortedData[0]; // Use actual min if no non-outliers
    const max = nonOutliers.length > 0 ? Math.max(...nonOutliers) : sortedData[n - 1]; // Use actual max

    const sum = data.reduce((acc, val) => acc + val, 0);
    const mean = sum / n;
    const stdDev = n > 1 ? Math.sqrt(data.reduce((acc, val) => acc + Math.pow(val - mean, 2), 0) / (n - 1)) : 0;

    return { min, q1, median, q3, max, mean, count: n, stdDev };
}


interface DataTableProps {
  data: any[];
  columns: string[];
  allColumns: string[];
  filters: Record<string, string>;
  onFilterChange: (column: string, value: string) => void;
  setFilters: React.Dispatch<React.SetStateAction<Record<string, string>>>;
  selectedColumns: string[];
  onColumnToggle: (column: string) => void;
  onRowClick: (row: DataRow) => void; // Added for modal trigger
}

function DataTableComponent({
  data,
  columns,
  allColumns,
  filters,
  onFilterChange,
  setFilters,
  selectedColumns,
  onColumnToggle,
  onRowClick
}: DataTableProps) {
  const [showFilters, setShowFilters] = useState(false);

  const clearFilters = () => {
    setFilters({});
    setShowFilters(false);
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-2 gap-2 px-4 pt-2">
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline" className="flex items-center gap-1 text-sm h-9">
              <Columns className="h-4 w-4" />
              Columns ({selectedColumns.length})
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="start" className="max-h-[400px] overflow-y-auto">
            <DropdownMenuLabel>Toggle Columns</DropdownMenuLabel>
            <DropdownMenuSeparator />
            {allColumns.map((column) => (
              <DropdownMenuCheckboxItem
                key={column}
                checked={selectedColumns.includes(column)}
                onCheckedChange={() => onColumnToggle(column)}
                onSelect={(e) => e.preventDefault()}
              >
                {column}
              </DropdownMenuCheckboxItem>
            ))}
          </DropdownMenuContent>
        </DropdownMenu>

        <div className='flex items-center gap-1'>
            <Button
            variant="outline"
            onClick={() => setShowFilters(!showFilters)}
            className="flex items-center gap-1 text-sm h-9"
            >
            <Filter className="h-4 w-4" />
            {showFilters ? "Hide Filters" : "Show Filters"}
            </Button>
            {showFilters && Object.values(filters).some(val => val) && (
            <Button
                variant="ghost"
                onClick={clearFilters}
                className="text-xs h-9 px-2 text-muted-foreground hover:bg-muted"
                title="Clear all column filters"
            >
                Clear
            </Button>
            )}
        </div>
      </div>

      <div className="rounded-md border overflow-x-auto">
        <Table className="min-w-full">
          <TableHeader>
            <TableRow>
              {columns.map((column) => (
                <TableHead key={column} className="whitespace-nowrap px-3 py-2">
                    <TooltipProvider delayDuration={100}>
                        <Tooltip>
                            <TooltipTrigger className="cursor-help">{column}</TooltipTrigger>
                            <TooltipContent>
                            <p>{column}</p>
                            </TooltipContent>
                        </Tooltip>
                    </TooltipProvider>
                </TableHead>
              ))}
            </TableRow>
            {showFilters && (
              <TableRow className="bg-muted/50 hover:bg-muted/50">
                {columns.map((column) => (
                  <TableHead key={`filter-${column}`} className="p-1 align-top">
                    <Input
                      placeholder={`Filter...`}
                      value={filters[column] || ""}
                      onChange={(e) => onFilterChange(column, e.target.value)}
                      className="h-8 text-xs border-none focus-visible:ring-1 focus-visible:ring-ring px-2 bg-transparent"
                    />
                  </TableHead>
                ))}
              </TableRow>
            )}
          </TableHeader>
          <TableBody>
            {data.length > 0 ? (
              data.map((row, rowIndex) => (
                <TableRow key={rowIndex} onClick={() => onRowClick(row)} className="cursor-pointer">
                  {columns.map((column) => (
                    <TableCell key={`${rowIndex}-${column}`} className="whitespace-nowrap px-3 py-1.5 text-sm">
                      <span title={String(row[column] ?? "")}>
                        {String(row[column] ?? "").length > 50
                          ? String(row[column]).substring(0, 50) + "..."
                          : String(row[column] ?? "")}
                      </span>
                    </TableCell>
                  ))}
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={columns.length} className="h-24 text-center text-muted-foreground">
                  No results found.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}

interface DataVisualizerProps {
  data: any[];
  columns: string[];
}

function DataVisualizerComponent({ data, columns }: DataVisualizerProps) {
  const [chartType, setChartType] = useState("boxplot"); // Default to boxplot
  const [yAxis, setYAxis] = useState(""); // Outcome / Numerical
  const [xAxis, setXAxis] = useState(""); // Primary Grouping / Categorical or Numerical for Scatter
  const [groupBy, setGroupBy] = useState("none"); // Secondary Grouping / Color
  const [numBins, setNumBins] = useState(10); // For histograms
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const chartInstanceRef = useRef<Chart | null>(null);

  const { numericalColumns, categoricalColumns } = useMemo(() => {
    const numerical: string[] = [];
    const categorical: string[] = [];

    columns.forEach(column => {
        if (!column) return;
        const values = data.map(row => row[column]).filter(v => v !== undefined && v !== null && v !== '');
        if (values.length === 0) return;
        const numericCount = values.reduce((count, val) => {
            const isPotentiallyNumeric = val === '' || !isNaN(Number(val));
            return count + (isPotentiallyNumeric && String(val).trim() !== '' && !isNaN(Number(val)) ? 1 : 0);
        }, 0);
        const uniqueValues = new Set(values);
        // More strict definition for numerical Y-axis
        if (numericCount / values.length > 0.9 && uniqueValues.size > 5) {
            numerical.push(column);
        // Relaxed definition for categorical X-axis / Grouping
        } else if (uniqueValues.size <= 50 && uniqueValues.size >= 1) {
             categorical.push(column);
        } else if (numericCount / values.length > 0.1) { // Also consider numeric-like as potential categorical bins or scatter X
             categorical.push(column); // Allow numeric for X in scatter, or binning in histogram
        }
    });
    return { numericalColumns: numerical.sort(), categoricalColumns: categorical.sort() };
  }, [data, columns]);

  useEffect(() => {
     if (!yAxis && numericalColumns.length > 0) {
         const defaultY = ["testscore", "index_confidence", "index_motivation", "index_complement", "index_cheating", "ConversationDurationMinutes", "MessageCount", "age", "gpa"].find(c => numericalColumns.includes(c)) || numericalColumns[0];
         setYAxis(defaultY);
      } else if (!yAxis && columns.length > 0) {
         setYAxis(columns[0]); // Fallback
      }

      if (!xAxis && categoricalColumns.length > 0) {
        const defaultX = ["treatment_clean", "gender", "highgpa"].find(c => categoricalColumns.includes(c)) || categoricalColumns.find(c => c !== yAxis) || categoricalColumns[0];
        setXAxis(defaultX);
      } else if (!xAxis && columns.length > 1) {
          setXAxis(columns.find(c => c !== yAxis) || columns[1]); // Fallback
      }
  }, [columns, numericalColumns, categoricalColumns, xAxis, yAxis]);

  useEffect(() => {
    if (!canvasRef.current || !yAxis || !xAxis || data.length === 0 || !chartType || !Chart) return;
    const ctx = canvasRef.current.getContext("2d");
    if (!ctx) return;
    if (chartInstanceRef.current) chartInstanceRef.current.destroy();

    let chartData: any = { labels: [], datasets: [] };
    let options: any = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false, position: 'top' },
            title: { display: true, text: `${yAxis} by ${xAxis}${groupBy && groupBy !== 'none' ? ` (Grouped by ${groupBy})` : ''}` },
            tooltip: { /* Default tooltips */ }
        },
        scales: { x: { title: { display: true, text: xAxis } }, y: { beginAtZero: true, title: { display: true, text: yAxis } } }
    };
    let type: Chart.ChartType = 'bar'; // Default type

    const colors = ['#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899', '#06b6d4', '#f97316'];
    const getGroupedData = () => {
        const groups: Record<string, Record<string, number[]>> = {};
        const xValues = new Set<string>();
        const groupValues = new Set<string>();

        data.forEach(row => {
            const xVal = String(row[xAxis] ?? 'N/A');
            const groupVal = groupBy && groupBy !== 'none' ? String(row[groupBy] ?? 'N/A') : '_main_';
            const yVal = Number(row[yAxis]);

            if (isNaN(yVal)) return;

            xValues.add(xVal);
            groupValues.add(groupVal);

            if (!groups[groupVal]) groups[groupVal] = {};
            if (!groups[groupVal][xVal]) groups[groupVal][xVal] = [];
            groups[groupVal][xVal].push(yVal);
        });
        const sortedXValues = [...xValues].sort((a, b) => a.localeCompare(b, undefined, {numeric: true, sensitivity: 'base'}));
        const sortedGroupValues = [...groupValues].sort((a, b) => a.localeCompare(b, undefined, {numeric: true, sensitivity: 'base'}));
        return { groups, sortedXValues, sortedGroupValues };
    };

    const { groups, sortedXValues, sortedGroupValues } = getGroupedData();
    chartData.labels = sortedXValues;

    if (chartType === 'boxplot') {
        type = 'boxplot' as Chart.ChartType;
        chartData.datasets = sortedGroupValues.map((groupVal, index) => ({
            label: groupVal === '_main_' ? yAxis : groupVal,
            data: sortedXValues.map(xVal => calculateBoxPlotStats(groups[groupVal]?.[xVal] || [])),
            backgroundColor: colors[index % colors.length] + '80', // Semi-transparent fill
            borderColor: colors[index % colors.length],
            borderWidth: 1,
            itemRadius: 3, // Optionally show mean point
        }));
         options.plugins.legend.display = groupBy && groupBy !== 'none' && sortedGroupValues.length > 1;
         options.plugins.tooltip = { // Customize tooltips for boxplot
             callbacks: {
                 label: (context: any) => {
                     const stats = context.raw;
                     if (!stats) return '';
                     return [
                         `Median: ${formatNumber(stats.median)}`,
                         `Q1: ${formatNumber(stats.q1)}`,
                         `Q3: ${formatNumber(stats.q3)}`,
                         `Mean: ${formatNumber(stats.mean)}`,
                         `N: ${stats.count}`
                     ];
                 }
             }
         };

    } else if (chartType === 'histogram') {
        type = 'bar';
        const yValues = data.map(row => Number(row[yAxis])).filter(v => !isNaN(v));
        if (yValues.length > 0) {
             const minVal = Math.min(...yValues);
             const maxVal = Math.max(...yValues);
             const binWidth = (maxVal - minVal) / numBins;
             const bins: number[] = Array(numBins).fill(0);
             const binLabels: string[] = [];

             yValues.forEach(val => {
                let binIndex = Math.floor((val - minVal) / binWidth);
                if (binIndex >= numBins) binIndex = numBins - 1; // Put max value in last bin
                if (binIndex < 0) binIndex = 0; // Handle potential floating point issues
                bins[binIndex]++;
             });

             for(let i=0; i<numBins; i++){
                 const binStart = minVal + i * binWidth;
                 const binEnd = binStart + binWidth;
                 binLabels.push(`${formatNumber(binStart)}-${formatNumber(binEnd)}`);
             }
             chartData.labels = binLabels;
             chartData.datasets = [{
                 label: yAxis,
                 data: bins,
                 backgroundColor: colors[0] + 'BF',
                 borderColor: colors[0],
                 borderWidth: 1,
             }];
             options.scales.x.title.text = yAxis; // X-axis shows bins of Y
             options.scales.y.title.text = 'Frequency';
             options.plugins.title.text = `${yAxis} Distribution (Histogram)`;
             options.plugins.legend.display = false;
        }

    } else if (chartType === 'scatter') {
        type = 'scatter';
        options.scales.y.beginAtZero = undefined; // Don't force zero for scatter
        chartData.datasets = sortedGroupValues.map((groupVal, index) => ({
            label: groupVal === '_main_' ? yAxis : groupVal,
            data: data
                .filter(row => (groupBy && groupBy !== 'none' ? String(row[groupBy] ?? 'N/A') : '_main_') === groupVal)
                .map(row => ({ x: Number(row[xAxis]), y: Number(row[yAxis]) }))
                .filter(p => !isNaN(p.x) && !isNaN(p.y)), // Ensure both are numbers
            backgroundColor: colors[index % colors.length], // Points solid
            borderColor: colors[index % colors.length],
        }));
        options.plugins.legend.display = groupBy && groupBy !== 'none' && sortedGroupValues.length > 1;
        options.plugins.title.text = `${yAxis} vs ${xAxis}${groupBy && groupBy !== 'none' ? ` (Colored by ${groupBy})` : ''}`;

    } else { // Default to Bar chart showing averages
        type = 'bar';
        chartData.datasets = sortedGroupValues.map((groupVal, index) => ({
            label: groupVal === '_main_' ? `Avg ${yAxis}` : groupVal,
            data: sortedXValues.map(xVal => {
                 const values = groups[groupVal]?.[xVal] || [];
                 return values.length > 0 ? values.reduce((a, b) => a + b, 0) / values.length : 0;
            }),
            backgroundColor: colors[index % colors.length] + 'BF',
            borderColor: colors[index % colors.length],
            borderWidth: 1,
        }));
        options.plugins.legend.display = groupBy && groupBy !== 'none' && sortedGroupValues.length > 1;
        options.plugins.title.text = `Avg ${yAxis} by ${xAxis}${groupBy && groupBy !== 'none' ? ` (Grouped by ${groupBy})` : ''}`;
    }


    chartInstanceRef.current = new Chart(ctx, { type, data: chartData, options });

    return () => { if (chartInstanceRef.current) chartInstanceRef.current.destroy(); chartInstanceRef.current = null; };
  }, [data, yAxis, xAxis, groupBy, chartType, numBins, numericalColumns, categoricalColumns]);


  const downloadChart = () => {
     if (!canvasRef.current) return;
    const link = document.createElement("a");
    link.download = `chart-${chartType}-${yAxis}-by-${xAxis}${groupBy && groupBy !== 'none' ? `-grouped-${groupBy}` : ''}.png`;
    link.href = canvasRef.current.toDataURL("image/png", 1.0);
    link.click();
  };

  // Helper to format numbers, used in tooltips and potentially axes
  const formatNumber = (num: number | string) => {
        if (typeof num === 'number' && !isNaN(num)) {
            if (Math.abs(num) < 1e9 && Math.floor(num) === num) return num.toLocaleString();
            return num.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        }
        return num;
    };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">Data Visualization</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 mb-4 items-end">
          <div>
            <label className="block text-xs font-medium mb-1 text-muted-foreground">Chart Type</label>
            <Select value={chartType} onValueChange={setChartType}>
              <SelectTrigger className="h-9"> <SelectValue placeholder="Chart Type" /> </SelectTrigger>
              <SelectContent>
                <SelectItem value="boxplot"><div className="flex items-center gap-2"><Box className="h-4 w-4"/>Box Plot</div></SelectItem>
                <SelectItem value="bar"><div className="flex items-center gap-2"><BarChart className="h-4 w-4"/>Bar (Avg)</div></SelectItem>
                <SelectItem value="histogram"><div className="flex items-center gap-2"><BarChart className="h-4 w-4"/>Histogram</div></SelectItem>
                <SelectItem value="scatter"><div className="flex items-center gap-2"><TrendingUp className="h-4 w-4"/>Scatter</div></SelectItem>
              </SelectContent>
            </Select>
          </div>
           <div>
            <label className="block text-xs font-medium mb-1 text-muted-foreground">Y-Axis (Value)</label>
            <Select value={yAxis} onValueChange={setYAxis} disabled={chartType === 'histogram'}>
              <SelectTrigger className="h-9"> <SelectValue placeholder="Select Y-Axis" /> </SelectTrigger>
              <SelectContent>
                {numericalColumns.map((column) => <SelectItem key={`y-${column}`} value={column}>{column}</SelectItem>)}
              </SelectContent>
            </Select>
            {chartType === 'histogram' && <Input value={yAxis} readOnly className="h-9 mt-1 bg-muted text-muted-foreground" />}
          </div>
          <div>
            <label className="block text-xs font-medium mb-1 text-muted-foreground">X-Axis ({chartType === 'scatter' ? 'Value' : 'Category'})</label>
            <Select value={xAxis} onValueChange={setXAxis} disabled={chartType === 'histogram'}>
              <SelectTrigger className="h-9"> <SelectValue placeholder="Select X-Axis" /> </SelectTrigger>
              <SelectContent>
                {(chartType === 'scatter' ? [...categoricalColumns, ...numericalColumns] : categoricalColumns)
                  .filter((c, i, a) => a.indexOf(c) === i)
                  .sort()
                  .map((column) => <SelectItem key={`x-${column}`} value={column}>{column}</SelectItem>)}
              </SelectContent>
            </Select>
             {chartType === 'histogram' && <Input value="# Bins" readOnly className="h-9 mt-1 bg-muted text-muted-foreground"/>}
          </div>
           <div>
            <label className="block text-xs font-medium mb-1 text-muted-foreground">{chartType === 'histogram' ? 'Number of Bins' : 'Group/Color By'}</label>
             {chartType === 'histogram' ? (
                 <Select value={numBins.toString()} onValueChange={(val) => setNumBins(Number(val))}>
                     <SelectTrigger className="h-9"><SelectValue /></SelectTrigger>
                     <SelectContent>
                         {[5, 10, 15, 20, 25, 30].map(n => <SelectItem key={`bins-${n}`} value={n.toString()}>{n} Bins</SelectItem>)}
                     </SelectContent>
                 </Select>
             ) : (
                <Select value={groupBy} onValueChange={setGroupBy}>
                    <SelectTrigger className="h-9"> <SelectValue placeholder="Group By (Optional)" /> </SelectTrigger>
                    <SelectContent>
                        <SelectItem value="none">No Grouping</SelectItem>
                        {categoricalColumns.filter(col => col !== xAxis).map((column) => <SelectItem key={`group-${column}`} value={column}>{column}</SelectItem>)}
                    </SelectContent>
                </Select>
            )}
          </div>
        </div>

        <div className="flex justify-end mb-2">
          <Button variant="outline" size="sm" onClick={downloadChart} className="flex items-center gap-2 h-9">
            <Download className="h-4 w-4" /> Download Chart
          </Button>
        </div>

        <div className="border rounded-lg p-2 sm:p-4 bg-background aspect-video relative min-h-[350px]">
          <canvas ref={canvasRef}></canvas>
        </div>
      </CardContent>
    </Card>
  );
}


interface DataSummaryProps {
  data: any[];
  columns: string[];
}

function DataSummaryComponent({ data, columns }: DataSummaryProps) {
    const [selectedDistColumn, setSelectedDistColumn] = useState("");
    const [showAllMissing, setShowAllMissing] = useState(false);
    const [groupSummaryBy, setGroupSummaryBy] = useState<string[]>(['treatment_clean']); // Default grouping
    const [groupSummaryVar, setGroupSummaryVar] = useState('testscore'); // Default variable

    // Find categorical columns suitable for grouping
    const potentialGroupingColumns = useMemo(() => {
         return columns.filter(col => {
             if(!col) return false;
             const uniqueValues = new Set(data.map(row => row[col]));
             return uniqueValues.size > 1 && uniqueValues.size < 15; // Keep it manageable
         }).sort();
    }, [data, columns]);

     // Find numerical columns suitable for summary
    const potentialSummaryVariables = useMemo(() => {
         return columns.filter(col => {
             if (!col) return false;
             const values = data.map(row => row[col]).filter(v => v !== undefined && v !== null && v !== '');
             if (values.length === 0) return false;
             const numericCount = values.reduce((count, val) => count + (val === '' || !isNaN(Number(val)) ? 1 : 0), 0);
             return numericCount / values.length > 0.8; // Mostly numeric
         }).sort();
    }, [data, columns]);


    useEffect(() => {
      if (!selectedDistColumn && potentialGroupingColumns.length > 0) {
        const defaultDist = ["treatment_clean", "gender", "highgpa"].find(c => potentialGroupingColumns.includes(c)) || potentialGroupingColumns[0];
        setSelectedDistColumn(defaultDist);
      }
      if (!groupSummaryVar && potentialSummaryVariables.length > 0){
          const defaultVar = ["testscore", "index_confidence", "index_motivation"].find(c => potentialSummaryVariables.includes(c)) || potentialSummaryVariables[0];
          setGroupSummaryVar(defaultVar);
      }
       if (groupSummaryBy.length === 0 && potentialGroupingColumns.length > 0){
          const defaultGroup = ["treatment_clean"].find(c => potentialGroupingColumns.includes(c)) || potentialGroupingColumns[0];
          setGroupSummaryBy([defaultGroup]);
      }
    }, [columns, selectedDistColumn, potentialGroupingColumns, groupSummaryVar, potentialSummaryVariables, groupSummaryBy]);

    const { summaryStats, missingStats } = useMemo(() => {
        // ... (calculation logic remains the same) ...
        const summary: any[] = [];
        const missing: any[] = [];
        columns.forEach(column => {
            if (!column) return;
            const values = data.map(row => row[column]);
            const validValues = values.filter(val => val !== undefined && val !== null && val !== '');
            const missingCount = values.length - validValues.length;
            const missingPercentage = data.length > 0 ? ((missingCount / data.length) * 100) : 0;
            missing.push({ column, missingCount, missingPercentage });
            const numericValues = validValues.map(val => Number(val)).filter(val => !isNaN(val));
            const isLikelyNumeric = validValues.length > 0 && (numericValues.length / validValues.length > 0.8) && new Set(numericValues).size > 5;
            const stats: any = { column, count: validValues.length, uniqueCount: new Set(validValues).size, missingCount, missingPercentage, isNumeric: isLikelyNumeric, min: '-', max: '-', mean: '-', median: '-', stdDev: '-' };
            if (isLikelyNumeric && numericValues.length > 0) {
                stats.min = Math.min(...numericValues);
                stats.max = Math.max(...numericValues);
                const sum = numericValues.reduce((s, v) => s + v, 0);
                stats.mean = sum / numericValues.length;
                stats.median = calculateMedian(numericValues);
                stats.stdDev = calculateStdDev(numericValues, stats.mean);
            }
            summary.push(stats);
        });
        missing.sort((a, b) => b.missingPercentage - a.missingPercentage);
        return { summaryStats: summary, missingStats: missing };
    }, [data, columns]);

    const frequencyDistribution = useMemo(() => {
        // ... (calculation logic remains the same) ...
        if (!selectedDistColumn || data.length === 0) return [];
        const values = data.map(row => row[selectedDistColumn]).filter(val => val !== undefined && val !== null && val !== '');
        if (values.length === 0) return [];
        const valueCounts: Record<string, number> = {};
        values.forEach(val => { const key = String(val); valueCounts[key] = (valueCounts[key] || 0) + 1; });
        return Object.entries(valueCounts)
            .sort((a, b) => b[1] - a[1])
            .map(([value, count]) => ({ value, count, percentage: ((count / values.length) * 100) }));
    }, [data, selectedDistColumn]);

    // NEW: Grouped Summary Statistics Logic
    const groupedSummaryData = useMemo(() => {
        if (!groupSummaryVar || groupSummaryBy.length === 0 || data.length === 0) return [];

        const groupMap = new Map<string, number[]>();

        data.forEach(row => {
            const yVal = Number(row[groupSummaryVar]);
            if (isNaN(yVal)) return;

            const groupKey = groupSummaryBy.map(key => String(row[key] ?? 'N/A')).join(' | '); // Combine group values

            if (!groupMap.has(groupKey)) {
                groupMap.set(groupKey, []);
            }
            groupMap.get(groupKey)!.push(yVal);
        });

        const results: any[] = [];
        groupMap.forEach((values, key) => {
            const keys = key.split(' | ');
            const stats = calculateBoxPlotStats(values); // Reuse boxplot calc for mean, stdDev, N
             if(stats){
                 const rowData: Record<string, any> = {};
                 groupSummaryBy.forEach((colName, index) => {
                     rowData[colName] = keys[index];
                 });
                 rowData.Count = stats.count;
                 rowData.Mean = stats.mean;
                 rowData.StdDev = stats.stdDev;
                 rowData.Median = stats.median;
                 results.push(rowData);
             }
        });

        // Sort results for consistency
        results.sort((a, b) => {
            for (let i = 0; i < groupSummaryBy.length; i++) {
                const key = groupSummaryBy[i];
                const compare = String(a[key]).localeCompare(String(b[key]), undefined, { numeric: true, sensitivity: 'base' });
                if (compare !== 0) return compare;
            }
            return 0;
        });

        return results;

    }, [data, groupSummaryVar, groupSummaryBy]);

    const calculateMedian = (values: number[]) => { if (values.length === 0) return 0; const sorted = [...values].sort((a, b) => a - b); const middle = Math.floor(sorted.length / 2); return sorted.length % 2 === 0 ? (sorted[middle - 1] + sorted[middle]) / 2 : sorted[middle]; };
    const calculateStdDev = (values: number[], mean: number) => { if (values.length <= 1) return 0; const variance = values.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / (values.length - 1); return Math.sqrt(variance); };
    const formatNumber = (num: number | string) => { if (typeof num === 'number' && !isNaN(num)) { if (Math.abs(num) < 1e9 && Math.floor(num) === num) return num.toLocaleString(); return num.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }); } return num; };
    const formatPercentage = (num: number) => { if (typeof num === 'number' && !isNaN(num)) { return num.toFixed(1) + '%'; } return '-'; };

    const displayedMissingStats = showAllMissing ? missingStats : missingStats.slice(0, 10);

    return (
        <div className="space-y-4">
            <Card>
                <CardHeader> <CardTitle className="text-lg">Column Summaries</CardTitle> </CardHeader>
                <CardContent>
                    <div className="overflow-x-auto max-h-[400px] border rounded-md">
                        <Table className="min-w-full">
                             <TableHeader className="sticky top-0 bg-background z-10">
                                <TableRow>
                                    <TableHead className="w-[150px]">Column</TableHead>
                                    <TableHead>Type</TableHead>
                                    <TableHead>Count</TableHead>
                                    <TableHead>Unique</TableHead>
                                    <TableHead>Missing</TableHead>
                                    <TableHead>Min</TableHead>
                                    <TableHead>Max</TableHead>
                                    <TableHead>Mean</TableHead>
                                    <TableHead>Median</TableHead>
                                    <TableHead>Std Dev</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {summaryStats.map((stats) => (
                                    <TableRow key={stats.column}>
                                        <TableCell className="font-medium max-w-[150px] truncate" title={stats.column}>{stats.column}</TableCell>
                                        <TableCell>{stats.isNumeric ? "Numeric" : "Category"}</TableCell>
                                        <TableCell>{formatNumber(stats.count)}</TableCell>
                                        <TableCell>{formatNumber(stats.uniqueCount)}</TableCell>
                                        <TableCell>{formatPercentage(stats.missingPercentage)}</TableCell>
                                        <TableCell>{formatNumber(stats.min)}</TableCell>
                                        <TableCell>{formatNumber(stats.max)}</TableCell>
                                        <TableCell>{formatNumber(stats.mean)}</TableCell>
                                        <TableCell>{formatNumber(stats.median)}</TableCell>
                                        <TableCell>{formatNumber(stats.stdDev)}</TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </div>
                </CardContent>
            </Card>

             {/* NEW: Grouped Summary Card */}
            <Card>
                 <CardHeader>
                    <CardTitle className="text-lg">Grouped Summaries</CardTitle>
                 </CardHeader>
                 <CardContent>
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-4 items-end">
                         <div>
                            <label className="block text-xs font-medium mb-1 text-muted-foreground">Variable</label>
                             <Select value={groupSummaryVar} onValueChange={setGroupSummaryVar}>
                                 <SelectTrigger className="h-9"><SelectValue placeholder="Select Variable" /></SelectTrigger>
                                 <SelectContent>
                                     {potentialSummaryVariables.map(col => <SelectItem key={`sumvar-${col}`} value={col}>{col}</SelectItem>)}
                                 </SelectContent>
                             </Select>
                         </div>
                         <div className="sm:col-span-2">
                             <label className="block text-xs font-medium mb-1 text-muted-foreground">Group By (Ctrl+Click for multiple)</label>
                              {/* Using a simple multi-select display for now */}
                             <DropdownMenu>
                                <DropdownMenuTrigger asChild>
                                    <Button variant="outline" className="h-9 w-full justify-start text-left font-normal">
                                        {groupSummaryBy.length === 0 ? "Select Groups..." : groupSummaryBy.join(', ')}
                                    </Button>
                                </DropdownMenuTrigger>
                                <DropdownMenuContent className="w-[--radix-dropdown-menu-trigger-width]">
                                    <DropdownMenuLabel>Group By</DropdownMenuLabel>
                                    <DropdownMenuSeparator />
                                    {potentialGroupingColumns.map(col => (
                                        <DropdownMenuCheckboxItem
                                            key={`groupcol-${col}`}
                                            checked={groupSummaryBy.includes(col)}
                                            onCheckedChange={(checked) => {
                                                setGroupSummaryBy(prev => checked ? [...prev, col] : prev.filter(c => c !== col));
                                            }}
                                             onSelect={(e) => e.preventDefault()}
                                        >
                                            {col}
                                        </DropdownMenuCheckboxItem>
                                    ))}
                                </DropdownMenuContent>
                             </DropdownMenu>
                         </div>
                    </div>
                     <div className="overflow-x-auto max-h-[400px] border rounded-md">
                        <Table className="min-w-full">
                             <TableHeader className="sticky top-0 bg-background z-10">
                                <TableRow>
                                    {groupSummaryBy.map(col => <TableHead key={`h-${col}`}>{col}</TableHead>)}
                                    <TableHead>Count</TableHead>
                                    <TableHead>Mean</TableHead>
                                    <TableHead>Median</TableHead>
                                    <TableHead>Std Dev</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {groupedSummaryData.length > 0 ? groupedSummaryData.map((row, index) => (
                                    <TableRow key={index}>
                                        {groupSummaryBy.map(col => <TableCell key={`cell-${index}-${col}`}>{row[col]}</TableCell>)}
                                        <TableCell>{formatNumber(row.Count)}</TableCell>
                                        <TableCell>{formatNumber(row.Mean)}</TableCell>
                                        <TableCell>{formatNumber(row.Median)}</TableCell>
                                        <TableCell>{formatNumber(row.StdDev)}</TableCell>
                                    </TableRow>
                                )) : (
                                     <TableRow>
                                        <TableCell colSpan={groupSummaryBy.length + 4} className="text-center text-muted-foreground h-24">
                                            Select a variable and grouping columns.
                                        </TableCell>
                                     </TableRow>
                                )}
                            </TableBody>
                        </Table>
                    </div>
                 </CardContent>
            </Card>


            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Card>
                    <CardHeader> <CardTitle className="text-lg">Frequency Distribution</CardTitle> </CardHeader>
                    <CardContent>
                        <div className="mb-3">
                            <Select value={selectedDistColumn} onValueChange={setSelectedDistColumn}>
                                <SelectTrigger className="h-9"><SelectValue placeholder="Select Column" /></SelectTrigger>
                                <SelectContent>
                                    {potentialGroupingColumns.map((column) => <SelectItem key={`dist-${column}`} value={column}>{column}</SelectItem>)}
                                </SelectContent>
                            </Select>
                        </div>
                        <div className="overflow-y-auto max-h-[300px] border rounded-md">
                            <Table>
                                <TableHeader className="sticky top-0 bg-background z-10">
                                    <TableRow> <TableHead>Value</TableHead> <TableHead>Count</TableHead> <TableHead>%</TableHead> </TableRow>
                                </TableHeader>
                                <TableBody>
                                    {frequencyDistribution.length > 0 ? frequencyDistribution.map((item, index) => (
                                        <TableRow key={index}>
                                            <TableCell className="max-w-[150px] truncate" title={item.value}>{item.value}</TableCell>
                                            <TableCell>{formatNumber(item.count)}</TableCell>
                                            <TableCell>{formatPercentage(item.percentage)}</TableCell>
                                        </TableRow>
                                    )) : ( <TableRow><TableCell colSpan={3} className="text-center text-muted-foreground h-24">No data.</TableCell></TableRow> )}
                                </TableBody>
                            </Table>
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle className="text-lg">Missing Values</CardTitle>
                         <p className="text-sm text-muted-foreground">Top columns sorted by missing %.</p>
                    </CardHeader>
                    <CardContent>
                        <div className="overflow-y-auto max-h-[340px] border rounded-md">
                             <Table>
                                <TableHeader className="sticky top-0 bg-background z-10">
                                    <TableRow> <TableHead>Column</TableHead> <TableHead>Missing #</TableHead> <TableHead>Missing %</TableHead> </TableRow>
                                </TableHeader>
                                <TableBody>
                                    {displayedMissingStats.filter(s => s.missingCount > 0).length > 0 ? displayedMissingStats.filter(s => s.missingCount > 0).map((stats) => (
                                        <TableRow key={`missing-${stats.column}`}>
                                            <TableCell className="max-w-[150px] truncate" title={stats.column}>{stats.column}</TableCell>
                                            <TableCell>{formatNumber(stats.missingCount)}</TableCell>
                                            <TableCell>{formatPercentage(stats.missingPercentage)}</TableCell>
                                        </TableRow>
                                    )) : ( <TableRow><TableCell colSpan={3} className="text-center text-muted-foreground h-24">No missing values.</TableCell></TableRow> )}
                                </TableBody>
                            </Table>
                        </div>
                        {missingStats.filter(s => s.missingCount > 0).length > 10 && (
                            <Button variant="link" size="sm" onClick={() => setShowAllMissing(!showAllMissing)} className="mt-2 p-0 h-auto">
                                {showAllMissing ? "Show Top 10 Missing" : `Show All (${missingStats.filter(s => s.missingCount > 0).length}) Missing`}
                            </Button>
                        )}
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}


type DataRow = Record<string, any>;

interface DataExplorerProps {
  initialData: DataRow[];
  initialColumns: string[];
}

function DataExplorer({ initialData, initialColumns }: DataExplorerProps) {
  const rawData = useMemo(() => initialData, [initialData]);
  const allColumns = useMemo(() => initialColumns, [initialColumns]);

  const [loading, setLoading] = useState(!initialData || initialData.length === 0);
  const [searchTerm, setSearchTerm] = useState("");
  const [filters, setFilters] = useState<Record<string, string>>({});
  const [selectedColumns, setSelectedColumns] = useState<string[]>(() => {
      const defaultCols = ["final_id", "treatment_clean", "gender", "highgpa", "testscore", "index_complement", "index_confidence", "index_cheating", "index_motivation", "MessageCount", "ConversationDurationMinutes"];
      const validDefaultCols = defaultCols.filter(col => allColumns.includes(col));
      return validDefaultCols.length > 0 ? validDefaultCols : allColumns.slice(0, 10);
  });
  const [pagination, setPagination] = useState({ currentPage: 1, itemsPerPage: 25 });
  const [activeTab, setActiveTab] = useState("table");
  const [selectedRowData, setSelectedRowData] = useState<DataRow | null>(null); // For modal

  useEffect(() => {
    if (initialData && initialData.length > 0) {
        setLoading(false);
        setSelectedColumns(prev => {
             const validCols = prev.filter(col => initialColumns.includes(col));
             if (validCols.length === 0 && initialColumns.length > 0) {
                 const defaultCols = ["final_id", "treatment_clean", "gender", "highgpa", "testscore", "index_complement", "index_confidence", "index_cheating", "index_motivation", "MessageCount", "ConversationDurationMinutes"];
                 const validDefaultCols = defaultCols.filter(col => initialColumns.includes(col));
                 return validDefaultCols.length > 0 ? validDefaultCols : initialColumns.slice(0, 10);
             }
             return validCols;
        })
    }
  }, [initialData, initialColumns]);


  const filteredData = useMemo(() => {
    let filtered = rawData;
    if (searchTerm) {
      const lowerSearchTerm = searchTerm.toLowerCase();
      filtered = filtered.filter(row => allColumns.some(col => row[col] !== null && row[col] !== undefined && String(row[col]).toLowerCase().includes(lowerSearchTerm)));
    }
    const activeFilters = Object.entries(filters).filter(([_, value]) => value);
    if (activeFilters.length > 0) {
      filtered = filtered.filter(row => activeFilters.every(([column, filterValue]) => { const lowerFilterValue = filterValue.toLowerCase(); return ( row[column] !== null && row[column] !== undefined && String(row[column]).toLowerCase().includes(lowerFilterValue) ); }));
    }
    return filtered;
  }, [rawData, searchTerm, filters, allColumns]);

  const paginatedData = useMemo(() => {
    const startIndex = (pagination.currentPage - 1) * pagination.itemsPerPage;
    return filteredData.slice(startIndex, startIndex + pagination.itemsPerPage);
  }, [filteredData, pagination.currentPage, pagination.itemsPerPage]);

  const totalPages = Math.ceil(filteredData.length / pagination.itemsPerPage);

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => { setSearchTerm(e.target.value); setPagination(p => ({ ...p, currentPage: 1 })); };
  const handleFilterChange = (column: string, value: string) => { setFilters(prev => ({ ...prev, [column]: value })); setPagination(p => ({ ...p, currentPage: 1 })); };
  const handleColumnToggle = (column: string) => { setSelectedColumns(prev => prev.includes(column) ? prev.filter(col => col !== column) : [...prev, column]); };
  const handlePageChange = (page: number) => { if (page >= 1 && page <= totalPages) { setPagination(p => ({ ...p, currentPage: page })); } };
  const handleItemsPerPageChange = (value: string) => { setPagination({ currentPage: 1, itemsPerPage: Number.parseInt(value) }); };
  const handleRowClick = (row: DataRow) => { setSelectedRowData(row); }; // Set data for modal

  const exportCSV = () => {
    const dataToExport = filteredData.map(row => { const newRow: Record<string, any> = {}; selectedColumns.forEach(col => { newRow[col] = row[col] ?? ""; }); return newRow; });
    if (dataToExport.length === 0) { alert("No data to export."); return; }
    const csvString = Papa.unparse(dataToExport, { columns: selectedColumns, header: true, quotes: true, quoteChar: '"', escapeChar: '"', delimiter: ",", newline: "\r\n" });
    const blob = new Blob([`\uFEFF${csvString}`], { type: "text/csv;charset=utf-8;" }); // Add BOM for Excel
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", "conversation_data_export.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

   const renderPaginationItems = () => {
            const items = []; const maxPagesToShow = 5; const halfMaxPages = Math.floor(maxPagesToShow / 2); let startPageNum = 1; let endPageNum = totalPages; if (totalPages > maxPagesToShow + 2) { if (pagination.currentPage <= halfMaxPages + 1) { endPageNum = maxPagesToShow + 1; } else if (pagination.currentPage >= totalPages - halfMaxPages) { startPageNum = totalPages - maxPagesToShow; } else { startPageNum = pagination.currentPage - halfMaxPages; endPageNum = pagination.currentPage + halfMaxPages; } } if (startPageNum > 1) { items.push( <PaginationItem key={1}> <PaginationLink onClick={() => handlePageChange(1)} className="cursor-pointer">1</PaginationLink> </PaginationItem> ); if (startPageNum > 2) { items.push(<PaginationItem key="start-ellipsis"><PaginationEllipsis /></PaginationItem>); } } for (let i = startPageNum; i <= endPageNum; i++) { items.push( <PaginationItem key={i}> <PaginationLink isActive={pagination.currentPage === i} onClick={() => handlePageChange(i)} className="cursor-pointer"> {i} </PaginationLink> </PaginationItem> ); } if (endPageNum < totalPages) { if (endPageNum < totalPages - 1) { items.push(<PaginationItem key="end-ellipsis"><PaginationEllipsis /></PaginationItem>); } items.push( <PaginationItem key={totalPages}> <PaginationLink onClick={() => handlePageChange(totalPages)} className="cursor-pointer">{totalPages}</PaginationLink> </PaginationItem> ); } return items;
    };

  if (loading) { return ( <div className="flex items-center justify-center h-screen"> <Loader2 className="h-8 w-8 animate-spin text-primary mr-2" /> <span>Loading data...</span> </div> ); }
  if (!initialData || initialData.length === 0) { return ( <div className="p-8 text-center text-destructive"> Failed to load or parse data. Please check the data source and format. </div> ); }

  return (
    <div className="p-4 md:p-6 space-y-4">
      <div className="flex flex-col md:flex-row gap-2 md:items-center">
        <div className="relative flex-1">
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input placeholder="Search data..." value={searchTerm} onChange={handleSearchChange} className="pl-8 h-9" />
        </div>
        <div className="flex gap-2 flex-shrink-0">
             <Select value={pagination.itemsPerPage.toString()} onValueChange={handleItemsPerPageChange}>
               <SelectTrigger className="w-[130px] h-9 text-xs"> <SelectValue placeholder="Rows per page" /> </SelectTrigger>
               <SelectContent> <SelectItem value="10">10 rows</SelectItem> <SelectItem value="25">25 rows</SelectItem> <SelectItem value="50">50 rows</SelectItem> <SelectItem value="100">100 rows</SelectItem> </SelectContent>
             </Select>
            <Button variant="outline" size="sm" onClick={exportCSV} className="h-9"> <Download className="h-4 w-4 mr-2" /> Export CSV </Button>
        </div>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="table" className="flex items-center gap-2"> <TableIcon className="h-4 w-4" /> Table </TabsTrigger>
          <TabsTrigger value="visualize" className="flex items-center gap-2"> <AreaChart className="h-4 w-4" /> Visualize </TabsTrigger>
          <TabsTrigger value="summary" className="flex items-center gap-2"> <BarChart className="h-4 w-4" /> Summary </TabsTrigger>
        </TabsList>

        <TabsContent value="table" className="mt-0">
          <Card>
            <CardContent className="p-0">
              <DataTableComponent
                data={paginatedData}
                columns={selectedColumns}
                allColumns={allColumns}
                filters={filters}
                onFilterChange={handleFilterChange}
                setFilters={setFilters}
                selectedColumns={selectedColumns}
                onColumnToggle={handleColumnToggle}
                onRowClick={handleRowClick} // Pass handler
              />
            </CardContent>
            {totalPages > 0 && (
                 <div className="flex items-center justify-between p-4 border-t">
                    <div className="text-xs text-muted-foreground"> Showing {filteredData.length > 0 ? (pagination.currentPage - 1) * pagination.itemsPerPage + 1 : 0} to {Math.min(pagination.currentPage * pagination.itemsPerPage, filteredData.length)} of {filteredData.length} results </div>
                    <Pagination> <PaginationContent> <PaginationItem> <PaginationPrevious onClick={() => handlePageChange(pagination.currentPage - 1)} className={pagination.currentPage === 1 ? "pointer-events-none opacity-50 cursor-not-allowed" : "cursor-pointer"} aria-disabled={pagination.currentPage === 1}/> </PaginationItem> {renderPaginationItems()} <PaginationItem> <PaginationNext onClick={() => handlePageChange(pagination.currentPage + 1)} className={pagination.currentPage === totalPages ? "pointer-events-none opacity-50 cursor-not-allowed" : "cursor-pointer"} aria-disabled={pagination.currentPage === totalPages}/> </PaginationItem> </PaginationContent> </Pagination>
                </div>
            )}
          </Card>
        </TabsContent>

        <TabsContent value="visualize" className="mt-4">
          <DataVisualizerComponent data={filteredData} columns={allColumns} />
        </TabsContent>

        <TabsContent value="summary" className="mt-4">
           <DataSummaryComponent data={rawData} columns={allColumns} />
        </TabsContent>
      </Tabs>

       {/* Conversation Detail Modal */}
       <Dialog open={selectedRowData !== null} onOpenChange={(isOpen) => !isOpen && setSelectedRowData(null)}>
            <DialogContent className="max-w-3xl">
                 <DialogHeader>
                    <DialogTitle>Conversation Details</DialogTitle>
                    <DialogDescription>
                         Viewing conversation for ID: {selectedRowData?.final_id || selectedRowData?.ResponseId || 'N/A'}
                    </DialogDescription>
                 </DialogHeader>
                 <ScrollArea className="max-h-[60vh] p-1 pr-3">
                     <pre className="text-sm whitespace-pre-wrap break-words bg-muted p-3 rounded-md font-mono">
                         {selectedRowData?.conversation_messages || "No conversation data available for this row."}
                     </pre>
                 </ScrollArea>
                  <DialogClose asChild>
                    <Button type="button" variant="secondary"> Close </Button>
                 </DialogClose>
            </DialogContent>
       </Dialog>

    </div>
  );
}


const CSV_URL = '../aligned_unified_conversation_data.csv';

export default function Page() {
  return <ClientDataExplorer csvUrl={CSV_URL} />;
}

// Create a separate client component for data loading and display
function ClientDataExplorer({ csvUrl }: { csvUrl: string }) {
  const [data, setData] = useState<DataRow[]>([]);
  const [columns, setColumns] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  
  useEffect(() => {
    async function fetchData() {
      try {
        console.log(`Attempting to load data from: ${csvUrl}`);
        const response = await fetch(csvUrl, { cache: 'no-store' });
        if (!response.ok) throw new Error(`Failed to fetch CSV: ${response.status} ${response.statusText}`);
        const csvText = await response.text();
        
        Papa.parse<DataRow>(csvText, {
          header: true, 
          skipEmptyLines: 'greedy', 
          dynamicTyping: true, 
          transformHeader: header => header.trim(),
          complete: (results) => {
            if (results.errors.length > 0) { 
              console.error("CSV Parsing Errors:", results.errors);
              console.warn("CSV parsing encountered errors."); 
            }
            
            if (!results.meta.fields || results.meta.fields.length === 0) { 
              console.error("CSV Parsing Error: No headers."); 
              setError(true);
              setLoading(false);
              return;
            }
            
            console.log(`Successfully parsed ${results.data.length} rows.`);
            // Basic data cleaning/typing fix attempts
            const cleanedData = results.data.map(row => {
                const cleanedRow = { ...row };
                // Example: Ensure boolean-like columns are boolean
                for (const key in cleanedRow) {
                     if (typeof cleanedRow[key] === 'string') {
                         const lowerVal = cleanedRow[key].toLowerCase();
                         if (lowerVal === 'true') cleanedRow[key] = true;
                         else if (lowerVal === 'false') cleanedRow[key] = false;
                     }
                     // Ensure specific numerical columns that might be strings are numbers
                     const numericCols = ['testscore', 'MessageCount', 'UserMessageCount', 'AIMessageCount', 'AverageUserMessageLength', 'AverageAIMessageLength', 'ConversationDuration', 'MessageRatio', 'ConversationDurationMinutes'];
                     if(numericCols.includes(key) && typeof cleanedRow[key] === 'string' && !isNaN(Number(cleanedRow[key]))) {
                         cleanedRow[key] = Number(cleanedRow[key]);
                     }
                }
                // Clean treatment variable
                if (cleanedRow.treatment === 'Control') cleanedRow.treatment_clean = 'Control';
                else if (cleanedRow.treatment === 'AI-assisted') cleanedRow.treatment_clean = 'AI-assisted';
                else if (cleanedRow.treatment === 'AI-guided') cleanedRow.treatment_clean = 'AI-guided';
                else if (cleanedRow.control === 1) cleanedRow.treatment_clean = 'Control';
                else if (cleanedRow.ai_assist === 1) cleanedRow.treatment_clean = 'AI-assisted';
                else if (cleanedRow.ai_guided === 1) cleanedRow.treatment_clean = 'AI-guided';
                else cleanedRow.treatment_clean = 'Unknown'; // Fallback

                 // Ensure highgpa is 0 or 1
                cleanedRow.highgpa = cleanedRow.highgpa === 1 ? 1 : 0;

                return cleanedRow;
            });
            
            const finalColumns = results.meta.fields.includes('treatment_clean') ? results.meta.fields : [...results.meta.fields, 'treatment_clean'];
            
            setData(cleanedData);
            setColumns(finalColumns);
            setLoading(false);
          },
          error: (error) => { 
            console.error("CSV Parsing Fatal Error:", error); 
            setError(true);
            setLoading(false);
          }
        });
      } catch (err) {
        console.error("Error loading data:", err);
        setError(true);
        setLoading(false);
      }
    }
    
    fetchData();
  }, [csvUrl]);
  
  if (loading) {
    return <div className="flex items-center justify-center h-screen">
      <div className="animate-spin mr-2 h-8 w-8 border-t-2 border-b-2 border-primary rounded-full"></div>
      Loading data...
    </div>;
  }
  
  if (error || columns.length === 0) {
    return <div className="flex items-center justify-center h-screen text-destructive">
      Error: Could not load data headers.
    </div>;
  }
  
  return <DataExplorer initialData={data} initialColumns={columns} />;
}