export type TransactionType = 'PAYMENT' | 'TRANSFER' | 'CASH_OUT' | 'DEBIT' | 'CASH_IN';
export type RiskLevel = 'LOW' | 'MEDIUM' | 'HIGH';
export type TransactionStatus = 'CLEARED' | 'REVIEW' | 'BLOCKED';

export interface Transaction {
  id: string;
  dateTime: string;
  type: TransactionType | string;
  amount: number;
  fraudProbability: number;
  riskLevel: RiskLevel;
  status: TransactionStatus;
  oldBalanceOrg?: number;
  newBalanceOrg?: number;
  oldBalanceDest?: number;
  newBalanceDest?: number;
}

export interface AnalyzePayload {
  type: TransactionType;
  amount: number;
  oldBalanceOrg: number;
  newBalanceOrg: number;
  oldBalanceDest: number;
  newBalanceDest: number;
}

export interface PredictionResult {
  transactionId: string;
  prediction: 'FRAUD' | 'LEGITIMATE';
  fraudProbability: number;
  riskLevel: RiskLevel;
  recommendation: string;
  timestamp: string;
}

export interface DashboardStats {
  totalTransactions: number;
  fraudDetected: number;
  legitimate: number;
  fraudRate: number;
  avgFraudProb: number;
  volumeTrendPercent: number;
  alertsTodayCount: number;
}

export interface ModelMetrics {
  modelName: string;
  accuracy: number;
  precision: number;
  recall: number;
  f1Score: number;
  rocAuc: number;
  tag?: string;
  isChampion?: boolean;
}

export interface FeatureImportance {
  feature: string;
  importance: number;
}

export interface ConfusionMatrixData {
  trueNegatives: number;
  falsePositives: number;
  falseNegatives: number;
  truePositives: number;
}

export interface PaginatedTransactions {
  transactions: Transaction[];
  page: number;
  limit: number;
  total: number;
  pages: number;
}

export interface HealthResponse {
  status: string;
  model_loaded: boolean;
  database_connected: boolean;
  model_type?: string;
  model_name?: string;
}
