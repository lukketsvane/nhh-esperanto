"use client"

import { useState, useMemo, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Button } from "@/components/ui/button"

interface DataSummaryProps {
  data: any[]
  columns: string[]
}

export default function DataSummary({ data, columns }: DataSummaryProps) {
  const [selectedDistColumn, setSelectedDistColumn] = useState("")
  const [showAllMissing, setShowAllMissing] = useState(false)

  useEffect(() => {
    if (columns.length > 0 && !selectedDistColumn) {
      const categoricalColumns = [
        "treatment_clean",
        "gender",
        "faculty",
        "yearincollege",
        "ai_assist",
        "ai_guided",
        "control",
      ]
      const foundColumn =
        columns.find((col) => categoricalColumns.includes(col)) ||
        columns.find((col) => col === "treatment") ||
        columns[0]
      setSelectedDistColumn(foundColumn || columns[0])
    }
  }, [columns, selectedDistColumn])

  const { summaryStats, missingStats } = useMemo(() => {
    const summary: any[] = []
    const missing: any[] = []

    columns.forEach((column) => {
      if (!column) return

      const values = data.map((row) => row[column])
      const validValues = values.filter((val) => val !== undefined && val !== null && val !== "")

      const missingCount = values.length - validValues.length
      const missingPercentage = data.length > 0 ? (missingCount / data.length) * 100 : 0

      missing.push({ column, missingCount, missingPercentage })

      const numericValues = validValues.map((val) => Number(val)).filter((val) => !isNaN(val))
      const isLikelyNumeric =
        validValues.length > 0 && numericValues.length / validValues.length > 0.8 && new Set(numericValues).size > 5

      const stats: any = {
        column,
        count: validValues.length,
        uniqueCount: new Set(validValues).size,
        missingCount,
        missingPercentage,
        isNumeric: isLikelyNumeric,
        min: "-",
        max: "-",
        mean: "-",
        median: "-",
        stdDev: "-",
      }

      if (isLikelyNumeric && numericValues.length > 0) {
        stats.min = Math.min(...numericValues)
        stats.max = Math.max(...numericValues)
        const sum = numericValues.reduce((s, v) => s + v, 0)
        stats.mean = sum / numericValues.length
        stats.median = calculateMedian(numericValues)
        stats.stdDev = calculateStdDev(numericValues, stats.mean)
      }
      summary.push(stats)
    })
    missing.sort((a, b) => b.missingPercentage - a.missingPercentage)
    return { summaryStats: summary, missingStats: missing }
  }, [data, columns])

  const frequencyDistribution = useMemo(() => {
    if (!selectedDistColumn || data.length === 0) return []

    const values = data
      .map((row) => row[selectedDistColumn])
      .filter((val) => val !== undefined && val !== null && val !== "")
    if (values.length === 0) return []

    const valueCounts: Record<string, number> = {}
    values.forEach((val) => {
      const key = String(val)
      valueCounts[key] = (valueCounts[key] || 0) + 1
    })

    return Object.entries(valueCounts)
      .sort((a, b) => b[1] - a[1])
      .map(([value, count]) => ({
        value,
        count,
        percentage: (count / values.length) * 100,
      }))
  }, [data, selectedDistColumn])

  const calculateMedian = (values: number[]) => {
    if (values.length === 0) return 0
    const sorted = [...values].sort((a, b) => a - b)
    const middle = Math.floor(sorted.length / 2)
    return sorted.length % 2 === 0 ? (sorted[middle - 1] + sorted[middle]) / 2 : sorted[middle]
  }

  const calculateStdDev = (values: number[], mean: number) => {
    if (values.length <= 1) return 0 // Std dev requires more than 1 point
    const variance = values.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / (values.length - 1) // Use sample variance
    return Math.sqrt(variance)
  }

  const formatNumber = (num: number | string) => {
    if (typeof num === "number" && !isNaN(num)) {
      // Basic check for integer-like numbers
      if (Math.abs(num) < 1e9 && Math.floor(num) === num) {
        return num.toLocaleString() // Format integers without decimals
      }
      return num.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })
    }
    return num
  }

  const formatPercentage = (num: number) => {
    if (typeof num === "number" && !isNaN(num)) {
      return num.toFixed(1) + "%"
    }
    return "-"
  }

  const displayedMissingStats = showAllMissing ? missingStats : missingStats.slice(0, 10)

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Column Summaries</CardTitle>
        </CardHeader>
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
                    <TableCell className="font-medium max-w-[150px] truncate" title={stats.column}>
                      {stats.column}
                    </TableCell>
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

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Frequency Distribution</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="mb-3">
              <Select value={selectedDistColumn} onValueChange={setSelectedDistColumn}>
                <SelectTrigger className="h-9">
                  <SelectValue placeholder="Select Column" />
                </SelectTrigger>
                <SelectContent>
                  {columns.map((column) => (
                    <SelectItem key={`dist-${column}`} value={column}>
                      {column}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="overflow-y-auto max-h-[300px] border rounded-md">
              <Table>
                <TableHeader className="sticky top-0 bg-background z-10">
                  <TableRow>
                    <TableHead>Value</TableHead>
                    <TableHead>Count</TableHead>
                    <TableHead>%</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {frequencyDistribution.length > 0 ? (
                    frequencyDistribution.map((item, index) => (
                      <TableRow key={index}>
                        <TableCell className="max-w-[150px] truncate" title={item.value}>
                          {item.value}
                        </TableCell>
                        <TableCell>{formatNumber(item.count)}</TableCell>
                        <TableCell>{formatPercentage(item.percentage)}</TableCell>
                      </TableRow>
                    ))
                  ) : (
                    <TableRow>
                      <TableCell colSpan={3} className="text-center text-muted-foreground h-24">
                        No data for selected column.
                      </TableCell>
                    </TableRow>
                  )}
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
                  <TableRow>
                    <TableHead>Column</TableHead>
                    <TableHead>Missing #</TableHead>
                    <TableHead>Missing %</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {displayedMissingStats.length > 0 ? (
                    displayedMissingStats.map(
                      (stats) =>
                        stats.missingCount > 0 && (
                          <TableRow key={`missing-${stats.column}`}>
                            <TableCell className="max-w-[150px] truncate" title={stats.column}>
                              {stats.column}
                            </TableCell>
                            <TableCell>{formatNumber(stats.missingCount)}</TableCell>
                            <TableCell>{formatPercentage(stats.missingPercentage)}</TableCell>
                          </TableRow>
                        ),
                    )
                  ) : (
                    <TableRow>
                      <TableCell colSpan={3} className="text-center text-muted-foreground h-24">
                        No missing values found.
                      </TableCell>
                    </TableRow>
                  )}
                </TableBody>
              </Table>
            </div>
            {missingStats.filter((s) => s.missingCount > 0).length > 10 && (
              <Button
                variant="link"
                size="sm"
                onClick={() => setShowAllMissing(!showAllMissing)}
                className="mt-2 p-0 h-auto"
              >
                {showAllMissing
                  ? "Show Top 10 Missing"
                  : `Show All (${missingStats.filter((s) => s.missingCount > 0).length}) Missing`}
              </Button>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
