import React from 'react';
import { Transaction } from '../../types';
import { RiskBadge, StatusBadge } from '../common/Badge';

interface TransactionTableProps {
  transactions: Transaction[];
  onActionClick?: (transaction: Transaction, action: 'block' | 'review' | 'view') => void;
  showFullActions?: boolean;
}

export const TransactionTable: React.FC<TransactionTableProps> = ({
  transactions,
  onActionClick,
  showFullActions = false,
}) => {
  return (
    <div className="overflow-x-auto w-full">
      <table className="w-full text-left border-collapse">
        <thead>
          <tr className="bg-surface-container-highest/50 border-b border-outline-variant">
            <th className="p-stack-sm px-stack-md text-label-md font-label-md text-on-surface-variant uppercase tracking-wider font-medium">
              ID
            </th>
            <th className="p-stack-sm px-stack-md text-label-md font-label-md text-on-surface-variant uppercase tracking-wider font-medium">
              Date/Time
            </th>
            <th className="p-stack-sm px-stack-md text-label-md font-label-md text-on-surface-variant uppercase tracking-wider font-medium">
              Type
            </th>
            <th className="p-stack-sm px-stack-md text-label-md font-label-md text-on-surface-variant uppercase tracking-wider font-medium text-right">
              Amount
            </th>
            <th className="p-stack-sm px-stack-md text-label-md font-label-md text-on-surface-variant uppercase tracking-wider font-medium">
              Fraud Prob
            </th>
            <th className="p-stack-sm px-stack-md text-label-md font-label-md text-on-surface-variant uppercase tracking-wider font-medium">
              Risk Level
            </th>
            <th className="p-stack-sm px-stack-md text-label-md font-label-md text-on-surface-variant uppercase tracking-wider font-medium">
              Status
            </th>
            <th className="p-stack-sm px-stack-md text-label-md font-label-md text-on-surface-variant uppercase tracking-wider font-medium text-center">
              Action
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-outline-variant/30">
          {transactions.map((tx) => {
            const probColor =
              tx.riskLevel === 'HIGH'
                ? 'text-error'
                : tx.riskLevel === 'MEDIUM'
                ? 'text-tertiary'
                : 'text-secondary';
            const barBg =
              tx.riskLevel === 'HIGH'
                ? 'bg-error'
                : tx.riskLevel === 'MEDIUM'
                ? 'bg-tertiary'
                : 'bg-secondary';

            return (
              <tr
                key={tx.id}
                className={`hover:bg-surface-container-highest/30 transition-colors ${
                  tx.riskLevel === 'HIGH' ? 'bg-error-container/10' : ''
                }`}
              >
                <td className="p-stack-sm px-stack-md text-mono-data font-mono-data text-on-surface font-semibold">
                  {tx.id}
                </td>
                <td className="p-stack-sm px-stack-md text-body-md font-body-md text-on-surface-variant">
                  {tx.dateTime}
                </td>
                <td className="p-stack-sm px-stack-md text-body-md font-body-md text-on-surface">
                  {tx.type}
                </td>
                <td className="p-stack-sm px-stack-md text-mono-data font-mono-data text-on-surface text-right font-medium">
                  ${tx.amount.toLocaleString(undefined, { minimumFractionDigits: 2 })}
                </td>
                <td className="p-stack-sm px-stack-md">
                  <div className="flex items-center gap-2">
                    <span className={`text-mono-data font-mono-data font-semibold ${probColor}`}>
                      {tx.fraudProbability.toFixed(1)}%
                    </span>
                    <div className="w-16 bg-surface-container-highest h-1 rounded-full overflow-hidden">
                      <div
                        className={`${barBg} h-1 rounded-full`}
                        style={{ width: `${Math.min(100, tx.fraudProbability)}%` }}
                      />
                    </div>
                  </div>
                </td>
                <td className="p-stack-sm px-stack-md">
                  <RiskBadge level={tx.riskLevel} />
                </td>
                <td className="p-stack-sm px-stack-md">
                  <StatusBadge status={tx.status} />
                </td>
                <td className="p-stack-sm px-stack-md text-center">
                  {showFullActions ? (
                    <button
                      type="button"
                      onClick={() => onActionClick && onActionClick(tx, 'view')}
                      className="text-primary hover:text-primary-fixed-dim transition-colors p-1 rounded hover:bg-surface-container"
                      title="View Details"
                    >
                      <span className="material-symbols-outlined text-[20px]">visibility</span>
                    </button>
                  ) : tx.status === 'BLOCKED' ? (
                    <button
                      type="button"
                      onClick={() => onActionClick && onActionClick(tx, 'block')}
                      className="px-3 py-1 bg-error text-on-error rounded text-label-md font-label-md hover:bg-error-container transition-colors"
                    >
                      Block
                    </button>
                  ) : tx.status === 'REVIEW' ? (
                    <button
                      type="button"
                      onClick={() => onActionClick && onActionClick(tx, 'review')}
                      className="px-3 py-1 border border-outline-variant text-on-surface rounded text-label-md font-label-md hover:bg-surface-container-highest transition-colors"
                    >
                      Review
                    </button>
                  ) : (
                    <button
                      type="button"
                      disabled
                      className="px-3 py-1 border border-outline-variant/40 text-on-surface-variant/50 rounded text-label-md font-label-md cursor-not-allowed"
                    >
                      Cleared
                    </button>
                  )}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};
