import React from 'react';
import { FeatureImportance } from '../../types';

interface FeatureImportanceChartProps {
  data: FeatureImportance[];
}

export const FeatureImportanceChart: React.FC<FeatureImportanceChartProps> = ({ data }) => {
  const maxVal = Math.max(...data.map((d) => d.importance), 0.001);

  const colors = ['bg-secondary', 'bg-primary', 'bg-primary-container', 'bg-outline'];
  const textColors = ['text-secondary', 'text-primary', 'text-primary-container', 'text-outline'];

  return (
    <div className="bg-surface-container border border-outline-variant rounded-xl flex flex-col overflow-hidden shadow-md h-full">
      <div className="px-4 py-3 border-b border-outline-variant bg-surface-container-low">
        <h3 className="text-headline-md font-headline-md text-on-surface flex items-center gap-2">
          <span className="material-symbols-outlined text-secondary">bar_chart</span>
          Top Predictors (Feature Importance)
        </h3>
      </div>

      <div className="p-4 flex-1 flex flex-col justify-center gap-4">
        {data.map((item, idx) => {
          const widthPct = Math.round((item.importance / maxVal) * 85);
          const barColor = colors[idx % colors.length];
          const textColor = textColors[idx % textColors.length];

          return (
            <div key={item.feature} className="flex flex-col gap-1">
              <div className="flex justify-between text-label-md font-label-md">
                <span className="text-on-surface font-mono-data">{item.feature}</span>
                <span className={textColor}>{item.importance.toFixed(3)}</span>
              </div>
              <div className="h-2 w-full bg-surface-container-highest rounded-full overflow-hidden">
                <div
                  className={`h-full ${barColor} rounded-full transition-all duration-1000`}
                  style={{ width: `${widthPct}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
