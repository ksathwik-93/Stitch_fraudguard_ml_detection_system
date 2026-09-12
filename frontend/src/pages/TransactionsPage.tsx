import React, { useState } from 'react';
import { RiskLevel, TransactionStatus } from '../types';
import { useTransactions } from '../context/TransactionContext';
import { TransactionTable } from '../components/dashboard/TransactionTable';

export const TransactionsPage: React.FC = () => {
  const { transactions } = useTransactions();

  // Filters state
  const [search, setSearch] = useState('');
  const [typeFilter, setTypeFilter] = useState('');
  const [riskFilter, setRiskFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [dateFilter, setDateFilter] = useState('');

  const handleReset = () => {
    setSearch('');
    setTypeFilter('');
    setRiskFilter('');
    setStatusFilter('');
    setDateFilter('');
  };

  const handleExportCSV = () => {
    const headers = ['ID', 'Date/Time', 'Type', 'Amount', 'Fraud Probability', 'Risk Level', 'Status'];
    const rows = filteredTransactions.map((tx) => [
      tx.id,
      tx.dateTime,
      tx.type,
      tx.amount,
      `${tx.fraudProbability}%`,
      tx.riskLevel,
      tx.status,
    ]);
    const csvContent =
      'data:text/csv;charset=utf-8,' +
      [headers.join(','), ...rows.map((r) => r.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `fraudguard_transactions_${Date.now()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Filter logic
  const filteredTransactions = transactions.filter((tx) => {
    if (search && !tx.id.toLowerCase().includes(search.toLowerCase())) return false;
    if (typeFilter && tx.type.toUpperCase() !== typeFilter.toUpperCase()) return false;
    if (riskFilter && tx.riskLevel !== (riskFilter as RiskLevel)) return false;
    if (statusFilter && tx.status !== (statusFilter as TransactionStatus)) return false;
    return true;
  });

  return (
    <div className="p-container-padding space-y-stack-lg max-w-[1600px] mx-auto w-full">
      {/* Page Header */}
      <div className="flex flex-col gap-1">
        <h2 className="font-display text-display text-on-surface">Transaction History</h2>
        <p className="font-body-lg text-on-surface-variant">
          Search, filter, and review all processed payment transactions across the system.
        </p>
      </div>

      {/* Filter Bar */}
      <div className="bg-surface-container-high border border-outline-variant rounded-lg p-stack-md shadow-md">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-gutter items-end">
          {/* Search */}
          <div className="flex flex-col gap-2 lg:col-span-1">
            <label className="font-display text-label-md text-on-surface-variant uppercase">
              Search
            </label>
            <div className="relative">
              <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant text-sm">
                search
              </span>
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="ID or Account"
                className="w-full bg-surface-dim border border-outline-variant rounded-md py-2 pl-9 pr-3 text-on-surface font-mono-data focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-all placeholder:font-body-md placeholder:text-on-surface-variant"
              />
            </div>
          </div>

          {/* Type */}
          <div className="flex flex-col gap-2">
            <label className="font-display text-label-md text-on-surface-variant uppercase">
              Type
            </label>
            <select
              value={typeFilter}
              onChange={(e) => setTypeFilter(e.target.value)}
              className="w-full bg-surface-dim border border-outline-variant rounded-md py-2 px-3 text-on-surface font-body-md focus:ring-2 focus:ring-primary focus:border-primary outline-none appearance-none cursor-pointer"
            >
              <option value="">All Types</option>
              <option value="TRANSFER">Transfer</option>
              <option value="CASH_OUT">Cash Out</option>
              <option value="PAYMENT">Payment</option>
              <option value="DEBIT">Debit</option>
              <option value="CASH_IN">Cash In</option>
            </select>
          </div>

          {/* Risk Level */}
          <div className="flex flex-col gap-2">
            <label className="font-display text-label-md text-on-surface-variant uppercase">
              Risk Level
            </label>
            <select
              value={riskFilter}
              onChange={(e) => setRiskFilter(e.target.value)}
              className="w-full bg-surface-dim border border-outline-variant rounded-md py-2 px-3 text-on-surface font-body-md focus:ring-2 focus:ring-primary focus:border-primary outline-none appearance-none cursor-pointer"
            >
              <option value="">All Risks</option>
              <option value="HIGH">High</option>
              <option value="MEDIUM">Medium</option>
              <option value="LOW">Low</option>
            </select>
          </div>

          {/* Status */}
          <div className="flex flex-col gap-2">
            <label className="font-display text-label-md text-on-surface-variant uppercase">
              Status
            </label>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="w-full bg-surface-dim border border-outline-variant rounded-md py-2 px-3 text-on-surface font-body-md focus:ring-2 focus:ring-primary focus:border-primary outline-none appearance-none cursor-pointer"
            >
              <option value="">All Statuses</option>
              <option value="CLEARED">Cleared</option>
              <option value="REVIEW">Review</option>
              <option value="BLOCKED">Blocked</option>
            </select>
          </div>

          {/* Date */}
          <div className="flex flex-col gap-2">
            <label className="font-display text-label-md text-on-surface-variant uppercase">
              Date Filter
            </label>
            <input
              type="date"
              value={dateFilter}
              onChange={(e) => setDateFilter(e.target.value)}
              className="w-full bg-surface-dim border border-outline-variant rounded-md py-2 px-3 text-on-surface font-mono-data focus:ring-2 focus:ring-primary focus:border-primary outline-none [color-scheme:dark]"
            />
          </div>
        </div>

        {/* Filter Action Buttons */}
        <div className="mt-stack-md pt-stack-md border-t border-outline-variant flex justify-between items-center">
          <button
            type="button"
            onClick={handleReset}
            className="text-on-surface-variant hover:text-on-surface font-display text-label-md uppercase tracking-wider transition-colors flex items-center gap-2"
          >
            <span className="material-symbols-outlined text-[18px]">restart_alt</span>
            Reset Filters
          </button>
          <div className="flex gap-3">
            <button
              type="button"
              onClick={handleExportCSV}
              className="bg-transparent border border-outline-variant text-on-surface hover:bg-surface-bright font-display text-label-md px-4 py-2 rounded-md transition-colors flex items-center gap-2"
            >
              <span className="material-symbols-outlined text-[18px]">download</span>
              Export CSV
            </button>
          </div>
        </div>
      </div>

      {/* Data Table Card */}
      <div className="bg-surface-container-high border border-outline-variant rounded-lg flex flex-col shadow-md overflow-hidden">
        <TransactionTable transactions={filteredTransactions} showFullActions />

        {/* Pagination Controls */}
        <div className="border-t border-outline-variant p-4 flex flex-col sm:flex-row justify-between items-center gap-4 bg-surface-container">
          <span className="font-body-md text-on-surface-variant">
            Showing {filteredTransactions.length > 0 ? 1 : 0}-{filteredTransactions.length} of {transactions.length} transactions
          </span>
          <div className="flex items-center gap-2">
            <button
              type="button"
              disabled
              className="p-1.5 rounded border border-outline-variant text-on-surface-variant opacity-50 cursor-not-allowed"
            >
              <span className="material-symbols-outlined text-[20px]">chevron_left</span>
            </button>
            <div className="flex items-center gap-1">
              <button
                type="button"
                className="w-8 h-8 flex items-center justify-center rounded bg-primary-container text-on-primary-container font-mono-data font-semibold text-xs"
              >
                1
              </button>
            </div>
            <button
              type="button"
              disabled
              className="p-1.5 rounded border border-outline-variant text-on-surface-variant opacity-50 cursor-not-allowed"
            >
              <span className="material-symbols-outlined text-[20px]">chevron_right</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
