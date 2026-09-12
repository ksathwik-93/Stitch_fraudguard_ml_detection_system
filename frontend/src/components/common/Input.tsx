import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  prefixSymbol?: string;
  mono?: boolean;
  requiredMark?: boolean;
}

export const Input: React.FC<InputProps> = ({
  label,
  error,
  prefixSymbol,
  mono = false,
  requiredMark = false,
  className = '',
  id,
  ...props
}) => {
  return (
    <div className="flex flex-col gap-1 w-full">
      {label && (
        <label
          htmlFor={id}
          className="text-label-md font-label-md text-on-surface-variant uppercase tracking-wider flex justify-between"
        >
          <span>
            {label} {requiredMark && <span className="text-error">*</span>}
          </span>
        </label>
      )}
      <div className="relative w-full">
        {prefixSymbol && (
          <span className="absolute left-3 top-1/2 -translate-y-1/2 text-outline font-mono-data text-sm">
            {prefixSymbol}
          </span>
        )}
        <input
          id={id}
          className={`w-full bg-surface border rounded-lg py-2.5 px-3 text-on-background focus:ring-2 focus:ring-primary focus:border-transparent outline-none input-ring ${
            mono ? 'font-mono-data text-mono-data' : 'font-body-md text-body-md'
          } ${prefixSymbol ? 'pl-7' : ''} ${
            error ? 'border-error' : 'border-outline-variant'
          } ${className}`}
          {...props}
        />
      </div>
      {error && <span className="text-xs text-error mt-0.5">{error}</span>}
    </div>
  );
};
