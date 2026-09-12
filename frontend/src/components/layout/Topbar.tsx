import React from 'react';

interface TopbarProps {
  onToggleMobileMenu?: () => void;
  title?: string;
}

export const Topbar: React.FC<TopbarProps> = ({ onToggleMobileMenu, title }) => {
  return (
    <header className="sticky top-0 z-30 flex justify-between items-center w-full px-container-padding h-16 bg-surface/90 backdrop-blur-md border-b border-outline-variant/50">
      {/* Left side / Mobile Menu Toggle */}
      <div className="flex items-center gap-3">
        <button
          type="button"
          onClick={onToggleMobileMenu}
          className="md:hidden text-on-surface-variant hover:text-primary transition-colors p-1"
          aria-label="Toggle Navigation Menu"
        >
          <span className="material-symbols-outlined">menu</span>
        </button>

        {/* Mobile Brand */}
        <div className="md:hidden flex items-center gap-2">
          <span
            className="material-symbols-outlined text-primary text-2xl"
            style={{ fontVariationSettings: "'FILL' 1" }}
          >
            shield
          </span>
          <span className="text-headline-md font-headline-md font-bold text-primary">
            FraudGuard
          </span>
        </div>

        {/* Desktop Title / Context */}
        {title && (
          <h2 className="hidden md:block text-headline-md font-headline-md font-semibold text-on-surface">
            {title}
          </h2>
        )}
      </div>

      {/* Right side Actions */}
      <div className="flex items-center gap-3 text-on-surface-variant">
        <span className="hidden sm:inline-block px-3 py-1 rounded text-label-md font-label-md text-on-surface-variant border border-outline-variant bg-surface-container-high/50">
          Academic Simulator Mode
        </span>
      </div>
    </header>
  );
};
