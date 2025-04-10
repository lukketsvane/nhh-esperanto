"use client"

import { useState, useEffect, useRef, useMemo } from "react"
import Chart from "chart.js/auto"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Button } from "@/components/ui/button"
import { BarChart, LineChart, PieChart, Download } from "lucide-react"

interface DataVisualizerProps {
  data: any[]
  columns: string[]
}

export default function DataVisualizer({ data, columns }: DataVisualizerProps) {
  const [chartType, setChartType] = useState("bar")
  const [xAxis, setXAxis] = useState("")
  const [yAxis, setYAxis] = useState("")
  const [groupBy, setGroupBy] = useState("none")
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const chartInstanceRef = useRef<Chart | null>(null)

  const { numericalColumns, categoricalColumns } = useMemo(() => {
    const numerical: string[] = []
    const categorical: string[] = []

    columns.forEach((column) => {
      if (!column) return
      const values = data.map((row) => row[column]).filter((v) => v !== undefined && v !== null && v !== "")
      if (values.length === 0) return

      const numericCount = values.reduce((count, val) => {
        const isPotentiallyNumeric = val === "" || !isNaN(Number(val))
        return count + (isPotentiallyNumeric && String(val).trim() !== "" && !isNaN(Number(val)) ? 1 : 0)
      }, 0)

      const uniqueValues = new Set(values)

      if (numericCount / values.length > 0.8 && uniqueValues.size > 5) {
        numerical.push(column)
      } else if (uniqueValues.size <= 50 && uniqueValues.size > 1) {
        categorical.push(column)
      }
    })
    return { numericalColumns: numerical.sort(), categoricalColumns: categorical.sort() }
  }, [data, columns])

  useEffect(() => {
    if (!xAxis && categoricalColumns.length > 0) {
      const defaultX =
        ["treatment_clean", "gender", "faculty", "yearincollege", "ai_assist", "ai_guided", "control"].find((c) =>
          categoricalColumns.includes(c),
        ) || categoricalColumns[0]
      setXAxis(defaultX)
    } else if (!xAxis && columns.length > 0) {
      setXAxis(columns[0])
    }

    if (!yAxis && numericalColumns.length > 0) {
      const defaultY =
        ["testscore", "ConversationDurationMinutes", "MessageCount", "age", "gpa"].find((c) =>
          numericalColumns.includes(c),
        ) || numericalColumns[0]
      setYAxis(defaultY)
    } else if (!yAxis && columns.length > 1) {
      setYAxis(
        columns.find((c) => c !== xAxis && numericalColumns.includes(c)) ||
          columns.find((c) => c !== xAxis) ||
          columns[1],
      )
    }
  }, [columns, numericalColumns, categoricalColumns, xAxis, yAxis])

  useEffect(() => {
    if (!canvasRef.current || !xAxis || !yAxis || data.length === 0 || !chartType || !Chart) return

    const ctx = canvasRef.current.getContext("2d")
    if (!ctx) return

    if (chartInstanceRef.current) {
      chartInstanceRef.current.destroy()
      chartInstanceRef.current = null
    }

    let labels: string[] = []
    let datasets: any[] = []
    const aggregate = (items: any[]) => {
      if (items.length === 0) return 0
      const sum = items.reduce((acc, item) => {
        const value = Number.parseFloat(item[yAxis])
        return acc + (isNaN(value) ? 0 : value)
      }, 0)
      return sum / items.length
    }
    const uniqueXValues = [...new Set(data.map((item) => String(item[xAxis] ?? "N/A")))].sort((a, b) =>
      a.localeCompare(b, undefined, { numeric: true, sensitivity: "base" }),
    )
    labels = uniqueXValues
    const colors = ["#3b82f6", "#ef4444", "#10b981", "#f59e0b", "#8b5cf6", "#ec4899", "#06b6d4", "#f97316"]

    if (groupBy && groupBy !== "none" && groupBy !== xAxis) {
      const uniqueGroupValues = [...new Set(data.map((item) => String(item[groupBy] ?? "N/A")))].sort((a, b) =>
        a.localeCompare(b, undefined, { numeric: true, sensitivity: "base" }),
      )
      datasets = uniqueGroupValues.map((groupValue, groupIndex) => {
        const groupData = data.filter((item) => String(item[groupBy] ?? "N/A") === groupValue)
        const values = uniqueXValues.map((xValue) => {
          const matchingItems = groupData.filter((item) => String(item[xAxis] ?? "N/A") === xValue)
          return aggregate(matchingItems)
        })
        return {
          label: groupValue,
          data: values,
          backgroundColor: colors[groupIndex % colors.length] + (chartType === "bar" ? "BF" : ""),
          borderColor: colors[groupIndex % colors.length],
          borderWidth: chartType === "line" ? 2 : 1,
          fill: chartType === "line" ? false : undefined,
          tension: chartType === "line" ? 0.1 : undefined,
        }
      })
    } else {
      const values = uniqueXValues.map((xValue) => {
        const matchingItems = data.filter((item) => String(item[xAxis] ?? "N/A") === xValue)
        return aggregate(matchingItems)
      })
      datasets = [
        {
          label: yAxis,
          data: values,
          backgroundColor:
            chartType === "pie"
              ? uniqueXValues.map((_, i) => colors[i % colors.length] + "BF")
              : colors[0] + (chartType === "bar" ? "BF" : ""),
          borderColor: chartType === "pie" ? uniqueXValues.map((_, i) => colors[i % colors.length]) : colors[0],
          borderWidth: chartType === "line" ? 2 : 1,
          fill: chartType === "line" ? false : undefined,
          tension: chartType === "line" ? 0.1 : undefined,
        },
      ]
    }

    const chartConfig: any = {
      type: chartType as Chart.ChartType,
      data: { labels, datasets },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales:
          chartType !== "pie"
            ? {
                y: {
                  beginAtZero: true,
                  title: { display: true, text: yAxis },
                },
                x: {
                  title: { display: true, text: xAxis },
                },
              }
            : undefined,
        plugins: {
          legend: {
            display: (groupBy && groupBy !== "none" && groupBy !== xAxis && datasets.length > 1) || chartType === "pie",
            position: "top",
          },
          title: {
            display: true,
            text: `Avg ${yAxis} by ${xAxis}${groupBy && groupBy !== "none" && groupBy !== xAxis ? ` (Grouped by ${groupBy})` : ""}`,
          },
          tooltip: {
            callbacks: {
              label: (context: any) => {
                let label = context.dataset.label || ""
                if (label) {
                  label += ": "
                }
                if (context.parsed.y !== null && context.parsed.y !== undefined) {
                  label += Number(context.parsed.y).toLocaleString(undefined, { maximumFractionDigits: 2 })
                } else if (chartType === "pie" && context.parsed !== null && context.parsed !== undefined) {
                  label += Number(context.parsed).toLocaleString(undefined, { maximumFractionDigits: 2 })
                }
                return label
              },
            },
          },
        },
      },
    }

    if (chartType === "pie") {
      delete chartConfig.options.scales
      if (datasets.length > 1) {
        // Cannot render multi-dataset pie chart, potentially show error or disable pie for grouped data
        console.warn("Pie chart selected with grouped data, only showing first group.")
        chartConfig.data.datasets = [datasets[0]] // Show only first group's data
        chartConfig.options.plugins.title.text = `Avg ${yAxis} by ${xAxis} (Group: ${datasets[0].label})`
      } else if (datasets.length === 1) {
        chartConfig.options.plugins.title.text = `${yAxis} Distribution by ${xAxis}`
      }
    }

    chartInstanceRef.current = new Chart(ctx, chartConfig)

    return () => {
      if (chartInstanceRef.current) {
        chartInstanceRef.current.destroy()
        chartInstanceRef.current = null
      }
    }
  }, [data, xAxis, yAxis, groupBy, chartType, numericalColumns, categoricalColumns])

  const downloadChart = () => {
    if (!canvasRef.current) return
    const link = document.createElement("a")
    link.download = `chart-${chartType}-${yAxis}-by-${xAxis}${groupBy && groupBy !== "none" ? `-grouped-${groupBy}` : ""}.png`
    link.href = canvasRef.current.toDataURL("image/png", 1.0)
    link.click()
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">Data Visualization</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3 mb-4 items-end">
          <div>
            <label className="block text-xs font-medium mb-1 text-muted-foreground">Chart Type</label>
            <Select value={chartType} onValueChange={setChartType}>
              <SelectTrigger className="h-9">
                <SelectValue placeholder="Chart Type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="bar">
                  <div className="flex items-center gap-2">
                    <BarChart className="h-4 w-4" />
                    Bar
                  </div>
                </SelectItem>
                <SelectItem value="line">
                  <div className="flex items-center gap-2">
                    <LineChart className="h-4 w-4" />
                    Line
                  </div>
                </SelectItem>
                <SelectItem value="pie" disabled={groupBy && groupBy !== "none"}>
                  <div className="flex items-center gap-2">
                    <PieChart className="h-4 w-4" />
                    Pie
                  </div>
                </SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div>
            <label className="block text-xs font-medium mb-1 text-muted-foreground">X-Axis (Category)</label>
            <Select value={xAxis} onValueChange={setXAxis}>
              <SelectTrigger className="h-9">
                <SelectValue placeholder="Select X-Axis" />
              </SelectTrigger>
              <SelectContent>
                {categoricalColumns.map((column) => (
                  <SelectItem key={`x-${column}`} value={column}>
                    {column}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div>
            <label className="block text-xs font-medium mb-1 text-muted-foreground">Y-Axis (Value - Averaged)</label>
            <Select value={yAxis} onValueChange={setYAxis}>
              <SelectTrigger className="h-9">
                <SelectValue placeholder="Select Y-Axis" />
              </SelectTrigger>
              <SelectContent>
                {numericalColumns.map((column) => (
                  <SelectItem key={`y-${column}`} value={column}>
                    {column}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div>
            <label className="block text-xs font-medium mb-1 text-muted-foreground">Group By</label>
            <Select
              value={groupBy}
              onValueChange={(value) => {
                setGroupBy(value)
                if (value !== "none" && chartType === "pie") setChartType("bar")
              }}
            >
              <SelectTrigger className="h-9">
                <SelectValue placeholder="Group By (Optional)" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="none">No Grouping</SelectItem>
                {categoricalColumns
                  .filter((col) => col !== xAxis)
                  .map((column) => (
                    <SelectItem key={`group-${column}`} value={column}>
                      {column}
                    </SelectItem>
                  ))}
              </SelectContent>
            </Select>
          </div>
        </div>

        <div className="flex justify-end mb-2">
          <Button variant="outline" size="sm" onClick={downloadChart} className="flex items-center gap-2 h-9">
            <Download className="h-4 w-4" />
            Download Chart
          </Button>
        </div>

        <div className="border rounded-lg p-4 bg-background aspect-video relative min-h-[350px]">
          <canvas ref={canvasRef}></canvas>
        </div>
      </CardContent>
    </Card>
  )
}
