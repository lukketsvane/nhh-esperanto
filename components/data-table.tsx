"use client"

import type React from "react"

import { useState } from "react"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Filter, Columns } from "lucide-react"

interface DataTableProps {
  data: any[]
  columns: string[]
  allColumns: string[]
  filters: Record<string, string>
  onFilterChange: (column: string, value: string) => void
  setFilters: React.Dispatch<React.SetStateAction<Record<string, string>>>
  selectedColumns: string[]
  onColumnToggle: (column: string) => void
}

export default function DataTable({
  data,
  columns,
  allColumns,
  filters,
  onFilterChange,
  setFilters,
  selectedColumns,
  onColumnToggle,
}: DataTableProps) {
  const [showFilters, setShowFilters] = useState(false)

  const clearFilters = () => {
    setFilters({})
    setShowFilters(false)
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-2 gap-2">
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

        <div className="flex items-center gap-1">
          <Button
            variant="outline"
            onClick={() => setShowFilters(!showFilters)}
            className="flex items-center gap-1 text-sm h-9"
          >
            <Filter className="h-4 w-4" />
            {showFilters ? "Hide Filters" : "Show Filters"}
          </Button>
          {showFilters && Object.values(filters).some((val) => val) && (
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
                  {column}
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
                <TableRow key={rowIndex}>
                  {columns.map((column) => (
                    <TableCell key={`${rowIndex}-${column}`} className="whitespace-nowrap px-3 py-1.5 text-sm">
                      <span title={String(row[column] ?? "")}>
                        {String(row[column] ?? "").length > 100
                          ? String(row[column]).substring(0, 100) + "..."
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
  )
}
