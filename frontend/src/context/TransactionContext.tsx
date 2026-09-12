import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { DashboardStats, Transaction } from '../types';
import { api } from '../services/api';

interface TransactionContextType {
  transactions: Transaction[];
  stats: DashboardStats;
  loading: boolean;
  error: string | null;
  refreshData: () => Promise<void>;
  getTransactionById: (id: string) => Transaction | undefined;
}

const DEFAULT_STATS: DashboardStats = {
  totalTransactions: 0,
  fraudDetected: 0,
  legitimate: 0,
  fraudRate: 0,
  avgFraudProb: 0,
  volumeTrendPercent: 5.2,
  alertsTodayCount: 0,
};

const TransactionContext = createContext<TransactionContextType | undefined>(undefined);

export const TransactionProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [stats, setStats] = useState<DashboardStats>(DEFAULT_STATS);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const refreshData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      // Fetch dashboard aggregated statistics directly from SQLite
      const dashboardData = await api.getDashboardStats();
      setStats({
        totalTransactions: dashboardData.totalTransactions,
        fraudDetected: dashboardData.fraudDetected,
        legitimate: dashboardData.legitimate,
        fraudRate: dashboardData.fraudRate,
        avgFraudProb: dashboardData.avgFraudProb,
        volumeTrendPercent: dashboardData.volumeTrendPercent,
        alertsTodayCount: dashboardData.alertsTodayCount,
      });

      // Fetch transactions list from SQLite
      const txData = await api.getTransactions({ page: 1, limit: 50 });
      setTransactions(txData.transactions);
    } catch (err) {
      console.error('[TransactionContext] Error fetching live backend data:', err);
      setError(err instanceof Error ? err.message : 'Failed to connect to backend server');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refreshData();
  }, [refreshData]);

  const getTransactionById = (id: string): Transaction | undefined => {
    return transactions.find((tx) => tx.id === id || (tx as any).transaction_id === id);
  };

  return (
    <TransactionContext.Provider
      value={{
        transactions,
        stats,
        loading,
        error,
        refreshData,
        getTransactionById,
      }}
    >
      {children}
    </TransactionContext.Provider>
  );
};

export const useTransactions = (): TransactionContextType => {
  const context = useContext(TransactionContext);
  if (!context) {
    throw new Error('useTransactions must be used within a TransactionProvider');
  }
  return context;
};
