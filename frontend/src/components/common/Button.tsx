import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  icon?: string;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  isLoading = false,
  icon,
  className = '',
  disabled,
  ...props
}) => {
  const baseStyles =
    'font-label-md text-label-md rounded-lg transition-colors flex items-center justify-center gap-2 outline-none focus:ring-2 focus:ring-primary/50';

  const sizeStyles = {
    sm: 'px-3 py-1.5 text-xs',
    md: 'px-4 py-2.5',
    lg: 'px-6 py-3 text-sm',
  };

  const variantStyles = {
    primary:
      'bg-primary hover:bg-primary-container text-on-primary font-bold shadow-[0_0_15px_rgba(77,142,255,0.15)]',
    secondary:
      'bg-surface-container-highest hover:bg-surface-bright text-on-surface border border-outline-variant',
    danger:
      'bg-error hover:bg-error-container text-on-error font-bold shadow-[0_0_15px_rgba(255,180,171,0.1)]',
    outline:
      'bg-transparent border border-outline text-on-surface hover:bg-surface-container-high',
    ghost:
      'bg-transparent text-primary hover:text-primary-container hover:bg-surface-container/50',
  };

  return (
    <button
      className={`${baseStyles} ${sizeStyles[size]} ${variantStyles[variant]} ${
        disabled || isLoading ? 'opacity-70 cursor-not-allowed' : ''
      } ${className}`}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? (
        <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
      ) : (
        icon && <span className="material-symbols-outlined text-[18px]">{icon}</span>
      )}
      <span>{children}</span>
    </button>
  );
};
