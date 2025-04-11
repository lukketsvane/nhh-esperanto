"use client";

import Papa from 'papaparse';
import React, { useState, useMemo, useEffect, useRef } from 'react';
import type { ChartTypeRegistry } from 'chart.js';
import Chart from 'chart.js/auto';
import { BoxPlotController, BoxAndWiskers } from '@sgratzl/chartjs-chart-boxplot';

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
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
import { DataRow } from '@/lib/data-loader';

// Register Chart.js components (BoxPlot)
try {
  Chart.register(BoxPlotController, BoxAndWiskers);
} catch (error) {
  console.warn("Failed to register BoxPlot components:", error);
}

// --- Helper Function: calculateBoxPlotStats ---
interface BoxPlotStats {
  min: number;
  q1: number;
  median: number;
  q3: number;
  max: number;
  mean: number;
  count: number;
  stdDev: number;
}

function calculateBoxPlotStats(data: number[]): BoxPlotStats | null {
    if (!data || data.length === 0) return null;
    const sortedData = data.filter(d => typeof d === 'number' && !isNaN(d)).sort((a, b) => a - b);
    const n = sortedData.length;
    if (n === 0) return null;

    const q1Index = Math.floor(n / 4);
    const medianIndex = Math.floor(n / 2);
    const q3Index = Math.floor((3 * n) / 4);

    const q1 = n % 4 === 0 && q1Index > 0 ? (sortedData[q1Index - 1] + sortedData[q1Index]) / 2 : sortedData[q1Index];
    const median = n % 2 === 0 && medianIndex > 0 ? (sortedData[medianIndex - 1] + sortedData[medianIndex]) / 2 : sortedData[medianIndex];
    const q3 = n % 4 === 0 && q3Index > 0 ? (sortedData[q3Index - 1] + sortedData[q3Index]) / 2 : sortedData[q3Index];

    const iqr = q3 - q1;
    const lowerFence = q1 - 1.5 * iqr;
    const upperFence = q3 + 1.5 * iqr;

    const nonOutliers = sortedData.filter(d => d >= lowerFence && d <= upperFence);

    const min = nonOutliers.length > 0 ? Math.min(...nonOutliers) : sortedData[0];
    const max = nonOutliers.length > 0 ? Math.max(...nonOutliers) : sortedData[n - 1];

    const sum = sortedData.reduce((acc, val) => acc + val, 0);
    const mean = sum / n;
    const stdDev = n > 1 ? Math.sqrt(sortedData.reduce((acc, val) => acc + Math.pow(val - mean, 2), 0) / (n - 1)) : 0;

    if (isNaN(q1) || isNaN(median) || isNaN(q3) || isNaN(min) || isNaN(max) || isNaN(mean) || isNaN(stdDev)) {
       console.warn("NaN detected during boxplot calculation for data:", data);
       return null;
    }

    return { min, q1, median, q3, max, mean, count: n, stdDev };
}

