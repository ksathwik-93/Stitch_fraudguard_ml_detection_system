import React from 'react';
import { RiskLevel, TransactionStatus } from '../../types';

interface RiskBadgeProps {
  level: RiskLevel;
}

export const RiskBadge: React.FC<RiskBadgeProps> = ({ level }) => {
  const styles = {
    HIGH: {
      bg: 'bg-error/10 text-error border-error/30',
      dot: 'bg-error',
      text: 'High',
    },
    MEDIUM: {
      bg: 'bg-tertiary/10 text-tertiary border-tertiary/30',
      dot: 'bg-tertiary',
      text: 'Medium',
    },
    LOW: {
      bg: 'bg-secondary/10 text-secondary border-secondary/30',
      dot: 'bg-secondary',
      text: 'Low',
    },
  };

  const current = styles[level] || styles.LOW;

  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded border text-label-md font-label-md font-medium ${current.bg}`}
    >
      <span className={`w-1.5 h-1.5 rounded-full ${current.dot}`} />
      {current.text}
    </span>
  );
};

interface StatusBadgeProps {
  status: TransactionStatus;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status }) => {
  const styles = {
    BLOCKED: 'text-error font-semibold',
    REVIEW: 'text-tertiary font-semibold',
    CLEARED: 'text-on-surface-variant',
  };

  return <span className={`font-body-md ${styles[status] || ''}`}>{status}</span>;
};
