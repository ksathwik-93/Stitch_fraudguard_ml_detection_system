import React from 'react';

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  label?: string;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = 'md',
  label = 'Loading...',
}) => {
  const dimensions = {
    sm: 'w-4 h-4 border-2',
    md: 'w-8 h-8 border-3',
    lg: 'w-12 h-12 border-4',
  };

  return (
    <div className="flex flex-col items-center justify-center p-6 gap-3 text-on-surface-variant">
      <div
        className={`${dimensions[size]} border-outline-variant border-t-primary rounded-full animate-spin`}
      />
      {label && <span className="text-label-md font-label-md">{label}</span>}
    </div>
  );
};
