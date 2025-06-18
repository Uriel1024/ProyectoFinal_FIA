import pandas as pd 
import joblib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier #random forest para tener un mejor resultado
from sklearn.feature_selection import RFE
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
#nuevas metricas para que el modelos sea mas preciso
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


def train_model(data_path, model_path):
    df = pd.read_csv(data_path, index_col='Date', parse_dates=True)
    X = df.select_dtypes(include  = 'number').drop(columns=['Target'])
    y = df['Target']

    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.3, random_state = 42)

    #para guardar las mejores caracteristicas
    best_features = []
    best_roc = 0

    for n_features in range(2, X.shape[1] + 1 ): 
        selector = RFE(RandomForestClassifier(random_state=42), n_features_to_select=n_features)
        selector. fit(X_train, y_train)
        selected_features = X.columns[selector.support_]

        model = RandomForestClassifier(random_state  = 42 )
        model.fit(X_train[selected_features], y_train)
        y_pred = model.predict(X_test[selected_features])
        current_roc = roc_auc_score(y_test,y_pred)

        if current_roc > best_roc: 
            best_roc = current_roc
            best_features = selected_features


    final_model = RandomForestClassifier(random_state = 42)
    final_model.fit(X_train[best_features], y_train)

    y_pred = final_model.predict(X_test[best_features])

    print("\nMetricas del modelo final")
    print(f"ROC AUC: {roc_auc_score(y_test,y_pred):.4f}")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):4f}")
    print(f"Precisión: {precision_score(y_test,y_pred):.4f}")
        
    joblib.dump({'model': final_model, 'features': best_features}, model_path)
    print(f'\nModelo guardad en {model_path}')
    print(f"Mejores features ({len(best_features)}): {', '.join(best_features)}")



if __name__ == "__main__":

    empresas = ['AAPL', 'MSFT','GOOGL','TSLA','BRK.B','JPM','V','MA','NVDA']
    for ticker in empresas: 
        raw_path = BASE_DIR / f"data/processed/{ticker}_processed.csv" 
        train_model(raw_path, f"{ticker}_model.pkl")           
