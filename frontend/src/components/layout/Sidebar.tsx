import React from 'react';
import { NavLink } from 'react-router-dom';

interface SidebarProps {
  onCloseMobile?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ onCloseMobile }) => {
  const navItems = [
    {
      label: 'Dashboard',
      path: '/dashboard',
      icon: 'dashboard',
    },
    {
      label: 'Analyze Transaction',
      path: '/analyze',
      icon: 'analytics',
    },
    {
      label: 'Transaction History',
      path: '/transactions',
      icon: 'receipt_long',
    },
    {
      label: 'Model Performance',
      path: '/model-performance',
      icon: 'query_stats',
    },
    {
      label: 'About Project',
      path: '/about',
      icon: 'info',
    },
  ];

  return (
    <aside className="w-60 h-full flex flex-col py-stack-lg px-stack-md bg-surface-container border-r border-outline-variant">
      {/* Brand Header */}
      <div className="mb-stack-lg px-3 flex items-center gap-3">
        <span
          className="material-symbols-outlined text-primary text-3xl"
          style={{ fontVariationSettings: "'FILL' 1" }}
        >
          shield
        </span>
        <div>
          <h1 className="text-headline-md font-headline-md font-black text-primary leading-tight">
            FraudGuard
          </h1>
          <p className="text-label-md font-label-md text-on-surface-variant uppercase tracking-wider">
            ML Monitoring Suite
          </p>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 space-y-1 overflow-y-auto">
        {navItems.map((item) => (
          <NavLink
            key={item.path + item.label}
            to={item.path}
            onClick={onCloseMobile}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-lg text-label-md font-label-md transition-all duration-200 ${
                isActive
                  ? 'bg-secondary-container text-on-secondary-container font-bold translate-x-1 shadow-sm'
                  : 'text-on-surface-variant hover:text-on-surface hover:bg-surface-container-highest'
              }`
            }
          >
            <span className="material-symbols-outlined text-[20px]">{item.icon}</span>
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>

      {/* Footer Status / Profile */}
      <div className="mt-auto pt-4 border-t border-outline-variant/50 flex items-center justify-between px-3">
        <div className="flex items-center gap-2 text-on-surface-variant">
          <span className="material-symbols-outlined text-sm">wifi</span>
          <span className="text-label-md font-label-md">System Online</span>
        </div>
        <span className="w-2 h-2 rounded-full bg-secondary animate-pulse" />
      </div>
    </aside>
  );
};
