import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  title?: string;
  subtitle?: string;
  action?: React.ReactNode;
}

export const Card: React.FC<CardProps> = ({
  children,
  className = '',
  title,
  subtitle,
  action,
}) => {
  return (
    <div
      className={`bg-surface-container border border-outline-variant rounded-xl p-container-padding relative overflow-hidden ${className}`}
    >
      {(title || action) && (
        <div className="flex items-center justify-between mb-stack-md pb-stack-sm border-b border-outline-variant/50">
          <div>
            {title && (
              <h3 className="text-headline-md font-headline-md text-on-surface">{title}</h3>
            )}
            {subtitle && (
              <p className="text-body-md font-body-md text-on-surface-variant mt-0.5">
                {subtitle}
              </p>
            )}
          </div>
          {action && <div>{action}</div>}
        </div>
      )}
      {children}
    </div>
  );
};
