import React from 'react';
import { Link } from 'react-router-dom';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';
import { Line, Doughnut } from 'react-chartjs-2';
import { useTransactions } from '../context/TransactionContext';
import { StatCard } from '../components/dashboard/StatCard';
import { TransactionTable } from '../components/dashboard/TransactionTable';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

export const DashboardPage: React.FC = () => {
  const { transactions, stats } = useTransactions();

  const highRiskCount = transactions.filter((t) => t.riskLevel === 'HIGH').length;
  const mediumRiskCount = transactions.filter((t) => t.riskLevel === 'MEDIUM').length;
  const lowRiskCount = transactions.filter((t) => t.riskLevel === 'LOW').length;

  // Chart 1: Line/Area chart data
  const mainChartData = {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    datasets: [
      {
        label: 'Total Volume',
        data: [1200, 1900, 1500, 2200, 1800, 2800, transactions.length * 100 || 2400],
        borderColor: '#adc6ff',
        backgroundColor: 'rgba(173, 198, 255, 0.15)',
        borderWidth: 2,
        pointBackgroundColor: '#2d3449',
        pointBorderColor: '#adc6ff',
        pointRadius: 4,
        fill: true,
        tension: 0.4,
      },
      {
        label: 'Fraud Alerts',
        data: [30, 45, 25, 60, 40, 85, stats.fraudDetected || 55],
        borderColor: '#ffb4ab',
        backgroundColor: 'rgba(255, 180, 171, 0.2)',
        borderWidth: 2,
        pointBackgroundColor: '#2d3449',
        pointBorderColor: '#ffb4ab',
        pointRadius: 4,
        fill: true,
        tension: 0.4,
        yAxisID: 'y1',
      },
    ],
  };

  const mainChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: '#171f33',
        titleColor: '#dae2fd',
        bodyColor: '#c2c6d6',
        borderColor: '#424754',
        borderWidth: 1,
        padding: 12,
      },
    },
    scales: {
      x: {
        grid: { display: false },
        ticks: { color: '#c2c6d6', font: { family: 'Geist' } },
      },
      y: {
        type: 'linear' as const,
        display: true,
        position: 'left' as const,
        grid: { color: 'rgba(66, 71, 84, 0.3)' },
        ticks: { color: '#c2c6d6', font: { family: 'Geist Mono' } },
      },
      y1: {
        type: 'linear' as const,
        display: true,
        position: 'right' as const,
        grid: { display: false },
        ticks: { color: '#ffb4ab', font: { family: 'Geist Mono' } },
      },
    },
  };

  // Chart 2: Risk distribution doughnut
  const riskChartData = {
    labels: ['High Risk', 'Medium Risk', 'Low Risk'],
    datasets: [
      {
        data: [highRiskCount, mediumRiskCount, lowRiskCount],
        backgroundColor: ['#ffb4ab', '#ffb3ad', '#4edea3'],
        borderWidth: 0,
        hoverOffset: 4,
      },
    ],
  };

  const riskChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    cutout: '75%',
    plugins: {
      legend: {
        position: 'bottom' as const,
        labels: {
          color: '#c2c6d6',
          padding: 16,
          font: { family: 'Geist', size: 12 },
          usePointStyle: true,
        },
      },
      tooltip: {
        backgroundColor: '#171f33',
        titleColor: '#dae2fd',
        bodyColor: '#c2c6d6',
        borderColor: '#424754',
        borderWidth: 1,
        padding: 12,
      },
    },
  };

  return (
    <div className="p-container-padding flex flex-col gap-stack-lg max-w-[1600px] mx-auto w-full">
      {/* Page Header */}
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-display font-display text-on-surface">Overview</h2>
          <p className="text-body-lg font-body-lg text-on-surface-variant mt-1">
            Real-time fraud detection and monitoring dashboard.
          </p>
        </div>
        <div className="flex gap-stack-sm">
          <button
            type="button"
            className="px-4 py-2 border border-outline-variant rounded-lg text-label-md font-label-md text-on-surface hover:bg-surface-container-highest transition-colors flex items-center gap-2"
          >
            <span className="material-symbols-outlined text-[18px]">download</span> Export
          </button>
          <button
            type="button"
            className="px-4 py-2 bg-primary-container text-on-primary-container rounded-lg text-label-md font-label-md font-bold hover:opacity-90 transition-opacity"
          >
            Generate Report
          </button>
        </div>
      </div>

      {/* Summary Metrics Bento Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-5 gap-gutter">
        <StatCard
          label="Total Transactions"
          value={stats.totalTransactions.toLocaleString()}
          icon="receipt_long"
          iconColor="text-primary"
          trendText={`+${stats.volumeTrendPercent}% from last week`}
          trendIcon="trending_up"
          trendColor="text-secondary"
        />
        <StatCard
          label="Fraud Detected"
          value={stats.fraudDetected}
          icon="warning"
          iconColor="text-error"
          trendText={`+${stats.alertsTodayCount} Alerts today`}
          trendIcon="trending_up"
          trendColor="text-error"
        />
        <StatCard
          label="Legitimate"
          value={stats.legitimate.toLocaleString()}
          icon="check_circle"
          iconColor="text-secondary"
          progressBarWidth={stats.totalTransactions > 0 ? `${((stats.legitimate / stats.totalTransactions) * 100).toFixed(1)}%` : '0%'}
        />
        <StatCard
          label="Fraud Rate"
          value={`${stats.fraudRate}%`}
          icon="pie_chart"
          iconColor="text-tertiary"
          subtext="Threshold limit: 3.00%"
        />
        <StatCard
          label="Avg Fraud Prob"
          value={`${stats.avgFraudProb}%`}
          icon="psychology"
          iconColor="text-primary"
          subtext="Across all evaluated transactions"
        />
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-gutter">
        {/* Main Volume Chart */}
        <div className="lg:col-span-2 bg-surface-container border border-outline-variant rounded-xl p-stack-md">
          <div className="flex justify-between items-center mb-stack-md pb-stack-sm border-b border-outline-variant/50">
            <h3 className="text-headline-md font-headline-md text-on-surface">
              Transaction Volume &amp; Fraud Trend
            </h3>
            <div className="flex gap-2">
              <button
                type="button"
                className="px-3 py-1 bg-surface-container-highest text-label-md font-label-md rounded text-on-surface"
              >
                7D
              </button>
              <button
                type="button"
                className="px-3 py-1 text-label-md font-label-md rounded text-on-surface-variant hover:bg-surface-container-highest"
              >
                30D
              </button>
            </div>
          </div>
          <div className="relative h-64 w-full">
            <Line data={mainChartData} options={mainChartOptions} />
          </div>
        </div>

        {/* Risk Distribution Chart */}
        <div className="bg-surface-container border border-outline-variant rounded-xl p-stack-md flex flex-col">
          <div className="flex justify-between items-center mb-stack-md pb-stack-sm border-b border-outline-variant/50">
            <h3 className="text-headline-md font-headline-md text-on-surface">
              Risk Distribution
            </h3>
          </div>
          <div className="relative flex-1 flex items-center justify-center min-h-[200px]">
            <Doughnut data={riskChartData} options={riskChartOptions} />
            <div className="absolute inset-0 flex items-center justify-center flex-col pointer-events-none pb-6">
              <span className="text-headline-lg font-headline-lg text-on-surface font-bold">
                {stats.totalTransactions >= 1000 ? `${(stats.totalTransactions / 1000).toFixed(1)}k` : stats.totalTransactions}
              </span>
              <span className="text-label-md font-label-md text-on-surface-variant">Total</span>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Flagged Transactions Table */}
      <div className="bg-surface-container border border-outline-variant rounded-xl overflow-hidden shadow-md">
        <div className="p-stack-md border-b border-outline-variant/50 flex justify-between items-center bg-surface-container-low">
          <h3 className="text-headline-md font-headline-md text-on-surface">
            Recent Transactions (Flagged)
          </h3>
          <Link
            to="/transactions"
            className="text-primary hover:text-primary-container text-label-md font-label-md flex items-center gap-1"
          >
            View All <span className="material-symbols-outlined text-[16px]">arrow_forward</span>
          </Link>
        </div>
        <TransactionTable transactions={transactions} />
      </div>
    </div>
  );
};
