import warnings
warnings.filterwarnings("ignore", category=UserWarning)
import pandas as pd 
import pandas_ta as ta 
import yfinance as yf 
import os
from pathlib import Path


#Para obtener la ruta base del proyecto XDDDD
BASE_DIR = Path(__file__).resolve().parent.parent



#Funcion para obtener la iaanformacion de los datos 
def  download_data(ticker, start, end, output_path):
    df = yf.download(ticker, start = start, end = end)    
    df.reset_index(inplace = True)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_path, index = False)
    return df


def preprocess_data(input_path, output_path):
    df = pd.read_csv(input_path, parse_dates=['Date'])
    
    # Verifica que 'Close' sea numérico
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
    
    # Elimina filas con valores NaN que puedan haberse creado
    df.dropna(subset=['Close'], inplace=True)
    
    df.set_index('Date', inplace=True)

    df['SMA_10'] = ta.sma(df['Close'], length=10)
    df['SMA_50'] = ta.sma(df['Close'], length=50)
    df['RSI'] = ta.rsi(df['Close'], length=14)
    df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
    df.dropna(inplace=True)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path)

if __name__ == "__main__":

    empresas = ['AAPL', 'MSFT','GOOGL','TSLA','INTC','JPM','V','MA','NVDA']
    for ticker in empresas: 
        raw_path = BASE_DIR / f"data/raw/{ticker}_raw.csv"
        processed_path = BASE_DIR/ f"data/processed/{ticker}_processed.csv"
        
        if not raw_path.exists():
            download_data(ticker, '2018-01-01', '2024-12-31',raw_path    )

        preprocess_data(raw_path, processed_path)
