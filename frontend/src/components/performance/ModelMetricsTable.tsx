import React from 'react';
import { ModelMetrics } from '../../types';

interface ModelMetricsTableProps {
  metrics: ModelMetrics[];
}

export const ModelMetricsTable: React.FC<ModelMetricsTableProps> = ({ metrics }) => {
  return (
    <div className="bg-surface-container border border-outline-variant rounded-xl flex flex-col overflow-hidden shadow-md">
      <div className="px-4 py-3 border-b border-outline-variant bg-surface-container-low flex justify-between items-center">
        <h3 className="text-headline-md font-headline-md text-on-surface flex items-center gap-2">
          <span className="material-symbols-outlined text-primary">table_chart</span>
          Algorithm Evaluation Metrics (Demo Benchmarks)
        </h3>
        <span className="text-xs font-mono-data text-on-surface-variant bg-surface-container-highest px-2.5 py-1 rounded">
          Sample Metrics
        </span>
      </div>

      <div className="p-4 overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-surface-container-highest text-on-surface-variant text-label-md font-label-md uppercase tracking-wider">
              <th className="py-3 px-4 font-medium rounded-tl">Model</th>
              <th className="py-3 px-4 font-medium text-right">Accuracy</th>
              <th className="py-3 px-4 font-medium text-right">Precision</th>
              <th className="py-3 px-4 font-medium text-right">Recall</th>
              <th className="py-3 px-4 font-medium text-right">F1-Score</th>
              <th className="py-3 px-4 font-medium text-right rounded-tr">ROC-AUC</th>
            </tr>
          </thead>
          <tbody className="text-body-md font-body-md text-on-surface font-mono-data divide-y divide-outline-variant/50">
            {metrics.map((m) => (
              <tr
                key={m.modelName}
                className={`hover:bg-surface-container-high transition-colors ${
                  m.isChampion ? 'bg-secondary-container/5 border-l-2 border-secondary' : ''
                }`}
              >
                <td className="py-3 px-4 flex items-center gap-2 font-sans font-medium">
                  <span
                    className={`w-2 h-2 rounded-full ${
                      m.isChampion
                        ? 'bg-secondary shadow-[0_0_8px_rgba(78,222,163,0.6)]'
                        : m.modelName.includes('Random Forest')
                        ? 'bg-primary-container'
                        : 'bg-outline'
                    }`}
                  />
                  <span className={m.isChampion ? 'text-secondary' : 'text-on-surface'}>
                    {m.modelName}
                  </span>
                  {m.tag && (
                    <span className="text-xs font-label-md text-on-surface-variant bg-surface-container-highest px-2 py-0.5 rounded ml-1">
                      {m.tag}
                    </span>
                  )}
                </td>
                <td className={`py-3 px-4 text-right ${m.isChampion ? 'text-secondary' : ''}`}>
                  {m.accuracy.toFixed(3)}
                </td>
                <td className={`py-3 px-4 text-right ${m.isChampion ? 'text-secondary' : ''}`}>
                  {m.precision.toFixed(3)}
                </td>
                <td className={`py-3 px-4 text-right ${m.isChampion ? 'text-secondary' : ''}`}>
                  {m.recall.toFixed(3)}
                </td>
                <td className={`py-3 px-4 text-right ${m.isChampion ? 'text-secondary' : ''}`}>
                  {m.f1Score.toFixed(3)}
                </td>
                <td className={`py-3 px-4 text-right ${m.isChampion ? 'text-secondary' : ''}`}>
                  {m.rocAuc.toFixed(3)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
