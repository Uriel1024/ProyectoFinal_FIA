import pandas as pd 
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report 
import os 
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def evaluete(data_path, model_path):
	df = pd.read_csv(data_path, index_col='Date', parse_dates = True)
	save_data = joblib.load(model_path)
	model = save_data['model']
	best_features = save_data['features']

	X = df[best_features]
	y = df['Target']

	X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3)


	y_pred = model.predict(X_test)
	print(classification_report(y_test,y_pred))

if __name__ == '__main__':
	empresas = ['AAPL', 'MSFT','GOOGL','TSLA','INTC','JPM','V','MA','NVDA']
	for ticker in empresas: 
		raw_path = BASE_DIR / f"data/processed/{ticker}_processed.csv"
		model = f"{ticker}_model.pkl"
		evaluete(raw_path, model)		
	

	