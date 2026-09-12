import React from 'react';
import { ConfusionMatrixData } from '../../types';

interface ConfusionMatrixProps {
  data: ConfusionMatrixData;
}

export const ConfusionMatrix: React.FC<ConfusionMatrixProps> = ({ data }) => {
  return (
    <div className="bg-surface-container border border-outline-variant rounded-xl flex flex-col overflow-hidden shadow-md h-full">
      <div className="px-4 py-3 border-b border-outline-variant bg-surface-container-low">
        <h3 className="text-headline-md font-headline-md text-on-surface flex items-center gap-2">
          <span className="material-symbols-outlined text-primary">grid_4x4</span>
          Confusion Matrix (Test Set Evaluation)
        </h3>
      </div>

      <div className="p-6 flex-1 flex items-center justify-center">
        <div className="grid grid-cols-[auto_1fr] gap-4 w-full max-w-md">
          {/* Y-axis Label */}
          <div className="flex items-center justify-center -rotate-90 text-label-md font-label-md text-on-surface-variant tracking-widest whitespace-nowrap">
            ACTUAL CLASS
          </div>

          <div className="flex flex-col gap-2 w-full">
            {/* Matrix Header */}
            <div className="grid grid-cols-2 gap-2 text-center text-label-md font-label-md text-on-surface-variant pl-8">
              <div>Pred Negative (Legit)</div>
              <div>Pred Positive (Fraud)</div>
            </div>

            {/* Row 1: Actual Negative */}
            <div className="grid grid-cols-[auto_1fr_1fr] gap-2 items-center">
              <div className="text-right text-label-md font-label-md text-on-surface-variant pr-2 w-8">
                Legit
              </div>
              <div className="bg-surface-container-highest border border-outline-variant/30 rounded p-4 text-center flex flex-col justify-center min-h-[80px]">
                <span className="text-headline-md font-headline-md text-on-surface font-mono-data font-semibold">
                  {data.trueNegatives.toLocaleString()}
                </span>
                <span className="text-label-md font-label-md text-outline">True Negatives</span>
              </div>
              <div className="bg-error-container/20 border border-error/30 rounded p-4 text-center flex flex-col justify-center min-h-[80px]">
                <span className="text-headline-md font-headline-md text-error font-mono-data font-semibold">
                  {data.falsePositives.toLocaleString()}
                </span>
                <span className="text-label-md font-label-md text-error">False Positives</span>
              </div>
            </div>

            {/* Row 2: Actual Positive */}
            <div className="grid grid-cols-[auto_1fr_1fr] gap-2 items-center">
              <div className="text-right text-label-md font-label-md text-on-surface-variant pr-2 w-8">
                Fraud
              </div>
              <div className="bg-tertiary-container/20 border border-tertiary/30 rounded p-4 text-center flex flex-col justify-center min-h-[80px]">
                <span className="text-headline-md font-headline-md text-tertiary font-mono-data font-semibold">
                  {data.falseNegatives.toLocaleString()}
                </span>
                <span className="text-label-md font-label-md text-tertiary">False Negatives</span>
              </div>
              <div className="bg-secondary-container/20 border border-secondary/50 rounded p-4 text-center flex flex-col justify-center min-h-[80px]">
                <span className="text-headline-md font-headline-md text-secondary font-mono-data font-semibold">
                  {data.truePositives.toLocaleString()}
                </span>
                <span className="text-label-md font-label-md text-secondary">True Positives</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
