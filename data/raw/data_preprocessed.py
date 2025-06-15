import pandas as pd 
import pandas_ta as ta 
import yfinanace as yf 
import os

#Funcion para obtener la informacion de los datos 
def  download_data(ticker, start, end, outputh_path):
	df = yf.download(ticker, start = start, end = end)
	df.to_csv(outputh_path)
	return df


def preprocess_data(input_path, outputh_path):
	df = pd.read_csv(input_path, index_col='Date', parse_dates=True)
	df['SMA_10'] = ta.sma(df['Close'], length = 10)
	df['SMA_50'] = ta.sma(df['Close'], length = 50)
	df['RSI'] = ta.rsi(df['Close'], length = 14)
	df['Target'] = (df['Close'].shift(-1)> df['Close']).astype(int)
	df.dropna(inplace=True)
	df.to_csv(outputh_path)

if __name__ == "__main__":
	raw_path = 'data/raw/AAPL_raw.csv'
	processed_path = 'data/processed/AAPL_processed.csv'
	if not os.path.exists(raw_path):
		download_data('AAPL', '2018-01-01', '2024-12-31', raw_path)
	processed_path(raw_path, processed_path)