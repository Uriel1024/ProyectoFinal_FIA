import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


empresas = {
	'AAPL': 'Apple',
	'MSFT': 'Microsoft',
	'GOOGL': 'Google',
	'TSLA' : 'TSLA',
	'INTCL': 'Intel',
	'JPM': 'JPMorgan Chase & Co',
	'V': 'Visa',
	'MA': 'Masterd Card' ,
	'NVDA': 'Nvidia' 
}

op = 0

def menu():
	print('\n\n1.Conocer las empresas.')
	print('2.Conocer el historico de las empresas.')
	print('3.Predecir si subirar o no el precio de las acciones.')
	print('Ingrese -1 para salir del programa.')



while op != -1:
	menu()
	op = int(input('Ingresa una opcion para poder continuar:'))
	if op == 1:
		for clave, valor  in empresas.items():
			print(f"\nTicker:{clave}", f'Empresa:{valor}')
	elif op == 2:
		emp = input('\n\nIngresa el ticker de la empresa para conocer sus datos historicos:')
		raw_path = BASE_DIR / f"data/raw/{emp}_raw.csv"
		df = pd.read_csv(raw_path, parse_dates=['Date'])

		fig = go.Figure(data = [go.Candlestick(
			x = df['Date'],
			open =df['Open'],
			high = df['High'],
			low =df['Low'],
			close = df['Close']
			)])
		fig.update_layout(title  = 'Precio historico ', xaxis_title = 'Fecha', yaxis_title = 'Precio')
		fig.show()

