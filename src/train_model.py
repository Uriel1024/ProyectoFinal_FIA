import pandas as pd 
import joblib
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestClassifier
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


def train_model(data_path, model_path):
	df = pd.read_csv(data_path, index_col='Date', parse_dates=True)
	X = df.select_dtypes(include  = 'number').drop(columns=['Target'])
	y = df['Target']

	selector = RFE(RandomForestClassifier() , n_features_to_select = 5)
	selector.fit(X,y)
	selected_features = X.columns[selector.support_]

	X_train, X_test, y_train, y_test = train_test_split(X[selected_features],y,test_size = 0.3)
	model = DecisionTreeClassifier(max_depth = 5)
	model.fit(X_train, y_train)


	joblib.dump((model,selected_features), model_path)

if __name__ == "__main__":
	raw_path = BASE_DIR / "data/processed/AAPL_processed.csv"
	train_model(raw_path, "model.pkl")