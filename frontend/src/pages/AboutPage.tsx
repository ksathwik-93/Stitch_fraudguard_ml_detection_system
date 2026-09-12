import React from 'react';

export const AboutPage: React.FC = () => {
  return (
    <div className="p-container-padding lg:p-stack-lg max-w-6xl mx-auto w-full space-y-stack-lg">
      {/* Header */}
      <header className="mb-stack-lg">
        <div className="flex items-center gap-2 mb-2 text-primary">
          <span className="material-symbols-outlined text-xl">school</span>
          <span className="text-label-md font-label-md uppercase tracking-wider font-semibold">
            Academic Project Overview (4th-Year Major Project)
          </span>
        </div>
        <h1 className="text-display font-display text-on-surface mb-4">
          Online Payment Fraud Detection Using Machine Learning
        </h1>
        <p className="text-body-lg font-body-lg text-on-surface-variant max-w-3xl">
          A comprehensive machine learning system designed to identify and flag anomalous transactions in simulated financial environments. This documentation outlines the architecture, methodologies, and technical scope of the FraudGuard project.
        </p>
      </header>

      {/* Disclaimer Warning Card */}
      <div className="bg-error-container/10 border border-error/20 rounded-xl p-6 flex items-start gap-4 shadow-sm">
        <span className="material-symbols-outlined text-error text-2xl mt-1">warning</span>
        <div>
          <h3 className="text-headline-md font-headline-md text-error mb-2">
            Important Prototype Disclaimer
          </h3>
          <p className="text-body-md font-body-md text-on-surface-variant">
            FraudGuard is strictly an <strong>academic prototype</strong> designed for educational and research purposes. It operates on synthetic financial transaction datasets and is <strong>not equipped or intended to process live payments or real banking APIs</strong>.
          </p>
        </div>
      </div>

      {/* Bento Grid Section */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-gutter">
        {/* Objective Card */}
        <div className="md:col-span-12 lg:col-span-8 bg-surface-container-low border border-outline-variant rounded-xl p-6 relative overflow-hidden group">
          <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
            <span className="material-symbols-outlined text-6xl text-primary">target</span>
          </div>
          <h2 className="text-headline-lg font-headline-lg text-on-surface mb-4 flex items-center gap-2">
            <span className="material-symbols-outlined text-primary">flag</span>
            Project Objective
          </h2>
          <div className="text-body-lg font-body-lg text-on-surface-variant space-y-4">
            <p>
              The primary goal of FraudGuard is to engineer a high-precision machine learning pipeline capable of detecting fraudulent transactions in real-time while maintaining minimal false positives.
            </p>
            <p>
              By addressing heavy class imbalance common in financial data, the system optimizes for high precision and recall on minority fraud classes without creating unnecessary friction for legitimate user transactions.
            </p>
            <ul className="list-disc pl-5 space-y-2 text-body-md font-body-md mt-4">
              <li>Target F1-score &gt; 0.85 on minority fraud class detection.</li>
              <li>Maintain end-to-end API inference latency &lt; 200ms per transaction payload.</li>
              <li>Provide clear, interpretable risk scoring for security analyst audit workflows.</li>
            </ul>
          </div>
        </div>

        {/* System Flow Card */}
        <div className="md:col-span-12 lg:col-span-4 bg-surface-container-low border border-outline-variant rounded-xl p-6 flex flex-col items-center justify-center min-h-[300px]">
          <h3 className="text-headline-md font-headline-md text-on-surface mb-4 self-start">
            System Data Flow
          </h3>
          <div className="w-full flex flex-col items-center justify-center gap-3 text-on-surface-variant opacity-80">
            <div className="flex items-center gap-2 bg-surface-container border border-outline-variant px-4 py-2.5 rounded-lg text-sm w-full justify-center font-mono-data">
              <span className="material-symbols-outlined text-primary">database</span> Data Ingestion
            </div>
            <span className="material-symbols-outlined text-primary">arrow_downward</span>
            <div className="flex items-center gap-2 bg-surface-container border border-primary/40 px-4 py-2.5 rounded-lg text-sm text-primary w-full justify-center font-mono-data">
              <span className="material-symbols-outlined">memory</span> ML Inference Engine
            </div>
            <span className="material-symbols-outlined text-primary">arrow_downward</span>
            <div className="flex items-center gap-2 bg-surface-container border border-outline-variant px-4 py-2.5 rounded-lg text-sm w-full justify-center font-mono-data">
              <span className="material-symbols-outlined text-secondary">dashboard</span> Analyst Dashboard UI
            </div>
          </div>
        </div>

        {/* Preprocessing Card */}
        <div className="md:col-span-12 lg:col-span-6 bg-surface-container-low border border-outline-variant rounded-xl p-6 space-y-4">
          <div className="flex items-center justify-between border-b border-outline-variant pb-3">
            <h3 className="text-headline-md font-headline-md text-on-surface flex items-center gap-2">
              <span className="material-symbols-outlined text-secondary">filter_alt</span>
              Data Preprocessing &amp; Pipeline
            </h3>
          </div>
          <div className="space-y-3">
            <div className="bg-surface-container rounded-lg p-4 border border-outline-variant/50">
              <h4 className="text-body-lg font-body-lg font-semibold text-on-surface mb-1">
                Feature Engineering
              </h4>
              <p className="text-body-md font-body-md text-on-surface-variant">
                Account balance differentials, transactional velocity, and one-hot encoding of categorical payment types (e.g. TRANSFER, CASH_OUT).
              </p>
            </div>
            <div className="bg-surface-container rounded-lg p-4 border border-outline-variant/50">
              <h4 className="text-body-lg font-body-lg font-semibold text-on-surface mb-1">
                Handling Imbalance
              </h4>
              <p className="text-body-md font-body-md text-on-surface-variant">
                Synthetic Minority Over-sampling Technique (SMOTE) combined with ENN to balance minority class training distributions.
              </p>
            </div>
            <div className="bg-surface-container rounded-lg p-4 border border-outline-variant/50">
              <h4 className="text-body-lg font-body-lg font-semibold text-on-surface mb-1">
                Scaling &amp; Normalization
              </h4>
              <p className="text-body-md font-body-md text-on-surface-variant">
                Robust Scaling applied to continuous financial amounts to mitigate heavy-tailed outlier skewed distributions.
              </p>
            </div>
          </div>
        </div>

        {/* Algorithms Card */}
        <div className="md:col-span-12 lg:col-span-6 bg-surface-container-low border border-outline-variant rounded-xl p-6 space-y-4">
          <div className="flex items-center justify-between border-b border-outline-variant pb-3">
            <h3 className="text-headline-md font-headline-md text-on-surface flex items-center gap-2">
              <span className="material-symbols-outlined text-primary-container">model_training</span>
              Evaluated Algorithms
            </h3>
          </div>
          <p className="text-body-md font-body-md text-on-surface-variant">
            Three baseline and ensemble models are cross-validated to compare predictive efficiency:
          </p>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-surface-container rounded-lg border border-outline-variant/50">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded bg-primary/20 flex items-center justify-center text-primary font-mono-data text-xs font-bold">
                  RF
                </div>
                <span className="text-body-md font-body-md text-on-surface font-medium">Random Forest</span>
              </div>
              <span className="text-label-md font-label-md text-secondary">Primary Candidate</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-surface-container rounded-lg border border-outline-variant/50">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded bg-surface-bright flex items-center justify-center text-on-surface-variant font-mono-data text-xs font-bold">
                  XGB
                </div>
                <span className="text-body-md font-body-md text-on-surface font-medium">XGBoost</span>
              </div>
              <span className="text-label-md font-label-md text-on-surface-variant">Gradient Boosting Candidate</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-surface-container rounded-lg border border-outline-variant/50">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded bg-surface-bright flex items-center justify-center text-on-surface-variant font-mono-data text-xs font-bold">
                  LR
                </div>
                <span className="text-body-md font-body-md text-on-surface font-medium">Logistic Regression</span>
              </div>
              <span className="text-label-md font-label-md text-on-surface-variant">Statistical Baseline</span>
            </div>
          </div>
        </div>

        {/* Deployment Architecture Stack */}
        <div className="md:col-span-12 bg-surface-container-low border border-outline-variant rounded-xl p-6">
          <h3 className="text-headline-lg font-headline-lg text-on-surface mb-6 flex items-center gap-2 border-b border-outline-variant pb-4">
            <span className="material-symbols-outlined text-inverse-primary">cloud_sync</span>
            System Stack Architecture
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-surface-container p-5 rounded-lg border border-outline-variant">
              <div className="w-10 h-10 rounded-full bg-surface-bright flex items-center justify-center mb-4">
                <span className="material-symbols-outlined text-primary">web</span>
              </div>
              <h4 className="text-headline-md font-headline-md text-on-surface mb-2">React + TypeScript (Frontend)</h4>
              <p className="text-body-md font-body-md text-on-surface-variant">
                High-density analyst suite built with Vite, Tailwind CSS, and React Router for real-time monitoring and transaction inspection.
              </p>
            </div>

            <div className="bg-surface-container p-5 rounded-lg border border-outline-variant">
              <div className="w-10 h-10 rounded-full bg-surface-bright flex items-center justify-center mb-4">
                <span className="material-symbols-outlined text-secondary">api</span>
              </div>
              <h4 className="text-headline-md font-headline-md text-on-surface mb-2">Flask REST API (Backend Layer)</h4>
              <p className="text-body-md font-body-md text-on-surface-variant">
                Python API serving model predictions via `/api/predict`, transaction log APIs, and analytics statistics.
              </p>
            </div>

            <div className="bg-surface-container p-5 rounded-lg border border-outline-variant">
              <div className="w-10 h-10 rounded-full bg-surface-bright flex items-center justify-center mb-4">
                <span className="material-symbols-outlined text-tertiary">storage</span>
              </div>
              <h4 className="text-headline-md font-headline-md text-on-surface mb-2">SQLite Database</h4>
              <p className="text-body-md font-body-md text-on-surface-variant">
                Embedded transactional store for logging processed payment records, auditor flags, and operational metrics.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
