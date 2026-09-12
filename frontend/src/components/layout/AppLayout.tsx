import React, { useState } from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { Topbar } from './Topbar';

export const AppLayout: React.FC = () => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const location = useLocation();

  // Derive dynamic top bar title from route
  const getPageTitle = () => {
    switch (location.pathname) {
      case '/dashboard':
        return 'Overview Dashboard';
      case '/analyze':
        return 'Real-Time Transaction Analysis';
      case '/transactions':
        return 'Transaction History Ledger';
      case '/model-performance':
        return 'ML Model Performance Analytics';
      case '/about':
        return 'About FraudGuard Project';
      default:
        return 'FraudGuard';
    }
  };

  return (
    <div className="flex h-screen overflow-hidden bg-background text-on-background">
      {/* Desktop Fixed Sidebar */}
      <div className="hidden md:block fixed left-0 top-0 h-full w-60 z-40">
        <Sidebar />
      </div>

      {/* Mobile Drawer Overlay */}
      {mobileOpen && (
        <div
          className="md:hidden fixed inset-0 bg-black/60 backdrop-blur-sm z-50 transition-opacity"
          onClick={() => setMobileOpen(false)}
        />
      )}

      {/* Mobile Slide-out Sidebar */}
      <div
        className={`md:hidden fixed left-0 top-0 h-full w-60 z-50 transform transition-transform duration-300 ${
          mobileOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <Sidebar onCloseMobile={() => setMobileOpen(false)} />
      </div>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col md:ml-60 min-h-screen overflow-hidden">
        <Topbar
          onToggleMobileMenu={() => setMobileOpen((prev) => !prev)}
          title={getPageTitle()}
        />
        <main className="flex-1 overflow-y-auto bg-background">
          <Outlet />
        </main>
      </div>
    </div>
  );
};
