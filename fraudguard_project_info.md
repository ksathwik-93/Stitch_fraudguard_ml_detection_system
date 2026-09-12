# FraudGuard: Online Payment Fraud Detection System
## Project Overview
FraudGuard is an academic B.Tech major project designed to demonstrate the application of Machine Learning in identifying fraudulent online payment transactions.

### Objective
To develop a robust, scalable, and accurate fraud detection system that analyzes transaction features in real-time to predict the likelihood of fraud.

### Machine Learning Approach
1. **Data Preprocessing**: Handling missing values, scaling features, and encoding categorical variables (e.g., transaction types like 'TRANSFER' or 'CASH_OUT').
2. **Class Imbalance Handling**: Utilizing techniques like SMOTE (Synthetic Minority Over-sampling Technique) to address the scarcity of fraud cases in typical financial datasets.
3. **Algorithms Used**: 
   - **Logistic Regression**: Baseline statistical model.
   - **Random Forest**: Ensemble learning for high accuracy and feature importance.
   - **XGBoost**: Gradient boosting for state-of-the-art predictive performance.
4. **Evaluation**: Metrics include Precision, Recall, F1-Score, and ROC-AUC, focusing on minimizing False Negatives (missed fraud).

### Deployment Architecture
The system follows a modern decoupled architecture:
- **Frontend**: React + TypeScript (Modern UI/UX).
- **API Layer**: Flask REST API for seamless communication.
- **ML Engine**: Python-based pipeline for inference.
- **Database**: SQLite for transaction logging and history.

### Limitations & Future Scope
- **Academic Scope**: This is a simulator and does not process real money or integrate with live banking APIs.
- **Future Enhancements**: Integration of Deep Learning (LSTMs), real-time streaming with Kafka, and explainable AI (SHAP) for better transparency.