// --- Component: DataTableComponent ---
interface DataTableProps {
  data: DataRow[];
  columns: string[];
  allColumns: string[];
  filters: Record<string, string>;
  onFilterChange: (column: string, value: string) => void;
  setFilters: React.Dispatch<React.SetStateAction<Record<string, string>>>;
  selectedColumns: string[];
  onColumnToggle: (column: string) => void;
  onRowClick: (row: DataRow) => void;
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
  };

   // Filter out any invalid column names before rendering
   const validDisplayColumns = columns.filter(col => typeof col === 'string' && col);
   const validAllColumns = allColumns.filter(col => typeof col === 'string' && col);

  return (
    <div>
      <div className="flex items-center justify-between mb-2 gap-2 px-4 pt-2">
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline" className="flex items-center gap-1 text-sm h-9">
              <Columns className="h-4 w-4" />
              Columns ({selectedColumns.length}/{validAllColumns.length})
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="start" className="max-h-[400px] overflow-y-auto">
            <DropdownMenuLabel>Toggle Columns</DropdownMenuLabel>
            <DropdownMenuSeparator />
            {validAllColumns.map((column) => (
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
            {Object.values(filters).some(val => val) && !showFilters && <span className="ml-1 text-xs text-blue-500">(Active)</span>}
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

      <ScrollArea className="rounded-md border w-full">
        <Table className="min-w-full whitespace-nowrap">
          <TableHeader>
            <TableRow>
              {validDisplayColumns.map((column) => (
                <TableHead key={column} className="sticky top-0 z-10 bg-background px-3 py-2">
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
              <TableRow className="bg-muted/50 hover:bg-muted/50 sticky top-[calc(theme(spacing.10)+1px)] z-10">
                {validDisplayColumns.map((column) => (
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
                <TableRow key={row.final_id || row.ResponseId || rowIndex} onClick={() => onRowClick(row)} className="cursor-pointer hover:bg-muted/50">
                  {validDisplayColumns.map((column) => (
                    <TableCell key={`${row.final_id || row.ResponseId || rowIndex}-${column}`} className="px-3 py-1.5 text-sm">
                      <TooltipProvider delayDuration={400}>
                         <Tooltip>
                           <TooltipTrigger asChild>
                               <span className="block max-w-[200px] truncate" title={String(row[column] ?? "")}>
                                    {String(row[column] ?? "")}
                               </span>
                           </TooltipTrigger>
                           {String(row[column] ?? "").length > 30 && (
                               <TooltipContent side="bottom" align="start">
                                   <p className="max-w-xs break-words">{String(row[column] ?? "")}</p>
                               </TooltipContent>
                           )}
                         </Tooltip>
                       </TooltipProvider>
                    </TableCell>
                  ))}
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={validDisplayColumns.length} className="h-24 text-center text-muted-foreground">
                  No results found matching your filters.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </ScrollArea>
    </div>
  );
}

// --- Component: DataVisualizerComponent ---
interface DataVisualizerProps {
  data: DataRow[];
  columns: string[];
}

function DataVisualizerComponent({ data, columns }: DataVisualizerProps) {
  const [chartType, setChartType] = useState("bar");
  const [yAxis, setYAxis] = useState("");
  const [xAxis, setXAxis] = useState("");
  const [groupBy, setGroupBy] = useState("none");
  const [numBins, setNumBins] = useState(10);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const chartInstanceRef = useRef<Chart | null>(null);

  const { numericalColumns, categoricalColumns } = useMemo(() => {
    const numerical: string[] = [];
    const categorical: string[] = [];
    const validColumns = columns.filter(c => typeof c === 'string' && c);

    validColumns.forEach(column => {
        const values = data.map(row => row[column]).filter(v => v !== undefined && v !== null && v !== '');
        if (values.length === 0) return;

        let numericCount = 0;
        const validNumericValues: number[] = [];
        values.forEach(val => {
            const strVal = String(val).trim();
            if (strVal !== '' && !isNaN(Number(strVal))) {
                numericCount++;
                validNumericValues.push(Number(strVal));
            }
        });

        const uniqueValues = new Set(values.map(v => String(v)));
        const numericRatio = values.length > 0 ? numericCount / values.length : 0;

        if (numericRatio >= 0.9 && uniqueValues.size > 5 && validNumericValues.length > 0) {
            const range = Math.max(...validNumericValues) - Math.min(...validNumericValues);
            if(range > 0) {
                 numerical.push(column);
            } else {
                categorical.push(column);
            }
        } else if (uniqueValues.size <= 50 && uniqueValues.size >= 1) {
             categorical.push(column);
        } else if (numericRatio > 0.1) {
             categorical.push(column);
        }
    });
    return { numericalColumns: numerical.sort(), categoricalColumns: categorical.sort() };
  }, [data, columns]);

  // Effect to set default axes based on identified column types
   useEffect(() => {
      if (!yAxis || !numericalColumns.includes(yAxis)) {
          const defaultY = ["testscore", "index_confidence", "index_motivation", "index_complement", "index_cheating", "ConversationDurationMinutes", "MessageCount", "age", "gpa"].find(c => numericalColumns.includes(c));
          setYAxis(defaultY || numericalColumns[0] || '');
      }

      if (!xAxis || (!categoricalColumns.includes(xAxis) && chartType !== 'scatter') || (chartType === 'scatter' && !([...categoricalColumns, ...numericalColumns]).includes(xAxis))) {
          const potentialXColumns = chartType === 'scatter' ? [...categoricalColumns, ...numericalColumns] : categoricalColumns;
          const defaultX = ["treatment_clean", "gender", "highgpa"].find(c => potentialXColumns.includes(c) && c !== yAxis);
          setXAxis(defaultX || potentialXColumns.find(c => c !== yAxis) || potentialXColumns[0] || '');
      }

      if (groupBy !== 'none' && (groupBy === xAxis || groupBy === yAxis)) {
          setGroupBy('none');
      }
   }, [columns, numericalColumns, categoricalColumns, xAxis, yAxis, chartType, groupBy]);

  // Effect to render chart
  useEffect(() => {
    if (!canvasRef.current || !yAxis || !xAxis || data.length === 0 || !chartType || typeof Chart === 'undefined') return;
    if(chartType !== 'histogram' && (!yAxis || !xAxis)) return;
    if(chartType === 'histogram' && !yAxis) return;

    const ctx = canvasRef.current.getContext("2d");
    if (!ctx) return;
    if (chartInstanceRef.current) chartInstanceRef.current.destroy();

    let chartData: any = { labels: [], datasets: [] };
    let options: any = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false, position: 'top' },
            title: { display: true, text: `Chart Title Placeholder`, font: { size: 14 } },
            tooltip: {
                backgroundColor: 'rgba(0,0,0,0.8)',
                titleFont: { weight: 'bold' },
                bodyFont: { size: 11 },
                padding: 10,
                boxPadding: 4,
                callbacks: {}
            }
        },
        scales: {
            x: { title: { display: true, text: xAxis }, grid: { display: false } },
            y: { beginAtZero: true, title: { display: true, text: yAxis }, grid: { color: '#e5e7eb' } }
        },
        animation: { duration: 500 }
    };
    let type: keyof ChartTypeRegistry = 'bar';

    const colors = ['#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899', '#06b6d4', '#f97316', '#6b7280', '#d946ef'];

    const formatNumber = (num: number | string) => {
        if (typeof num === 'number' && !isNaN(num)) {
            if (Math.abs(num) < 0.01 && num !== 0) return num.toExponential(1);
            if (Math.abs(num) >= 1e6) return num.toExponential(1);
            return num.toLocaleString(undefined, { minimumFractionDigits: 0, maximumFractionDigits: 2 });
        }
        return String(num);
    };

    const getGroupedData = () => {
        const groups: Record<string, Record<string, number[]>> = {};
        const xValues = new Set<string>();
        const groupValues = new Set<string>();
        const useGrouping = groupBy && groupBy !== 'none' && categoricalColumns.includes(groupBy);

        data.forEach(row => {
            const xVal = String(row[xAxis] ?? 'N/A');
            const groupVal = useGrouping ? String(row[groupBy] ?? 'N/A') : '_main_';
            const yVal = Number(row[yAxis]);

            if (isNaN(yVal)) return;

            xValues.add(xVal);
            if (useGrouping) groupValues.add(groupVal);

            if (!groups[groupVal]) groups[groupVal] = {};
            if (!groups[groupVal][xVal]) groups[groupVal][xVal] = [];
            groups[groupVal][xVal].push(yVal);
        });

        const sortedXValues = [...xValues].sort((a, b) => {
            const numA = Number(a);
            const numB = Number(b);
            if (!isNaN(numA) && !isNaN(numB)) {
                return numA - numB;
            }
            return a.localeCompare(b, undefined, { sensitivity: 'base' });
        });

        const sortedGroupValues = useGrouping ? [...groupValues].sort((a, b) => a.localeCompare(b, undefined, { sensitivity: 'base' })) : ['_main_'];

        return { groups, sortedXValues, sortedGroupValues, useGrouping };
    };

    const { groups, sortedXValues, sortedGroupValues, useGrouping } = getGroupedData();
    chartData.labels = sortedXValues;
    options.plugins.legend.display = useGrouping && sortedGroupValues.length > 1;

    if (chartType === 'bar') {
        type = 'bar';
        chartData.datasets = sortedGroupValues.map((groupVal, index) => {
             const means = sortedXValues.map(xVal => {
                 const values = groups[groupVal]?.[xVal] || [];
                 const sum = values.reduce((a, b) => a + b, 0);
                 return values.length > 0 ? sum / values.length : NaN;
             });
             return {
                label: groupVal === '_main_' ? `Avg ${yAxis}` : groupVal,
                data: means,
                backgroundColor: colors[index % colors.length] + 'BF',
                borderColor: colors[index % colors.length],
                borderWidth: 1
             };
        });
        options.plugins.title.text = `Average ${yAxis} by ${xAxis}${useGrouping ? ` (Grouped by ${groupBy})` : ''}`;
    } else if (chartType === 'line') {
        type = 'line';
        chartData.datasets = sortedGroupValues.map((groupVal, index) => {
             const means = sortedXValues.map(xVal => {
                 const values = groups[groupVal]?.[xVal] || [];
                 const sum = values.reduce((a, b) => a + b, 0);
                 return values.length > 0 ? sum / values.length : NaN;
             });
             return {
                label: groupVal === '_main_' ? `Avg ${yAxis}` : groupVal,
                data: means,
                backgroundColor: colors[index % colors.length] + '30',
                borderColor: colors[index % colors.length],
                borderWidth: 2,
                tension: 0.1,
                fill: false
             };
        });
        options.plugins.title.text = `Average ${yAxis} Trend by ${xAxis}${useGrouping ? ` (Grouped by ${groupBy})` : ''}`;
    } else if (chartType === 'pie' && !useGrouping) {
        type = 'pie';
        const means = sortedXValues.map(xVal => {
            const values = groups['_main_']?.[xVal] || [];
            const sum = values.reduce((a, b) => a + b, 0);
            return values.length > 0 ? sum / values.length : 0;
        });
        chartData.datasets = [{
            data: means,
            backgroundColor: sortedXValues.map((_, i) => colors[i % colors.length] + 'BF'),
            borderColor: sortedXValues.map((_, i) => colors[i % colors.length]),
            borderWidth: 1
        }];
        delete options.scales;
        options.plugins.title.text = `${yAxis} Distribution by ${xAxis}`;
        options.plugins.legend.display = true;
    }

    try {
        chartInstanceRef.current = new Chart(ctx, { type, data: chartData, options });
    } catch (error) {
         console.error("Chart.js rendering error:", error);
         ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
         ctx.fillStyle = 'red';
         ctx.font = '14px sans-serif';
         ctx.textAlign = 'center';
         ctx.fillText('Error rendering chart. Check console.', canvasRef.current.width / 2, canvasRef.current.height / 2);
    }

    return () => {
      if (chartInstanceRef.current) {
        chartInstanceRef.current.destroy();
        chartInstanceRef.current = null;
      }
    };
  }, [data, yAxis, xAxis, groupBy, chartType, numBins, numericalColumns, categoricalColumns]);

  const downloadChart = () => {
     if (!canvasRef.current || !chartInstanceRef.current) {
         alert("Chart not ready or failed to render.");
         return;
     }
     
     const link = document.createElement("a");
     link.download = `chart-${chartType}-${yAxis}-by-${xAxis}${groupBy && groupBy !== "none" ? `-grouped-${groupBy}` : ""}.png`;
     link.href = canvasRef.current.toDataURL("image/png");
     link.click();
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">Data Visualization</CardTitle>
         <p className="text-sm text-muted-foreground">Explore relationships between variables.</p>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 mb-4 items-end">
          <div>
            <label htmlFor="chartTypeSelect" className="block text-xs font-medium mb-1 text-muted-foreground">Chart Type</label>
            <Select value={chartType} onValueChange={setChartType}>
              <SelectTrigger id="chartTypeSelect" className="h-9"> <SelectValue placeholder="Chart Type" /> </SelectTrigger>
              <SelectContent>
                <SelectItem value="bar"><div className="flex items-center gap-2"><BarChart className="h-4 w-4 text-blue-500"/>Bar Chart</div></SelectItem>
                <SelectItem value="line"><div className="flex items-center gap-2"><LineChart className="h-4 w-4 text-green-500"/>Line Chart</div></SelectItem>
                <SelectItem value="pie" disabled={groupBy !== 'none'}><div className="flex items-center gap-2"><PieChart className="h-4 w-4 text-yellow-500"/>Pie Chart</div></SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div>
            <label htmlFor="yAxisSelect" className="block text-xs font-medium mb-1 text-muted-foreground">Y-Axis (Numeric)</label>
            <Select value={yAxis} onValueChange={setYAxis}>
              <SelectTrigger id="yAxisSelect" className="h-9"> <SelectValue placeholder="Select Variable" /> </SelectTrigger>
              <SelectContent>
                {numericalColumns.length > 0 ? numericalColumns.map((column) => (
                  <SelectItem key={`y-${column}`} value={column}>{column}</SelectItem>
                )) : <SelectItem value="" disabled>No numeric columns</SelectItem>}
              </SelectContent>
            </Select>
          </div>
          <div>
            <label htmlFor="xAxisSelect" className="block text-xs font-medium mb-1 text-muted-foreground">X-Axis (Category)</label>
            <Select value={xAxis} onValueChange={setXAxis} disabled={!yAxis}>
              <SelectTrigger id="xAxisSelect" className="h-9"> <SelectValue placeholder="Select X-Axis" /> </SelectTrigger>
              <SelectContent>
                {categoricalColumns
                  .filter(c => c !== yAxis)
                  .map((column) => (
                    <SelectItem key={`x-${column}`} value={column}>{column}</SelectItem>
                  ))}
                {categoricalColumns.length === 0 && <SelectItem value="" disabled>No categorical columns</SelectItem>}
              </SelectContent>
            </Select>
          </div>
          <div>
            <label htmlFor="groupBySelect" className="block text-xs font-medium mb-1 text-muted-foreground">Group By (Optional)</label>
            <Select 
              value={groupBy} 
              onValueChange={(val) => {
                setGroupBy(val);
                if (val !== 'none' && chartType === 'pie') setChartType('bar');
              }}
              disabled={!yAxis || !xAxis}
            >
              <SelectTrigger id="groupBySelect" className="h-9"> <SelectValue placeholder="Group By" /> </SelectTrigger>
              <SelectContent>
                <SelectItem value="none">No Grouping</SelectItem>
                {categoricalColumns
                  .filter(col => col !== xAxis && col !== yAxis)
                  .map((column) => (
                    <SelectItem key={`group-${column}`} value={column}>{column}</SelectItem>
                  ))}
                {categoricalColumns.filter(col => col !== xAxis && col !== yAxis).length === 0 && 
                  <SelectItem value="" disabled>No other category columns</SelectItem>
                }
              </SelectContent>
            </Select>
          </div>
        </div>

        <div className="flex justify-end mb-2">
          <Button variant="outline" size="sm" onClick={downloadChart} className="flex items-center gap-2 h-9" disabled={!chartInstanceRef.current}>
            <Download className="h-4 w-4" /> Download Chart
          </Button>
        </div>

        <div className="border rounded-lg p-2 sm:p-4 bg-background aspect-video relative min-h-[350px]">
          {(!yAxis || !xAxis) && (
             <div className="absolute inset-0 flex items-center justify-center text-muted-foreground">Select axes to render the chart.</div>
          )}
          {(yAxis && xAxis) && (
             <canvas ref={canvasRef}></canvas>
          )}
        </div>
      </CardContent>
    </Card>
  );
}

// --- Component: DataSummaryComponent ---
interface DataSummaryProps {
  data: DataRow[];
  columns: string[];
}

function DataSummaryComponent({ data, columns }: DataSummaryProps) {
  const [selectedDistColumn, setSelectedDistColumn] = useState("");
  const [showAllMissing, setShowAllMissing] = useState(false);
  
  const validColumns = useMemo(() => columns.filter(c => typeof c === 'string' && c), [columns]);

  // Identify potential columns for different summary types
  const { potentialDistributionColumns } = useMemo(() => {
    const distCols: string[] = [];

    validColumns.forEach(col => {
      const values = data.map(row => row[col]).filter(v => v !== undefined && v !== null && v !== '');
      if (values.length === 0) return;

      const uniqueValues = new Set(values.map(v => String(v)));
      if (uniqueValues.size > 1 && uniqueValues.size <= 50) {
        distCols.push(col);
      }
    });

    return { potentialDistributionColumns: distCols.sort() };
  }, [data, validColumns]);

  // Set default selection once columns are identified
  useEffect(() => {
    if (!selectedDistColumn && potentialDistributionColumns.length > 0) {
      const defaultDist = ["treatment_clean", "gender", "highgpa"].find(c => potentialDistributionColumns.includes(c));
      setSelectedDistColumn(defaultDist || potentialDistributionColumns[0]);
    }
  }, [potentialDistributionColumns, selectedDistColumn]);

  // Memoized calculations for summaries
  const { summaryStats, missingStats } = useMemo(() => {
    const summary: any[] = [];
    const missing: any[] = [];
    const totalRows = data.length;

    validColumns.forEach(column => {
      const values = data.map(row => row[column]);
      const validValues = values.filter(val => val !== undefined && val !== null && val !== '');
      const missingCount = totalRows - validValues.length;
      const missingPercentage = totalRows > 0 ? (missingCount / totalRows) * 100 : 0;
      missing.push({ column, missingCount, missingPercentage });

      const numericValues = validValues.map(val => Number(String(val).trim())).filter(val => !isNaN(val));
      const isLikelyNumeric = numericValues.length > 0 && numericValues.length / validValues.length > 0.8;
      const uniqueCount = new Set(validValues.map(v => String(v))).size;

      const stats: any = {
        column,
        count: validValues.length,
        uniqueCount: uniqueCount,
        missingCount,
        missingPercentage,
        isNumeric: isLikelyNumeric,
        min: '-', max: '-', mean: '-', median: '-', stdDev: '-'
      };

      if (isLikelyNumeric && numericValues.length > 0) {
        const boxStats = calculateBoxPlotStats(numericValues);
        if(boxStats){
          stats.min = boxStats.min;
          stats.max = boxStats.max;
          stats.mean = boxStats.mean;
          stats.median = boxStats.median;
          stats.stdDev = boxStats.stdDev;
        }
      }
      summary.push(stats);
    });

    missing.sort((a, b) => b.missingPercentage - a.missingPercentage);
    summary.sort((a,b) => a.column.localeCompare(b.column));
    return { summaryStats: summary, missingStats: missing };
  }, [data, validColumns]);

  const frequencyDistribution = useMemo(() => {
    if (!selectedDistColumn || data.length === 0 || !potentialDistributionColumns.includes(selectedDistColumn)) return [];

    const values = data.map(row => row[selectedDistColumn]).filter(val => val !== undefined && val !== null && val !== '');
    const totalValid = values.length;
    if (totalValid === 0) return [];

    const valueCounts: Record<string, number> = {};
    values.forEach(val => {
      const key = String(val).trim() || '""';
      valueCounts[key] = (valueCounts[key] || 0) + 1;
    });

    return Object.entries(valueCounts)
      .sort(([, countA], [, countB]) => countB - countA)
      .map(([value, count]) => ({
        value: value === '""' ? '(Empty String)' : value,
        count,
        percentage: (count / totalValid) * 100
      }));
  }, [data, selectedDistColumn, potentialDistributionColumns]);

  const formatNumber = (num: number | string | undefined | null, precision = 2): string => {
    if (num === undefined || num === null || num === '-') return '-';
    const numVal = Number(num);
    if (isNaN(numVal)) return String(num);

    if (Math.abs(numVal) < 1e-6 && numVal !== 0) return numVal.toExponential(1);
    if (Math.abs(numVal) >= 1e9) return numVal.toExponential(1);

    return numVal.toLocaleString(undefined, {
      minimumFractionDigits: Number.isInteger(numVal) ? 0 : Math.min(precision, 2),
      maximumFractionDigits: precision
    });
  };
  
  const formatPercentage = (num: number | undefined | null): string => {
    if (typeof num !== 'number' || isNaN(num)) return '-';
    return num.toFixed(1) + '%';
  };

  const displayedMissingStats = showAllMissing ? missingStats : missingStats.slice(0, 10);

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Column Summaries</CardTitle>
          <p className="text-sm text-muted-foreground">Basic statistics for each column in the dataset.</p>
        </CardHeader>
        <CardContent>
          <ScrollArea className="max-h-[450px] w-full border rounded-md">
            <Table className="min-w-full text-xs">
              <TableHeader className="sticky top-0 bg-background z-10 shadow-sm">
                <TableRow>
                  <TableHead className="w-[150px] font-semibold">Column</TableHead>
                  <TableHead className="font-semibold">Type</TableHead>
                  <TableHead className="font-semibold text-right">Count</TableHead>
                  <TableHead className="font-semibold text-right">Unique</TableHead>
                  <TableHead className="font-semibold text-right">Missing %</TableHead>
                  <TableHead className="font-semibold text-right">Min</TableHead>
                  <TableHead className="font-semibold text-right">Max</TableHead>
                  <TableHead className="font-semibold text-right">Mean</TableHead>
                  <TableHead className="font-semibold text-right">Median</TableHead>
                  <TableHead className="font-semibold text-right">Std Dev</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {summaryStats.length > 0 ? summaryStats.map((stats) => (
                  <TableRow key={stats.column} className="hover:bg-muted/50">
                    <TableCell className="font-medium max-w-[150px] truncate py-1.5" title={stats.column}>{stats.column}</TableCell>
                    <TableCell className="py-1.5">{stats.isNumeric ? "Numeric" : "Category"}</TableCell>
                    <TableCell className="text-right py-1.5">{formatNumber(stats.count, 0)}</TableCell>
                    <TableCell className="text-right py-1.5">{formatNumber(stats.uniqueCount, 0)}</TableCell>
                    <TableCell className="text-right py-1.5">{formatPercentage(stats.missingPercentage)}</TableCell>
                    <TableCell className="text-right py-1.5">{formatNumber(stats.min)}</TableCell>
                    <TableCell className="text-right py-1.5">{formatNumber(stats.max)}</TableCell>
                    <TableCell className="text-right py-1.5">{formatNumber(stats.mean)}</TableCell>
                    <TableCell className="text-right py-1.5">{formatNumber(stats.median)}</TableCell>
                    <TableCell className="text-right py-1.5">{formatNumber(stats.stdDev)}</TableCell>
                  </TableRow>
                )) : (
                  <TableRow><TableCell colSpan={10} className="text-center h-20 text-muted-foreground">No summary data.</TableCell></TableRow>
                )}
              </TableBody>
            </Table>
          </ScrollArea>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Frequency Distribution</CardTitle>
            <p className="text-sm text-muted-foreground">Counts and percentages for categories in a selected column.</p>
          </CardHeader>
          <CardContent>
            <div className="mb-3">
              <label htmlFor="distColSelect" className="block text-xs font-medium mb-1 text-muted-foreground">Column (Category)</label>
              <Select value={selectedDistColumn} onValueChange={setSelectedDistColumn}>
                <SelectTrigger id="distColSelect" className="h-9"><SelectValue placeholder="Select Column" /></SelectTrigger>
                <SelectContent>
                  {potentialDistributionColumns.map((column) => (
                    <SelectItem key={`dist-${column}`} value={column}>{column}</SelectItem>
                  ))}
                  {potentialDistributionColumns.length === 0 && <SelectItem value="" disabled>No suitable columns</SelectItem>}
                </SelectContent>
              </Select>
            </div>
            <ScrollArea className="max-h-[300px] border rounded-md">
              <Table className="text-xs">
                <TableHeader className="sticky top-0 bg-background z-10 shadow-sm">
                  <TableRow>
                    <TableHead className="font-semibold">Value</TableHead>
                    <TableHead className="font-semibold text-right">Count</TableHead>
                    <TableHead className="font-semibold text-right">%</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {frequencyDistribution.length > 0 ? frequencyDistribution.map((item, index) => (
                    <TableRow key={index} className="hover:bg-muted/50">
                      <TableCell className="max-w-[180px] truncate py-1.5" title={item.value}>{item.value}</TableCell>
                      <TableCell className="text-right py-1.5">{formatNumber(item.count, 0)}</TableCell>
                      <TableCell className="text-right py-1.5">{formatPercentage(item.percentage)}</TableCell>
                    </TableRow>
                  )) : (
                    <TableRow><TableCell colSpan={3} className="text-center text-muted-foreground h-24">{selectedDistColumn ? "No data or column not suitable." : "Select a column."}</TableCell></TableRow>
                  )}
                </TableBody>
              </Table>
            </ScrollArea>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Missing Values</CardTitle>
            <p className="text-sm text-muted-foreground">Columns sorted by the percentage of missing entries.</p>
          </CardHeader>
          <CardContent>
            <ScrollArea className="max-h-[340px] border rounded-md">
              <Table className="text-xs">
                <TableHeader className="sticky top-0 bg-background z-10 shadow-sm">
                  <TableRow>
                    <TableHead className="font-semibold">Column</TableHead>
                    <TableHead className="font-semibold text-right">Missing #</TableHead>
                    <TableHead className="font-semibold text-right">Missing %</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {displayedMissingStats.filter(s => s.missingCount > 0).length > 0 ? displayedMissingStats.filter(s => s.missingCount > 0).map((stats) => (
                    <TableRow key={`missing-${stats.column}`} className="hover:bg-muted/50">
                      <TableCell className="max-w-[180px] truncate py-1.5" title={stats.column}>{stats.column}</TableCell>
                      <TableCell className="text-right py-1.5">{formatNumber(stats.missingCount, 0)}</TableCell>
                      <TableCell className="text-right py-1.5">{formatPercentage(stats.missingPercentage)}</TableCell>
                    </TableRow>
                  )) : (
                    <TableRow><TableCell colSpan={3} className="text-center text-muted-foreground h-24">No missing values found.</TableCell></TableRow>
                  )}
                </TableBody>
              </Table>
            </ScrollArea>
            {missingStats.filter(s => s.missingCount > 0).length > 10 && (
              <Button variant="link" size="sm" onClick={() => setShowAllMissing(!showAllMissing)} className="mt-2 p-0 h-auto text-xs">
                {showAllMissing ? "Show Top 10" : `Show All (${missingStats.filter(s => s.missingCount > 0).length})`}
              </Button>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

// --- Main Page Component: DataExplorer ---
interface DataExplorerProps {
  initialData: DataRow[];
  initialColumns: string[];
}

export default function DataExplorer({ initialData, initialColumns }: DataExplorerProps) {  const rawData = useMemo(() => initialData, [initialData]);
  const allColumns = useMemo(() => initialColumns.filter(c => typeof c === 'string' && c), [initialColumns]);

  const [loading, setLoading] = useState(!initialData || initialData.length === 0);
  const [searchTerm, setSearchTerm] = useState("");
  const [filters, setFilters] = useState<Record<string, string>>({});
  const [selectedColumns, setSelectedColumns] = useState<string[]>(() => {
    const defaultCols = ["final_id", "treatment_clean", "gender", "highgpa", "testscore", "index_complement", "index_confidence", "index_cheating", "index_motivation", "MessageCount", "ConversationDurationMinutes"];
    const validDefaultCols = defaultCols.filter(col => allColumns.includes(col));
    const initialSelect = validDefaultCols.length > 5 ? validDefaultCols : allColumns.slice(0, Math.min(allColumns.length, 10));
    return initialSelect;
  });
  const [pagination, setPagination] = useState({ currentPage: 1, itemsPerPage: 25 });
  const [activeTab, setActiveTab] = useState("table");
  const [selectedRowData, setSelectedRowData] = useState<DataRow | null>(null);

  // Effect to handle initial loading state
  useEffect(() => {
    if (initialData && initialData.length > 0 && allColumns.length > 0) {
      setLoading(false);
      setSelectedColumns(prev => {
        const validSelected = prev.filter(col => allColumns.includes(col));
        if (validSelected.length === 0) {
          const defaultCols = ["final_id", "treatment_clean", "gender", "highgpa", "testscore", "index_complement", "index_confidence", "index_cheating", "index_motivation", "MessageCount", "ConversationDurationMinutes"];
          const validDefaultCols = defaultCols.filter(col => allColumns.includes(col));
          return validDefaultCols.length > 5 ? validDefaultCols : allColumns.slice(0, Math.min(allColumns.length, 10));
        }
        return validSelected;
      });
    } else if (initialData) {
      setLoading(false);
    }
  }, [initialData, allColumns]);

  // Memoized filtering logic
  const filteredData = useMemo(() => {
    if (!rawData) return [];
    let filtered = rawData;

    // Global Search
    if (searchTerm) {
      const lowerSearchTerm = searchTerm.toLowerCase().trim();
      if (lowerSearchTerm) {
        filtered = filtered.filter(row =>
          allColumns.some(col => {
            const value = row[col];
            return value !== null && value !== undefined && String(value).toLowerCase().includes(lowerSearchTerm);
          })
        );
      }
    }

    // Column Filters
    const activeFilters = Object.entries(filters).filter(([_, value]) => value && value.trim());
    if (activeFilters.length > 0) {
      filtered = filtered.filter(row =>
        activeFilters.every(([column, filterValue]) => {
          const lowerFilterValue = filterValue.toLowerCase().trim();
          const cellValue = row[column];
          return cellValue !== null && cellValue !== undefined && String(cellValue).toLowerCase().includes(lowerFilterValue);
        })
      );
    }
    return filtered;
  }, [rawData, searchTerm, filters, allColumns]);

  // Memoized pagination logic
  const paginatedData = useMemo(() => {
    const startIndex = (pagination.currentPage - 1) * pagination.itemsPerPage;
    return filteredData.slice(startIndex, startIndex + pagination.itemsPerPage);
  }, [filteredData, pagination.currentPage, pagination.itemsPerPage]);

  const totalPages = Math.max(1, Math.ceil(filteredData.length / pagination.itemsPerPage));

  // Handlers
  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => { 
    setSearchTerm(e.target.value); 
    setPagination(p => ({ ...p, currentPage: 1 })); 
  };
  
  const handleFilterChange = (column: string, value: string) => { 
    setFilters(prev => ({ ...prev, [column]: value })); 
    setPagination(p => ({ ...p, currentPage: 1 })); 
  };
  
  const handleColumnToggle = (column: string) => {
    setSelectedColumns(prev => {
      const isSelected = prev.includes(column);
      if (isSelected && prev.length <= 1) return prev;
      return isSelected ? prev.filter(col => col !== column) : [...prev, column];
    });
  };
  
  const handlePageChange = (page: number) => {
    const newPage = Math.max(1, Math.min(page, totalPages));
    if (newPage !== pagination.currentPage) {
      setPagination(p => ({ ...p, currentPage: newPage }));
    }
  };
  
  const handleItemsPerPageChange = (value: string) => { 
    setPagination({ currentPage: 1, itemsPerPage: Number.parseInt(value) || 25 }); 
  };
  
  const handleRowClick = (row: DataRow) => {
    setSelectedRowData(row);
  };

  // CSV Export Function
  const exportCSV = () => {
    if (filteredData.length === 0) { 
      alert("No data to export based on current filters."); 
      return; 
    }
    
    const dataToExport = filteredData.map(row => {
      const newRow: Record<string, any> = {};
      selectedColumns.forEach(col => {
        newRow[col] = row[col] ?? "";
      });
      return newRow;
    });

    try {
      const csvString = Papa.unparse(dataToExport, {
        columns: selectedColumns,
        header: true,
        quotes: true,
        quoteChar: '"',
        escapeChar: '"',
        delimiter: ",",
        newline: "\r\n"
      });

      const blob = new Blob([`\uFEFF${csvString}`], { type: "text/csv;charset=utf-8;" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      link.setAttribute("href", url);
      link.setAttribute("download", `esperanto_export_${timestamp}.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Error generating CSV:", error);
      alert("Failed to generate CSV file. Check console for details.");
    }
  };

  // Pagination Rendering Logic
  const renderPaginationItems = () => {
    if (totalPages <= 1) return null;

    const items = [];
    const maxPagesToShow = 5;
    const halfMaxPages = Math.floor(maxPagesToShow / 2);

    let startPageNum = Math.max(1, pagination.currentPage - halfMaxPages);
    let endPageNum = Math.min(totalPages, pagination.currentPage + halfMaxPages);

    if (pagination.currentPage - halfMaxPages <= 1) {
      endPageNum = Math.min(totalPages, maxPagesToShow);
    }
    if (pagination.currentPage + halfMaxPages >= totalPages) {
      startPageNum = Math.max(1, totalPages - maxPagesToShow + 1);
    }

    // "First" button and ellipsis
    if (startPageNum > 1) {
      items.push(
        <PaginationItem key={1}>
          <PaginationLink onClick={() => handlePageChange(1)} className="cursor-pointer">1</PaginationLink>
        </PaginationItem>
      );
      if (startPageNum > 2) {
        items.push(<PaginationItem key="start-ellipsis"><PaginationEllipsis /></PaginationItem>);
      }
    }

    // Page number links
    for (let i = startPageNum; i <= endPageNum; i++) {
      items.push(
        <PaginationItem key={i}>
          <PaginationLink 
            isActive={pagination.currentPage === i} 
            onClick={() => handlePageChange(i)} 
            className="cursor-pointer"
            aria-current={pagination.currentPage === i ? 'page' : undefined}
          >
            {i}
          </PaginationLink>
        </PaginationItem>
      );
    }

    // "Last" button and ellipsis
    if (endPageNum < totalPages) {
      if (endPageNum < totalPages - 1) {
        items.push(<PaginationItem key="end-ellipsis"><PaginationEllipsis /></PaginationItem>);
      }
      items.push(
        <PaginationItem key={totalPages}>
          <PaginationLink onClick={() => handlePageChange(totalPages)} className="cursor-pointer">{totalPages}</PaginationLink>
        </PaginationItem>
      );
    }
    return items;
  };

  // Loading State
  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen p-4 text-center">
        <Loader2 className="h-10 w-10 animate-spin text-primary mb-4" />
        <p className="text-lg font-semibold">Loading Data...</p>
        <p className="text-muted-foreground">Please wait while the dataset is being fetched and processed.</p>
      </div>
    );
  }

  // Error State
  if (!initialData || allColumns.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen p-4 text-center text-destructive">
        <Info className="h-10 w-10 mb-4"/>
        <p className="text-lg font-semibold">Failed to Load Data</p>
        <p>Could not load or parse the dataset. Please check the file path and ensure the CSV format is valid.</p>
        <p className="text-sm mt-2">(Check browser console and server logs for more details)</p>
      </div>
    );
  }

  // Main Explorer UI
  return (
    <div className="p-4 md:p-6 space-y-4 max-w-screen-2xl mx-auto">
      {/* Top Controls: Search, Rows per page, Export */}
      <div className="flex flex-col md:flex-row gap-2 md:items-center">
        {/* Search Input */}
        <div className="relative flex-grow">
          <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input placeholder="Search all columns..." value={searchTerm} onChange={handleSearchChange} className="pl-8 h-9 w-full md:w-auto" />
        </div>
        {/* Rows per Page & Export */}
        <div className="flex gap-2 flex-shrink-0">
          <Select value={pagination.itemsPerPage.toString()} onValueChange={handleItemsPerPageChange}>
            <SelectTrigger className="w-[130px] h-9 text-xs"> <SelectValue placeholder="Rows per page" /> </SelectTrigger>
            <SelectContent>
              <SelectItem value="10">10 rows</SelectItem>
              <SelectItem value="25">25 rows</SelectItem>
              <SelectItem value="50">50 rows</SelectItem>
              <SelectItem value="100">100 rows</SelectItem>
              <SelectItem value="250">250 rows</SelectItem>
            </SelectContent>
          </Select>
          <Button variant="outline" size="sm" onClick={exportCSV} className="h-9">
            <Download className="h-4 w-4 mr-1.5" /> Export CSV
          </Button>
        </div>
      </div>

      {/* Main Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-3 mb-4">
          <TabsTrigger value="table" className="flex items-center gap-1.5"> <TableIcon className="h-4 w-4" /> Table </TabsTrigger>
          <TabsTrigger value="visualize" className="flex items-center gap-1.5"> <AreaChart className="h-4 w-4" /> Visualize </TabsTrigger>
          <TabsTrigger value="summary" className="flex items-center gap-1.5"> <BarChart className="h-4 w-4" /> Summary </TabsTrigger>
        </TabsList>

        {/* Table Tab Content */}
        <TabsContent value="table" className="mt-0 focus-visible:ring-0">
          <Card className="overflow-hidden">
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
                onRowClick={handleRowClick}
              />
            </CardContent>
            {/* Pagination Controls */}
            {filteredData.length > 0 && totalPages > 1 && (
              <div className="flex items-center justify-between flex-wrap gap-2 p-3 border-t bg-background">
                <div className="text-xs text-muted-foreground">
                  Showing {filteredData.length > 0 ? (pagination.currentPage - 1) * pagination.itemsPerPage + 1 : 0}
                  {' '}to {Math.min(pagination.currentPage * pagination.itemsPerPage, filteredData.length)}
                  {' '}of {filteredData.length} results
                </div>
                <Pagination>
                  <PaginationContent>
                    <PaginationItem>
                      <PaginationPrevious
                        onClick={() => handlePageChange(pagination.currentPage - 1)}
                        className={pagination.currentPage === 1 ? "pointer-events-none opacity-50 cursor-not-allowed" : "cursor-pointer"}
                        aria-disabled={pagination.currentPage === 1}
                      />
                    </PaginationItem>
                    {renderPaginationItems()}
                    <PaginationItem>
                      <PaginationNext
                        onClick={() => handlePageChange(pagination.currentPage + 1)}
                        className={pagination.currentPage === totalPages ? "pointer-events-none opacity-50 cursor-not-allowed" : "cursor-pointer"}
                        aria-disabled={pagination.currentPage === totalPages}
                      />
                    </PaginationItem>
                  </PaginationContent>
                </Pagination>
              </div>
            )}
            {filteredData.length === 0 && searchTerm && (
              <div className="p-4 text-center text-sm text-muted-foreground border-t">No results match your search term "{searchTerm}".</div>
            )}
            {filteredData.length === 0 && !searchTerm && Object.values(filters).some(f => f) && (
              <div className="p-4 text-center text-sm text-muted-foreground border-t">No results match your current filters.</div>
            )}
          </Card>
        </TabsContent>

        {/* Visualize Tab Content */}
        <TabsContent value="visualize" className="mt-0 focus-visible:ring-0">
          <DataVisualizerComponent data={filteredData} columns={allColumns} />
        </TabsContent>

        {/* Summary Tab Content */}
        <TabsContent value="summary" className="mt-0 focus-visible:ring-0">
          <DataSummaryComponent data={rawData} columns={allColumns} />
        </TabsContent>
      </Tabs>

      {/* Dialog for Row Details */}
      <Dialog open={selectedRowData !== null} onOpenChange={(isOpen) => !isOpen && setSelectedRowData(null)}>
        <DialogContent className="max-w-3xl sm:max-w-4xl md:max-w-5xl">
          <DialogHeader>
            <DialogTitle>Row Details</DialogTitle>
            <DialogDescription>
              Viewing details for row ID: {selectedRowData?.final_id || selectedRowData?.ResponseId || 'N/A'}
              {' '}| Treatment: {selectedRowData?.treatment_clean || selectedRowData?.treatment || 'N/A'}
            </DialogDescription>
          </DialogHeader>
          <ScrollArea className="max-h-[65vh] p-1 pr-3 my-4 border rounded-md">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-4 gap-y-2 p-3 text-sm">
              {selectedRowData && Object.entries(selectedRowData).map(([key, value]) => (
                <div key={key} className="flex flex-col border-b pb-1 last:border-b-0 sm:border-b-0 sm:pb-0">
                  <span className="font-medium text-muted-foreground truncate" title={key}>{key}:</span>
                  {key === 'conversation_messages' ? (
                    <pre className="text-xs whitespace-pre-wrap break-words bg-muted p-2 rounded mt-1 font-mono max-h-48 overflow-auto">
                      {String(value || 'N/A')}
                    </pre>
                  ) : (
                    <span className="break-words mt-0.5" title={String(value ?? '')}>
                      {String(value ?? 'N/A')}
                    </span>
                  )}
                </div>
              ))}
            </div>
          </ScrollArea>
          <DialogClose asChild>
            <Button type="button" variant="outline" size="sm">Close</Button>
          </DialogClose>
        </DialogContent>
      </Dialog>
    </div>
  );
}

