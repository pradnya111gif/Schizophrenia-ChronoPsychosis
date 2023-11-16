import pandas as pd
from sklearn.model_selection import StratifiedKFold
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, f1_score, precision_score


file_path = '/Users/pradnyajadhav/Desktop/Schizophrenia_Chronopsychosis/12_parts_features.csv'
df = pd.read_csv(file_path)


X = df.drop(['Filename', 'Date', 'Class'], axis=1)
y = df['Class']


classifiers = {
    'XGBoost': XGBClassifier(),
    'LightGBM': LGBMClassifier(),
}


cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)


for clf_name, model in classifiers.items():
    accuracy_scores = []
    auc_roc_scores = []
    f1_scores = []
    precision_scores = []
    
    
    for train_index, test_index in cv.split(X, y):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        
        
        model.fit(X_train, y_train)
        
        
        y_pred = model.predict(X_test)
        
        
        accuracy = accuracy_score(y_test, y_pred)
        accuracy_scores.append(accuracy)
        
        auc_roc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
        auc_roc_scores.append(auc_roc)
        
        f1 = f1_score(y_test, y_pred)
        f1_scores.append(f1)
        
        precision = precision_score(y_test, y_pred)
        precision_scores.append(precision)
    
    
    average_accuracy = sum(accuracy_scores) / len(accuracy_scores)
    average_auc_roc = sum(auc_roc_scores) / len(auc_roc_scores)
    average_f1 = sum(f1_scores) / len(f1_scores)
    average_precision = sum(precision_scores) / len(precision_scores)
    
    print(f'{clf_name} Results:')
    print(f'Average Accuracy: {average_accuracy:.2f}')
    print(f'Average AUC-ROC: {average_auc_roc:.2f}')
    print(f'Average F1 Score: {average_f1:.2f}')
    print(f'Average Precision: {average_precision:.2f}')
    print('\n')
