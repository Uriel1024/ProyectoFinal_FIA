import pandas as pd 
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report 
import os 
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def evaluete(data_path, model_path):
	df = pd.read_csv(data_path, index_col='Date', parse_dates = True)
	model, selected_features = joblib.load(model_path)

	X = df[selected_features]
	y = df['Target']

	X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3)


	y_pred = model.predict(X_test)
	print(classification_report(y_test,y_pred))

if __name__ == '__main__':
	raw_path = BASE_DIR / "data/processed/AAPL_processed.csv"
	evaluete(raw_path, "model.pkl")