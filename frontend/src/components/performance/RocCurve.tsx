import React from 'react';

export const RocCurve: React.FC = () => {
  return (
    <div className="bg-surface-container border border-outline-variant rounded-xl flex flex-col overflow-hidden shadow-md h-full">
      <div className="px-4 py-3 border-b border-outline-variant bg-surface-container-low">
        <h3 className="text-headline-md font-headline-md text-on-surface flex items-center gap-2">
          <span className="material-symbols-outlined text-primary">show_chart</span>
          Receiver Operating Characteristic (ROC) Curve
        </h3>
      </div>

      <div className="p-4 flex-1 relative min-h-[260px] flex items-center justify-center bg-surface-container-lowest overflow-hidden">
        {/* Plot area */}
        <div className="absolute inset-6 border-l border-b border-outline-variant flex items-end">
          <div className="w-full h-full relative">
            {/* Grid lines */}
            <div className="absolute bottom-[25%] w-full border-t border-dashed border-outline-variant/30" />
            <div className="absolute bottom-[50%] w-full border-t border-dashed border-outline-variant/30" />
            <div className="absolute bottom-[75%] w-full border-t border-dashed border-outline-variant/30" />
            <div className="absolute left-[25%] h-full border-l border-dashed border-outline-variant/30" />
            <div className="absolute left-[50%] h-full border-l border-dashed border-outline-variant/30" />
            <div className="absolute left-[75%] h-full border-l border-dashed border-outline-variant/30" />

            {/* Random Chance Diagonal Line */}
            <div className="absolute bottom-0 left-0 w-[141%] h-px bg-outline-variant origin-bottom-left -rotate-45 transform" />

            {/* ROC SVG Curves */}
            <svg className="absolute inset-0 w-full h-full overflow-visible" viewBox="0 0 100 100" preserveAspectRatio="none">
              {/* Curve 1: XGBoost / Gradient Boost Candidate */}
              <path
                d="M 0 100 Q 5 10 100 0"
                fill="none"
                stroke="#4edea3"
                strokeWidth="2.5"
                className="drop-shadow-[0_0_4px_rgba(78,222,163,0.5)]"
              />
              {/* Curve 2: Random Forest */}
              <path
                d="M 0 100 Q 15 20 100 5"
                fill="none"
                stroke="#4d8eff"
                strokeWidth="2"
                strokeDasharray="4 2"
              />
            </svg>

            {/* Axis labels */}
            <div className="absolute -left-7 top-1/2 -rotate-90 text-[10px] text-on-surface-variant font-mono-data">
              True Positive Rate
            </div>
            <div className="absolute -bottom-6 left-1/2 -translate-x-1/2 text-[10px] text-on-surface-variant font-mono-data">
              False Positive Rate
            </div>
          </div>
        </div>

        {/* Legend */}
        <div className="absolute bottom-6 right-6 bg-surface/90 backdrop-blur border border-outline-variant rounded p-2 text-[10px] font-mono-data flex flex-col gap-1 z-10">
          <div className="flex items-center gap-2 text-secondary">
            <span className="w-3 h-0.5 bg-secondary" /> XGBoost (AUC: 0.994)
          </div>
          <div className="flex items-center gap-2 text-primary">
            <span className="w-3 h-0.5 bg-primary border-t border-dashed border-primary" /> R.Forest (AUC: 0.978)
          </div>
          <div className="flex items-center gap-2 text-outline-variant">
            <span className="w-3 h-0.5 bg-outline-variant" /> Random Chance (AUC: 0.500)
          </div>
        </div>
      </div>
    </div>
  );
};
