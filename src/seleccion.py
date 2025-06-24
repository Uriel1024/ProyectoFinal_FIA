import pandas as pd
import joblib
import plotly.graph_objects as go
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


empresas = {
	'AAPL': 'Apple',
	'MSFT': 'Microsoft',
	'GOOGL': 'Google',
	'TSLA' : 'Tesla',
	'INTC': 'Intel',
	'JPM': 'JPMorgan Chase & Co',
	'V': 'Visa',
	'MA': 'Masterd Card' ,
	'NVDA': 'Nvidia' 
}

op = '0'

def menu():
	print('\n\n1.Conocer las empresas.')
	print('2.Conocer el historico de las empresas.')
	print('3.Predecir el precio de las acciones.')
	print('4.Sugerencias para invertir.')
	print('Ingrese -1 para salir del programa.')

def graphs(emp):
	raw_path = BASE_DIR /f"data/raw/{emp}_raw.csv"
	df = pd.read_csv(raw_path, parse_dates= ['Date'])
	fig = go.Figure(data = [go.Candlestick(
		x = df['Date'],
		open =df['Open'],
		high = df['High'],
		low =df['Low'],
		close = df['Close']
		)])
	fig.update_layout(title = 'Precio historico' , xaxis_title = 'Fecha', yaxis_title = 'Precio' )
	fig.show()	

def prediccion(ticker):
	model_path = BASE_DIR / f"src/model/{ticker}_model.pkl"
	data_path = BASE_DIR / f"data/processed/{ticker}_processed.csv"
	#model_path = BASE_DIR / f"model/{ticker}_model.pkl"


	if not model_path.exists() or not data_path.exists():
		print("Modelo o datos no encontrados para la empresa seleccionada.")
		return


	df = pd.read_csv(data_path, index_col='Date', parse_dates = True)

	save_data = joblib.load(model_path)
	model = save_data['model']
	features = save_data['features']


	latest_data = df.iloc[-1:][features]


	pred = model.predict(latest_data)[0]
	print(f"\nLa predicción para la acción de {empresas[ticker]} es que mañana va a {'subir' if pred == 1 else 'bajar'}.\n") 



while op != '-1':
	menu()
	op = input('Ingresa una opcion para poder continuar:')
	if op == '1':
		for clave, valor  in empresas.items():
			print(f"\nTicker:{clave}", f'Empresa:{valor}')
	elif op == '2':
		emp = input('\n\nIngresa el ticker de la empresa para conocer sus datos historicos:')
		graphs(emp)
	elif op == '3':
		emp = input("\n\nIngresa el ticker de la empresa para concer si bajara o subira el precio:")
		if emp in empresas: 
			prediccion(emp)
		else:
			print("\nTicker no reconocido.")
	elif op == '-1':
		print('\n\nGracias por usar STOCKIA.')
