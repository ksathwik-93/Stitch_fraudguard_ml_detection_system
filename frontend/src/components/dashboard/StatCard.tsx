import React from 'react';

interface StatCardProps {
  label: string;
  value: string | number;
  subtext?: string;
  icon: string;
  iconColor?: string;
  trendText?: string;
  trendIcon?: string;
  trendColor?: string;
  progressBarWidth?: string;
}

export const StatCard: React.FC<StatCardProps> = ({
  label,
  value,
  subtext,
  icon,
  iconColor = 'text-primary',
  trendText,
  trendIcon,
  trendColor = 'text-secondary',
  progressBarWidth,
}) => {
  return (
    <div className="bg-surface-container border border-outline-variant rounded-xl p-stack-md flex flex-col justify-between hover:border-outline transition-colors relative overflow-hidden group">
      <div className="flex justify-between items-start mb-stack-sm">
        <span className="text-label-md font-label-md text-on-surface-variant uppercase tracking-wider">
          {label}
        </span>
        <span className={`material-symbols-outlined ${iconColor} text-[20px]`}>{icon}</span>
      </div>

      <div className="flex items-baseline gap-stack-sm">
        <span className="text-display font-display text-on-surface">{value}</span>
      </div>

      {trendText && (
        <div className={`text-label-md font-label-md ${trendColor} mt-2 flex items-center gap-1`}>
          {trendIcon && (
            <span className="material-symbols-outlined text-[14px]">{trendIcon}</span>
          )}
          {trendText}
        </div>
      )}

      {progressBarWidth && (
        <div className="w-full bg-surface-container-highest rounded-full h-1.5 mt-3">
          <div
            className="bg-secondary h-1.5 rounded-full"
            style={{ width: progressBarWidth }}
          />
        </div>
      )}

      {subtext && !trendText && !progressBarWidth && (
        <div className="text-label-md font-label-md text-on-surface-variant mt-2 flex items-center gap-1">
          {subtext}
        </div>
      )}
    </div>
  );
};
