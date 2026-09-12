import React, { useState } from 'react';
import { AnalyzePayload, TransactionType } from '../../types';
import { Button } from '../common/Button';
import { Input } from '../common/Input';
import { Select } from '../common/Select';

interface TransactionFormProps {
  onAnalyze: (payload: AnalyzePayload) => void;
  isLoading: boolean;
}

export const TransactionForm: React.FC<TransactionFormProps> = ({
  onAnalyze,
  isLoading,
}) => {
  const [type, setType] = useState<TransactionType | ''>('TRANSFER');
  const [amount, setAmount] = useState<string>('45200.00');
  const [oldBalanceOrg, setOldBalanceOrg] = useState<string>('45200.00');
  const [newBalanceOrg, setNewBalanceOrg] = useState<string>('0.00');
  const [oldBalanceDest, setOldBalanceDest] = useState<string>('0.00');
  const [newBalanceDest, setNewBalanceDest] = useState<string>('0.00');
  const [errors, setErrors] = useState<{ [key: string]: string }>({});

  const handleClear = () => {
    setType('');
    setAmount('');
    setOldBalanceOrg('');
    setNewBalanceOrg('');
    setOldBalanceDest('');
    setNewBalanceDest('');
    setErrors({});
  };

  const validate = () => {
    const errs: { [key: string]: string } = {};

    if (!type) errs.type = 'Transaction type is required';
    if (!amount || isNaN(Number(amount)) || Number(amount) <= 0) {
      errs.amount = 'Valid positive amount is required';
    }
    if (oldBalanceOrg === '' || isNaN(Number(oldBalanceOrg))) {
      errs.oldBalanceOrg = 'Origin balance before is required';
    }
    if (newBalanceOrg === '' || isNaN(Number(newBalanceOrg))) {
      errs.newBalanceOrg = 'Origin balance after is required';
    }
    if (oldBalanceDest === '' || isNaN(Number(oldBalanceDest))) {
      errs.oldBalanceDest = 'Destination balance before is required';
    }
    if (newBalanceDest === '' || isNaN(Number(newBalanceDest))) {
      errs.newBalanceDest = 'Destination balance after is required';
    }

    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;

    onAnalyze({
      type: type as TransactionType,
      amount: Number(amount),
      oldBalanceOrg: Number(oldBalanceOrg),
      newBalanceOrg: Number(newBalanceOrg),
      oldBalanceDest: Number(oldBalanceDest),
      newBalanceDest: Number(newBalanceDest),
    });
  };

  return (
    <div className="bg-surface-variant border border-outline-variant rounded-xl p-container-padding relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute top-0 right-0 w-64 h-64 bg-primary/5 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2 pointer-events-none" />

      {/* Header */}
      <div className="flex items-center justify-between mb-stack-md pb-stack-sm border-b border-outline-variant/50">
        <h2 className="text-headline-md font-headline-md text-on-background flex items-center gap-2">
          <span className="material-symbols-outlined text-outline">tune</span>
          Input Parameters
        </h2>
        <button
          type="button"
          onClick={handleClear}
          className="text-label-md font-label-md text-primary hover:text-primary-container transition-colors"
        >
          Clear Form
        </button>
      </div>

      <form onSubmit={handleSubmit} className="space-y-stack-md">
        {/* Row 1: Type & Amount */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-gutter">
          <Select
            id="tx-type"
            label="Transaction Type"
            requiredMark
            value={type}
            onChange={(e) => setType(e.target.value as TransactionType)}
            error={errors.type}
            options={[
              { value: 'PAYMENT', label: 'PAYMENT' },
              { value: 'TRANSFER', label: 'TRANSFER' },
              { value: 'CASH_OUT', label: 'CASH_OUT' },
              { value: 'DEBIT', label: 'DEBIT' },
              { value: 'CASH_IN', label: 'CASH_IN' },
            ]}
          />

          <Input
            id="tx-amount"
            label="Amount (USD)"
            requiredMark
            prefixSymbol="$"
            mono
            type="number"
            placeholder="0.00"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            error={errors.amount}
          />
        </div>

        {/* Sender Section */}
        <div className="p-stack-sm bg-surface-container-low border border-outline-variant/50 rounded-lg">
          <div className="text-label-md font-label-md text-on-surface mb-2 flex items-center gap-2">
            <span className="material-symbols-outlined text-[16px]">person_remove</span>
            Origin (Sender) Accounts
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-gutter">
            <Input
              id="old-balance-org"
              label="Balance Before"
              mono
              type="number"
              placeholder="0.00"
              value={oldBalanceOrg}
              onChange={(e) => setOldBalanceOrg(e.target.value)}
              error={errors.oldBalanceOrg}
            />
            <Input
              id="new-balance-org"
              label="Balance After"
              mono
              type="number"
              placeholder="0.00"
              value={newBalanceOrg}
              onChange={(e) => setNewBalanceOrg(e.target.value)}
              error={errors.newBalanceOrg}
            />
          </div>
        </div>

        {/* Receiver Section */}
        <div className="p-stack-sm bg-surface-container-low border border-outline-variant/50 rounded-lg">
          <div className="text-label-md font-label-md text-on-surface mb-2 flex items-center gap-2">
            <span className="material-symbols-outlined text-[16px]">person_add</span>
            Destination (Receiver) Accounts
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-gutter">
            <Input
              id="old-balance-dest"
              label="Balance Before"
              mono
              type="number"
              placeholder="0.00"
              value={oldBalanceDest}
              onChange={(e) => setOldBalanceDest(e.target.value)}
              error={errors.oldBalanceDest}
            />
            <Input
              id="new-balance-dest"
              label="Balance After"
              mono
              type="number"
              placeholder="0.00"
              value={newBalanceDest}
              onChange={(e) => setNewBalanceDest(e.target.value)}
              error={errors.newBalanceDest}
            />
          </div>
        </div>

        {/* Action Button */}
        <div className="pt-stack-sm border-t border-outline-variant/50 flex justify-end">
          <Button
            type="submit"
            isLoading={isLoading}
            icon="science"
            variant="primary"
            size="lg"
          >
            {isLoading ? 'Analyzing...' : 'Run Analysis'}
          </Button>
        </div>
      </form>
    </div>
  );
};
