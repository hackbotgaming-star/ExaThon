import React, { useState, useEffect } from 'react';
import {
  Database,
  Search,
  Upload,
  RefreshCw,
  FileSpreadsheet,
  AlertCircle,
  CheckCircle2,
  ChevronLeft,
  ChevronRight,
  Filter
} from 'lucide-react';
import { GlassCard } from '../components/GlassCard';
import { DatasetSummary, DatasetSchemaColumn } from '../types';
import {
  fetchDatasets,
  fetchDatasetSchema,
  fetchDatasetPreview,
  uploadDataset,
  resetSampleData
} from '../services/api';

export const DataExplorer: React.FC = () => {
  const [datasets, setDatasets] = useState<DatasetSummary[]>([]);
  const [selectedTable, setSelectedTable] = useState<string>('deliveries');
  const [schema, setSchema] = useState<DatasetSchemaColumn[]>([]);
  const [previewData, setPreviewData] = useState<any[]>([]);
  const [columns, setColumns] = useState<string[]>([]);
  const [page, setPage] = useState<number>(1);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [totalRows, setTotalRows] = useState<number>(0);
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<'preview' | 'schema' | 'upload'>('preview');

  // Upload state
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState<boolean>(false);

  useEffect(() => {
    loadDatasetList();
  }, []);

  useEffect(() => {
    if (selectedTable) {
      loadTableData(selectedTable, page, searchQuery);
    }
  }, [selectedTable, page]);

  const loadDatasetList = async () => {
    try {
      const res = await fetchDatasets();
      setDatasets(res.datasets);
      if (res.datasets.length > 0 && !selectedTable) {
        setSelectedTable(res.datasets[0].table_name);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const loadTableData = async (table: string, currentPage: number, search?: string) => {
    setIsLoading(true);
    try {
      const [schemaRes, previewRes] = await Promise.all([
        fetchDatasetSchema(table),
        fetchDatasetPreview(table, currentPage, 15, search)
      ]);
      setSchema(schemaRes.schema);
      setPreviewData(previewRes.data);
      setColumns(previewRes.columns);
      setTotalPages(previewRes.total_pages);
      setTotalRows(previewRes.total_rows);
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(1);
    loadTableData(selectedTable, 1, searchQuery);
  };

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!uploadFile) return;

    setIsUploading(true);
    setUploadStatus(null);
    try {
      const res = await uploadDataset(uploadFile);
      setUploadStatus(`Success: ${res.rows_imported} rows ingested into table '${res.table_name}'.`);
      setUploadFile(null);
      await loadDatasetList();
      setSelectedTable(res.table_name);
      setActiveTab('preview');
    } catch (err: any) {
      setUploadStatus(`Error: ${err.message}`);
    } finally {
      setIsUploading(false);
    }
  };

  const handleReset = async () => {
    if (!window.confirm("Reload synthetic operational datasets into the analytical database?")) return;
    setIsLoading(true);
    try {
      await resetSampleData();
      await loadDatasetList();
      loadTableData(selectedTable, 1);
    } finally {
      setIsLoading(false);
    }
  };

  const currentSummary = datasets.find(d => d.table_name === selectedTable);

  return (
    <div className="space-y-6">
      {/* Header and Dataset Selector */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-extrabold text-navy-900 tracking-tight">
            Data Explorer &amp; Quality Profiler
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Inspect relational operational tables, examine data quality schemas, and validate CSV uploads.
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={handleReset}
            className="flex items-center space-x-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 shadow-xs transition-colors"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Reset Sample Data</span>
          </button>
          <button
            onClick={() => setActiveTab('upload')}
            className="flex items-center space-x-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg bg-lavender-600 text-white hover:bg-lavender-700 shadow-sm transition-colors"
          >
            <Upload className="w-3.5 h-3.5" />
            <span>Upload CSV</span>
          </button>
        </div>
      </div>

      {/* Table Selection Pills */}
      <div className="flex items-center space-x-2 overflow-x-auto pb-1 scrollbar-none">
        {datasets.map((d) => (
          <button
            key={d.table_name}
            onClick={() => {
              setSelectedTable(d.table_name);
              setPage(1);
              setSearchQuery('');
            }}
            className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all shrink-0 flex items-center space-x-2 border ${
              selectedTable === d.table_name
                ? 'bg-navy-900 text-white border-navy-900 shadow-xs'
                : 'bg-white text-slate-600 border-slate-200/80 hover:bg-slate-50'
            }`}
          >
            <FileSpreadsheet className="w-3.5 h-3.5" />
            <span>{d.table_name}</span>
            <span className={`text-[10px] px-1.5 py-0.2 rounded-md ${
              selectedTable === d.table_name ? 'bg-navy-800 text-slate-200' : 'bg-slate-100 text-slate-500'
            }`}>
              {d.row_count.toLocaleString()}
            </span>
          </button>
        ))}
      </div>

      {/* Table Quality & Metadata Summary Bar */}
      {currentSummary && (
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
          <div className="p-3 rounded-xl bg-white border border-slate-200/70 shadow-xs">
            <span className="text-[10px] uppercase font-bold text-slate-400">Total Rows</span>
            <div className="text-sm font-extrabold text-navy-900 mt-0.5">
              {currentSummary.row_count.toLocaleString()}
            </div>
          </div>
          <div className="p-3 rounded-xl bg-white border border-slate-200/70 shadow-xs">
            <span className="text-[10px] uppercase font-bold text-slate-400">Columns</span>
            <div className="text-sm font-extrabold text-navy-900 mt-0.5">
              {currentSummary.column_count} fields
            </div>
          </div>
          <div className="p-3 rounded-xl bg-white border border-slate-200/70 shadow-xs">
            <span className="text-[10px] uppercase font-bold text-slate-400">Missing Values</span>
            <div className={`text-sm font-extrabold mt-0.5 ${currentSummary.missing_percentage > 0 ? 'text-amber-600' : 'text-emerald-600'}`}>
              {currentSummary.missing_percentage}% ({currentSummary.missing_values_count})
            </div>
          </div>
          <div className="p-3 rounded-xl bg-white border border-slate-200/70 shadow-xs">
            <span className="text-[10px] uppercase font-bold text-slate-400">Memory Footprint</span>
            <div className="text-sm font-extrabold text-navy-900 mt-0.5">
              {currentSummary.memory_usage_kb} KB
            </div>
          </div>
          <div className="p-3 rounded-xl bg-white border border-slate-200/70 shadow-xs">
            <span className="text-[10px] uppercase font-bold text-slate-400">Date Span</span>
            <div className="text-xs font-semibold text-slate-700 mt-0.5 truncate" title={currentSummary.date_range}>
              {currentSummary.date_range}
            </div>
          </div>
        </div>
      )}

      {/* Navigation Tabs (Preview vs Schema vs Upload) */}
      <div className="border-b border-slate-200 flex space-x-6">
        <button
          onClick={() => setActiveTab('preview')}
          className={`pb-2.5 text-xs font-bold transition-colors border-b-2 ${
            activeTab === 'preview'
              ? 'border-lavender-600 text-lavender-600'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          Data Records Preview ({totalRows.toLocaleString()})
        </button>
        <button
          onClick={() => setActiveTab('schema')}
          className={`pb-2.5 text-xs font-bold transition-colors border-b-2 ${
            activeTab === 'schema'
              ? 'border-lavender-600 text-lavender-600'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          Schema &amp; Field Types ({schema.length} fields)
        </button>
        <button
          onClick={() => setActiveTab('upload')}
          className={`pb-2.5 text-xs font-bold transition-colors border-b-2 ${
            activeTab === 'upload'
              ? 'border-lavender-600 text-lavender-600'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          CSV Ingestion &amp; Validation
        </button>
      </div>

      {/* Tab 1: Record Preview */}
      {activeTab === 'preview' && (
        <GlassCard>
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
            <form onSubmit={handleSearch} className="relative flex-1 max-w-sm">
              <Search className="w-4 h-4 absolute left-3 top-2.5 text-slate-400" />
              <input
                type="text"
                placeholder={`Search in ${selectedTable}...`}
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-9 pr-3 py-1.5 text-xs rounded-xl bg-slate-50 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-lavender-500/20 focus:border-lavender-500"
              />
            </form>

            {/* Pagination Controls */}
            <div className="flex items-center space-x-2 text-xs text-slate-600">
              <span>Page <strong>{page}</strong> of <strong>{totalPages}</strong></span>
              <button
                disabled={page <= 1}
                onClick={() => setPage(p => Math.max(1, p - 1))}
                className="p-1.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 disabled:opacity-40"
              >
                <ChevronLeft className="w-3.5 h-3.5" />
              </button>
              <button
                disabled={page >= totalPages}
                onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                className="p-1.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 disabled:opacity-40"
              >
                <ChevronRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          {/* Table Container */}
          <div className="overflow-x-auto custom-scrollbar border border-slate-200/80 rounded-xl">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50/90 text-navy-900 border-b border-slate-200 font-bold uppercase tracking-wider text-[10px]">
                <tr>
                  {columns.map((c) => (
                    <th key={c} className="px-3 py-2.5 whitespace-nowrap">
                      {c}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 bg-white/70">
                {isLoading ? (
                  <tr>
                    <td colSpan={columns.length || 1} className="p-8 text-center text-slate-400">
                      Loading records...
                    </td>
                  </tr>
                ) : previewData.length === 0 ? (
                  <tr>
                    <td colSpan={columns.length || 1} className="p-8 text-center text-slate-400">
                      No matching records found.
                    </td>
                  </tr>
                ) : (
                  previewData.map((row, idx) => (
                    <tr key={idx} className="hover:bg-slate-50/60 transition-colors">
                      {columns.map((col) => (
                        <td key={col} className="px-3 py-2 whitespace-nowrap text-slate-700 font-mono text-[11px]">
                          {String(row[col] ?? '')}
                        </td>
                      ))}
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </GlassCard>
      )}

      {/* Tab 2: Schema Explorer */}
      {activeTab === 'schema' && (
        <GlassCard title={`Field Schema: ${selectedTable}`} subtitle="Relational column specifications and null distributions">
          <div className="overflow-x-auto border border-slate-200/80 rounded-xl">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-navy-900 border-b border-slate-200 font-bold text-[10px] uppercase">
                <tr>
                  <th className="px-4 py-2.5">Field Name</th>
                  <th className="px-4 py-2.5">Data Type</th>
                  <th className="px-4 py-2.5">Null Count</th>
                  <th className="px-4 py-2.5">Missing %</th>
                  <th className="px-4 py-2.5">Distinct Values</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 bg-white">
                {schema.map((col) => (
                  <tr key={col.column_name} className="hover:bg-slate-50/60">
                    <td className="px-4 py-2.5 font-bold text-navy-900 font-mono">{col.column_name}</td>
                    <td className="px-4 py-2.5 text-lavender-700 font-mono text-[11px]">{col.data_type}</td>
                    <td className="px-4 py-2.5 text-slate-600">{col.null_count}</td>
                    <td className="px-4 py-2.5">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-semibold ${
                        col.null_percentage > 0 ? 'bg-amber-100 text-amber-800' : 'bg-emerald-50 text-emerald-700'
                      }`}>
                        {col.null_percentage}%
                      </span>
                    </td>
                    <td className="px-4 py-2.5 text-slate-600">{col.unique_values.toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </GlassCard>
      )}

      {/* Tab 3: CSV Upload */}
      {activeTab === 'upload' && (
        <GlassCard title="CSV Dataset Ingestion" subtitle="Validate and import custom operational datasets">
          <form onSubmit={handleUpload} className="max-w-xl space-y-4">
            <div className="border-2 border-dashed border-slate-200 rounded-2xl p-6 text-center hover:border-lavender-400 transition-colors bg-slate-50/50">
              <Upload className="w-8 h-8 text-lavender-600 mx-auto mb-2" />
              <p className="text-xs font-semibold text-navy-900">
                Upload CSV File
              </p>
              <p className="text-[11px] text-slate-500 mt-1">
                Supported formats: standard comma-separated CSV (max 25MB). Content is validated without executing code or SQL.
              </p>
              <input
                type="file"
                accept=".csv"
                onChange={(e) => setUploadFile(e.target.files?.[0] || null)}
                className="mt-4 text-xs text-slate-600 file:mr-3 file:py-1.5 file:px-3 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-lavender-50 file:text-lavender-700 hover:file:bg-lavender-100 cursor-pointer"
              />
            </div>

            {uploadFile && (
              <div className="p-3 rounded-xl bg-slate-100 text-xs text-slate-700 flex items-center justify-between">
                <span>Selected: <strong>{uploadFile.name}</strong> ({(uploadFile.size / 1024).toFixed(1)} KB)</span>
              </div>
            )}

            {uploadStatus && (
              <div className={`p-3 rounded-xl text-xs font-medium flex items-center space-x-2 ${
                uploadStatus.startsWith('Success')
                  ? 'bg-emerald-50 text-emerald-800 border border-emerald-200'
                  : 'bg-red-50 text-red-800 border border-red-200'
              }`}>
                {uploadStatus.startsWith('Success') ? <CheckCircle2 className="w-4 h-4 text-emerald-600" /> : <AlertCircle className="w-4 h-4 text-red-600" />}
                <span>{uploadStatus}</span>
              </div>
            )}

            <button
              type="submit"
              disabled={!uploadFile || isUploading}
              className="px-4 py-2 rounded-xl text-xs font-bold bg-navy-900 text-white hover:bg-navy-800 disabled:opacity-40 transition-all shadow-sm"
            >
              {isUploading ? "Validating & Ingesting..." : "Validate & Import Dataset"}
            </button>
          </form>
        </GlassCard>
      )}
    </div>
  );
};
