import React from 'react';
import { PredictionResult } from '../../types';
import { Button } from '../common/Button';

interface PredictionResultCardProps {
  result: PredictionResult | null;
  onReset?: () => void;
  onViewHistory?: () => void;
}

export const PredictionResultCard: React.FC<PredictionResultCardProps> = ({
  result,
  onReset,
  onViewHistory,
}) => {
  if (!result) {
    return (
      <div className="bg-surface-variant border border-outline-variant border-dashed rounded-xl p-container-padding h-full min-h-[400px] flex flex-col items-center justify-center text-center gap-4">
        <span className="material-symbols-outlined text-outline-variant text-[48px]">
          troubleshoot
        </span>
        <div>
          <h3 className="text-headline-md font-headline-md text-on-surface-variant">
            Awaiting Data
          </h3>
          <p className="text-body-md font-body-md text-outline mt-1 max-w-xs">
            Enter transaction details and run analysis to view ML prediction results and risk scoring.
          </p>
        </div>
      </div>
    );
  }

  const isFraud = result.prediction === 'FRAUD';

  return (
    <div
      className={`bg-surface-variant border rounded-xl p-container-padding h-full flex flex-col relative overflow-hidden shadow-lg ${
        isFraud ? 'border-error/30' : 'border-secondary/30'
      }`}
    >
      {/* Ambient Glow */}
      <div
        className={`absolute top-0 left-0 w-full h-1 bg-gradient-to-r ${
          isFraud
            ? 'from-error/0 via-error to-error/0'
            : 'from-secondary/0 via-secondary to-secondary/0'
        }`}
      />
      <div
        className={`absolute -top-24 -right-24 w-64 h-64 rounded-full blur-3xl pointer-events-none ${
          isFraud ? 'bg-error/10' : 'bg-secondary/10'
        }`}
      />

      {/* Header */}
      <div className="flex items-center justify-between mb-stack-md pb-stack-sm border-b border-outline-variant/50 z-10 relative">
        <h2 className="text-headline-md font-headline-md text-on-background">
          Prediction Result
        </h2>
        <span className="text-label-md font-label-md text-on-surface-variant bg-surface-container px-2.5 py-1 rounded font-mono-data">
          ID: {result.transactionId}
        </span>
      </div>

      {/* Center Content */}
      <div className="flex-1 flex flex-col items-center justify-center text-center gap-stack-md z-10 relative py-stack-md">
        {/* Status Badge */}
        <div
          className={`font-label-md text-label-md rounded-full px-4 py-1.5 flex items-center gap-2 border ${
            isFraud
              ? 'bg-error-container text-on-error-container border-error/20'
              : 'bg-secondary-container/20 text-secondary border-secondary/30'
          }`}
        >
          <span
            className={`w-2 h-2 rounded-full ${
              isFraud ? 'bg-error animate-pulse' : 'bg-secondary'
            }`}
          />
          {isFraud ? 'FRAUD DETECTED' : 'LEGITIMATE TRANSACTION'}
        </div>

        {/* Probability Score */}
        <div>
          <div
            className={`text-display font-display leading-none mb-1 ${
              isFraud ? 'text-error' : 'text-secondary'
            }`}
          >
            {result.fraudProbability.toFixed(1)}%
          </div>
          <div className="text-label-md font-label-md text-on-surface-variant uppercase tracking-widest">
            Fraud Probability
          </div>
        </div>

        {/* Risk Level Bar */}
        <div className="w-full max-w-xs bg-surface-container rounded-full h-2 mt-2 mb-1 overflow-hidden flex">
          <div
            className={`h-full w-1/3 ${
              result.riskLevel === 'LOW' ? 'bg-secondary shadow-[0_0_10px_rgba(78,222,163,0.8)]' : 'bg-secondary/20'
            }`}
          />
          <div
            className={`h-full w-1/3 ${
              result.riskLevel === 'MEDIUM' ? 'bg-tertiary shadow-[0_0_10px_rgba(255,179,173,0.8)]' : 'bg-tertiary-container/20'
            }`}
          />
          <div
            className={`h-full w-1/3 ${
              result.riskLevel === 'HIGH' ? 'bg-error shadow-[0_0_10px_rgba(255,180,171,0.8)]' : 'bg-error/20'
            }`}
          />
        </div>
        <div className="w-full max-w-xs flex justify-between text-[10px] font-label-md text-outline uppercase tracking-wider">
          <span className={result.riskLevel === 'LOW' ? 'text-secondary font-bold' : ''}>Low</span>
          <span className={result.riskLevel === 'MEDIUM' ? 'text-tertiary font-bold' : ''}>Med</span>
          <span className={result.riskLevel === 'HIGH' ? 'text-error font-bold' : ''}>High</span>
        </div>

        {/* Recommendation Box */}
        <div className="mt-4 p-4 bg-surface-container-low border border-outline-variant rounded-lg w-full text-left flex gap-3">
          <span
            className={`material-symbols-outlined shrink-0 mt-0.5 ${
              isFraud ? 'text-tertiary-container' : 'text-secondary'
            }`}
          >
            {isFraud ? 'warning' : 'check_circle'}
          </span>
          <div>
            <h4 className="text-body-md font-body-md font-semibold text-on-surface">
              Recommendation
            </h4>
            <p className="text-body-md font-body-md text-on-surface-variant mt-1">
              {result.recommendation}
            </p>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="mt-auto pt-stack-sm border-t border-outline-variant/50 flex flex-col sm:flex-row gap-3 z-10 relative">
        <Button variant="secondary" className="flex-1" onClick={onReset}>
          Analyze Another
        </Button>
        <Button variant="primary" className="flex-1" onClick={onViewHistory}>
          View Transaction History
        </Button>
      </div>
    </div>
  );
};
