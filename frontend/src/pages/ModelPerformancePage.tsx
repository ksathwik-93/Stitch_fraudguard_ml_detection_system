import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { ConfusionMatrixData, FeatureImportance, ModelMetrics } from '../types';
import { ModelMetricsTable } from '../components/performance/ModelMetricsTable';
import { FeatureImportanceChart } from '../components/performance/FeatureImportanceChart';
import { ConfusionMatrix } from '../components/performance/ConfusionMatrix';
import { RocCurve } from '../components/performance/RocCurve';
import { LoadingSpinner } from '../components/common/LoadingSpinner';

export const ModelPerformancePage: React.FC = () => {
  const [metrics, setMetrics] = useState<ModelMetrics[]>([]);
  const [featureImportance, setFeatureImportance] = useState<FeatureImportance[]>([]);
  const [confusionMatrix, setConfusionMatrix] = useState<ConfusionMatrixData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const data = await api.getModelPerformance();
        setMetrics(data.metrics);
        setFeatureImportance(data.featureImportance);
        setConfusionMatrix(data.confusionMatrix);
      } catch (err) {
        console.error('Failed to load model performance data:', err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  if (loading || !confusionMatrix) {
    return (
      <div className="h-full flex items-center justify-center p-12">
        <LoadingSpinner label="Loading model benchmarks & metrics..." size="lg" />
      </div>
    );
  }

  return (
    <div className="p-container-padding space-y-stack-lg max-w-7xl mx-auto w-full">
      {/* Page Header */}
      <div className="flex flex-col gap-2 border-b border-outline-variant/30 pb-4">
        <div className="flex justify-between items-center">
          <h1 className="text-headline-lg font-headline-lg text-on-surface font-semibold">
            Model Performance Overview
          </h1>
          <span className="px-3 py-1 rounded text-label-md font-label-md text-on-surface-variant border border-outline-variant bg-surface-container-high/50 font-mono-data">
            Benchmark / Demo Data
          </span>
        </div>
        <p className="text-body-lg font-body-lg text-on-surface-variant max-w-3xl">
          Comparative evaluation of candidate machine learning algorithms evaluated on synthetic transaction datasets. Note: Final champion model will be selected after full backend training execution.
        </p>
      </div>

      {/* Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-gutter">
        {/* Evaluation Metrics Table */}
        <div className="col-span-1 lg:col-span-8">
          <ModelMetricsTable metrics={metrics} />
        </div>

        {/* Feature Importance Bar */}
        <div className="col-span-1 lg:col-span-4">
          <FeatureImportanceChart data={featureImportance} />
        </div>

        {/* Confusion Matrix */}
        <div className="col-span-1 lg:col-span-6">
          <ConfusionMatrix data={confusionMatrix} />
        </div>

        {/* ROC Curve Chart */}
        <div className="col-span-1 lg:col-span-6">
          <RocCurve />
        </div>
      </div>
    </div>
  );
};
