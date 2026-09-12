import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { AnalyzePayload, PredictionResult } from '../types';
import { useTransactions } from '../context/TransactionContext';
import { TransactionForm } from '../components/analysis/TransactionForm';
import { PredictionResultCard } from '../components/analysis/PredictionResultCard';

export const AnalyzePage: React.FC = () => {
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);
  const { refreshData } = useTransactions();
  const navigate = useNavigate();

  const handleAnalyze = async (payload: AnalyzePayload) => {
    setLoading(true);
    setApiError(null);
    try {
      // POST to Flask REST API (/api/predict)
      const res = await api.predict(payload);
      setResult(res);

      // Refresh transactions and dashboard stats from SQLite database
      await refreshData();
    } catch (err) {
      console.error('Prediction analysis failed:', err);
      setApiError(err instanceof Error ? err.message : 'Prediction request failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-container-padding space-y-stack-lg max-w-[1400px] mx-auto w-full">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-outline-variant/30 pb-4">
        <div>
          <h1 className="text-headline-lg font-headline-lg text-on-background mb-1">
            Analyze Transaction
          </h1>
          <p className="text-body-md font-body-md text-on-surface-variant">
            Input transaction parameters to run real-time inference against the saved XGBoost model.
          </p>
        </div>
        <div className="text-label-md font-label-md text-on-surface-variant bg-surface-container px-3 py-1.5 rounded-full border border-outline-variant/50 flex items-center gap-2 shadow-[0_4px_20px_rgba(0,0,0,0.2)] shrink-0">
          <span className="w-2 h-2 rounded-full bg-secondary" />
          Model: XGBoost (Stage 3C Champion)
        </div>
      </div>

      {apiError && (
        <div className="p-4 bg-error-container/20 border border-error/30 rounded-lg text-error flex items-center gap-3">
          <span className="material-symbols-outlined">error</span>
          <div>
            <div className="font-semibold text-sm">Prediction Failed</div>
            <div className="text-xs text-on-surface-variant">{apiError}</div>
          </div>
        </div>
      )}

      {/* Content Grid */}
      <div className="grid grid-cols-12 gap-gutter">
        {/* Form Column */}
        <div className="col-span-12 xl:col-span-7">
          <TransactionForm onAnalyze={handleAnalyze} isLoading={loading} />
        </div>

        {/* Prediction Result Column */}
        <div className="col-span-12 xl:col-span-5">
          <PredictionResultCard
            result={result}
            onReset={() => {
              setResult(null);
              setApiError(null);
            }}
            onViewHistory={() => navigate('/transactions')}
          />
        </div>
      </div>
    </div>
  );
};
