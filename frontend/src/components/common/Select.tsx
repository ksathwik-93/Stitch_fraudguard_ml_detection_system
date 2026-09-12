import React from 'react';

interface SelectOption {
  value: string;
  label: string;
}

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  options: SelectOption[];
  placeholder?: string;
  requiredMark?: boolean;
  error?: string;
}

export const Select: React.FC<SelectProps> = ({
  label,
  options,
  placeholder = 'Select option...',
  requiredMark = false,
  error,
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
      <select
        id={id}
        className={`w-full bg-surface border rounded-lg px-3 py-2.5 text-body-md font-body-md text-on-background focus:ring-2 focus:ring-primary focus:border-transparent outline-none input-ring appearance-none cursor-pointer ${
          error ? 'border-error' : 'border-outline-variant'
        } ${className}`}
        {...props}
      >
        {placeholder && (
          <option value="" disabled>
            {placeholder}
          </option>
        )}
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
      {error && <span className="text-xs text-error mt-0.5">{error}</span>}
    </div>
  );
};
