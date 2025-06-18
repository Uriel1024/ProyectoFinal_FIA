#archivo para probar codigo y funciones 

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

empresas = ['AAPL', 'MSFT','GOOGL','TSLA','INTC','JPM','V','MA','NVDA']
for ticker in empresas: 
	raw_path = BASE_DIR / f"data/processed/{ticker}_processed.csv"
	print(raw_path)

