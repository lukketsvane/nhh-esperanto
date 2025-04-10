"use client"

import type React from "react"

import { useState, useMemo, useEffect } from "react"
import Papa from "papaparse"
import { Loader2, Download, Search, BarChart, TableIcon, AreaChart } from "lucide-react"

import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

import DataTable from "@/components/data-table"
import DataVisualizer from "@/components/data-visualizer"
import DataSummary from "@/components/data-summary"

type DataRow = Record<string, any>

interface DataExplorerProps {
  initialData: DataRow[]
  initialColumns: string[]
}

export default function DataExplorer({ initialData, initialColumns }: DataExplorerProps) {
  const rawData = useMemo(() => initialData, [initialData])
  const allColumns = useMemo(() => initialColumns, [initialColumns])

  const [loading, setLoading] = useState(!initialData || initialData.length === 0)
  const [searchTerm, setSearchTerm] = useState("")
  const [filters, setFilters] = useState<Record<string, string>>({})
  const [selectedColumns, setSelectedColumns] = useState<string[]>(() => {
    const defaultCols = [
      "final_id",
      "treatment_clean",
      "gender",
      "highgpa",
      "testscore",
      "ConversationDurationMinutes",
      "MessageCount",
      "index_confidence",
      "index_motivation",
    ]
    // Ensure default columns actually exist in the data
    const validDefaultCols = defaultCols.filter((col) => allColumns.includes(col))
    // If none of the preferred defaults exist, fall back to first 10
    return validDefaultCols.length > 0 ? validDefaultCols : allColumns.slice(0, 10)
  })
  const [pagination, setPagination] = useState({ currentPage: 1, itemsPerPage: 25 })
  const [activeTab, setActiveTab] = useState("table")

  useEffect(() => {
    if (initialData && initialData.length > 0) {
      setLoading(false)
      setSelectedColumns((prev) => {
        const validCols = prev.filter((col) => initialColumns.includes(col))
        if (validCols.length === 0 && initialColumns.length > 0) {
          const defaultCols = [
            "final_id",
            "treatment_clean",
            "gender",
            "highgpa",
            "testscore",
            "ConversationDurationMinutes",
            "MessageCount",
            "index_confidence",
            "index_motivation",
          ]
          const validDefaultCols = defaultCols.filter((col) => initialColumns.includes(col))
          return validDefaultCols.length > 0 ? validDefaultCols : initialColumns.slice(0, 10)
        }
        return validCols
      })
    }
  }, [initialData, initialColumns])

  const filteredData = useMemo(() => {
    let filtered = rawData

    if (searchTerm) {
      const lowerSearchTerm = searchTerm.toLowerCase()
      filtered = filtered.filter((row) =>
        allColumns.some(
          (col) =>
            row[col] !== null && row[col] !== undefined && String(row[col]).toLowerCase().includes(lowerSearchTerm),
        ),
      )
    }

    const activeFilters = Object.entries(filters).filter(([_, value]) => value)
    if (activeFilters.length > 0) {
      filtered = filtered.filter((row) =>
        activeFilters.every(([column, filterValue]) => {
          const lowerFilterValue = filterValue.toLowerCase()
          return (
            row[column] !== null &&
            row[column] !== undefined &&
            String(row[column]).toLowerCase().includes(lowerFilterValue)
          )
        }),
      )
    }

    return filtered
  }, [rawData, searchTerm, filters, allColumns])

  const paginatedData = useMemo(() => {
    const startIndex = (pagination.currentPage - 1) * pagination.itemsPerPage
    return filteredData.slice(startIndex, startIndex + pagination.itemsPerPage)
  }, [filteredData, pagination.currentPage, pagination.itemsPerPage])

  const totalPages = Math.ceil(filteredData.length / pagination.itemsPerPage)

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value)
    setPagination((p) => ({ ...p, currentPage: 1 }))
  }

  const handleFilterChange = (column: string, value: string) => {
    setFilters((prev) => ({ ...prev, [column]: value }))
    setPagination((p) => ({ ...p, currentPage: 1 }))
  }

  const handleColumnToggle = (column: string) => {
    setSelectedColumns((prev) => (prev.includes(column) ? prev.filter((col) => col !== column) : [...prev, column]))
  }

  const handlePageChange = (page: number) => {
    if (page >= 1 && page <= totalPages) {
      setPagination((p) => ({ ...p, currentPage: page }))
    }
  }

  const handleItemsPerPageChange = (value: string) => {
    setPagination({ currentPage: 1, itemsPerPage: Number.parseInt(value) })
  }

  const exportCSV = () => {
    const dataToExport = filteredData.map((row) => {
      const newRow: Record<string, any> = {}
      selectedColumns.forEach((col) => {
        newRow[col] = row[col] ?? ""
      })
      return newRow
    })

    if (dataToExport.length === 0) {
      alert("No data to export based on current filters.")
      return
    }

    const csvString = Papa.unparse(dataToExport, {
      columns: selectedColumns,
      header: true,
      quotes: true,
      quoteChar: '"',
      escapeChar: '"',
      delimiter: ",",
      newline: "\r\n",
    })

    const blob = new Blob([csvString], { type: "text/csv;charset=utf-8;" })
    const url = URL.createObjectURL(blob)
    const link = document.createElement("a")
    link.setAttribute("href", url)
    link.setAttribute("download", "data_export.csv")
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  }

  const renderPaginationItems = () => {
    const items = []
    const maxPagesToShow = 5
    const halfMaxPages = Math.floor(maxPagesToShow / 2)

    let startPageNum = 1
    let endPageNum = totalPages

    if (totalPages > maxPagesToShow + 2) {
      if (pagination.currentPage <= halfMaxPages + 1) {
        endPageNum = maxPagesToShow + 1
      } else if (pagination.currentPage >= totalPages - halfMaxPages) {
        startPageNum = totalPages - maxPagesToShow
      } else {
        startPageNum = pagination.currentPage - halfMaxPages
        endPageNum = pagination.currentPage + halfMaxPages
      }
    }

    // Always show first page
    if (startPageNum > 1) {
      items.push(
        <PaginationItem key={1}>
          <PaginationLink onClick={() => handlePageChange(1)} className="cursor-pointer">
            1
          </PaginationLink>
        </PaginationItem>,
      )
      if (startPageNum > 2) {
        items.push(
          <PaginationItem key="start-ellipsis">
            <PaginationEllipsis />
          </PaginationItem>,
        )
      }
    }

    // Render page numbers
    for (let i = startPageNum; i <= endPageNum; i++) {
      items.push(
        <PaginationItem key={i}>
          <PaginationLink
            isActive={pagination.currentPage === i}
            onClick={() => handlePageChange(i)}
            className="cursor-pointer"
          >
            {i}
          </PaginationLink>
        </PaginationItem>,
      )
    }

    // Always show last page
    if (endPageNum < totalPages) {
      if (endPageNum < totalPages - 1) {
        items.push(
          <PaginationItem key="end-ellipsis">
            <PaginationEllipsis />
          </PaginationItem>,
        )
      }
      items.push(
        <PaginationItem key={totalPages}>
          <PaginationLink onClick={() => handlePageChange(totalPages)} className="cursor-pointer">
            {totalPages}
          </PaginationLink>
        </PaginationItem>,
      )
    }

    return items
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <Loader2 className="h-8 w-8 animate-spin text-primary mr-2" />
        <span>Loading data...</span>
      </div>
    )
  }

  if (!initialData || initialData.length === 0) {
    return (
      <div className="p-8 text-center text-destructive">
        Failed to load or parse data. Please check the data source and format.
      </div>
    )
  }

  return (
    <div className="p-4 md:p-6 space-y-4">
      <div className="flex flex-col md:flex-row gap-2 md:items-center">
        <div className="relative flex-1">
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input placeholder="Search data..." value={searchTerm} onChange={handleSearchChange} className="pl-8 h-9" />
        </div>
        <div className="flex gap-2 flex-shrink-0">
          <Select value={pagination.itemsPerPage.toString()} onValueChange={handleItemsPerPageChange}>
            <SelectTrigger className="w-[130px] h-9 text-xs">
              <SelectValue placeholder="Rows per page" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="10">10 rows</SelectItem>
              <SelectItem value="25">25 rows</SelectItem>
              <SelectItem value="50">50 rows</SelectItem>
              <SelectItem value="100">100 rows</SelectItem>
            </SelectContent>
          </Select>
          <Button variant="outline" size="sm" onClick={exportCSV} className="h-9">
            <Download className="h-4 w-4 mr-2" />
            Export CSV
          </Button>
        </div>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="table" className="flex items-center gap-2">
            <TableIcon className="h-4 w-4" /> Table
          </TabsTrigger>
          <TabsTrigger value="visualize" className="flex items-center gap-2">
            <AreaChart className="h-4 w-4" /> Visualize
          </TabsTrigger>
          <TabsTrigger value="summary" className="flex items-center gap-2">
            <BarChart className="h-4 w-4" /> Summary
          </TabsTrigger>
        </TabsList>

        <TabsContent value="table" className="mt-0">
          <Card>
            <CardContent className="p-0 pt-4">
              <DataTable
                data={paginatedData}
                columns={selectedColumns}
                allColumns={allColumns}
                filters={filters}
                onFilterChange={handleFilterChange}
                setFilters={setFilters}
                selectedColumns={selectedColumns}
                onColumnToggle={handleColumnToggle}
              />
            </CardContent>
            {totalPages > 0 && (
              <div className="flex items-center justify-between p-4 border-t">
                <div className="text-xs text-muted-foreground">
                  Showing {filteredData.length > 0 ? (pagination.currentPage - 1) * pagination.itemsPerPage + 1 : 0} to{" "}
                  {Math.min(pagination.currentPage * pagination.itemsPerPage, filteredData.length)} of{" "}
                  {filteredData.length} results
                </div>
                <Pagination>
                  <PaginationContent>
                    <PaginationItem>
                      <PaginationPrevious
                        onClick={() => handlePageChange(pagination.currentPage - 1)}
                        className={
                          pagination.currentPage === 1
                            ? "pointer-events-none opacity-50 cursor-not-allowed"
                            : "cursor-pointer"
                        }
                        aria-disabled={pagination.currentPage === 1}
                      />
                    </PaginationItem>
                    {renderPaginationItems()}
                    <PaginationItem>
                      <PaginationNext
                        onClick={() => handlePageChange(pagination.currentPage + 1)}
                        className={
                          pagination.currentPage === totalPages
                            ? "pointer-events-none opacity-50 cursor-not-allowed"
                            : "cursor-pointer"
                        }
                        aria-disabled={pagination.currentPage === totalPages}
                      />
                    </PaginationItem>
                  </PaginationContent>
                </Pagination>
              </div>
            )}
          </Card>
        </TabsContent>

        <TabsContent value="visualize" className="mt-4">
          <DataVisualizer data={filteredData} columns={allColumns} />
        </TabsContent>

        <TabsContent value="summary" className="mt-4">
          <DataSummary data={rawData} columns={allColumns} />
        </TabsContent>
      </Tabs>
    </div>
  )
}
