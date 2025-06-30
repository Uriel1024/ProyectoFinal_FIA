import pandas as pd
import joblib
import plotly.graph_objects as go
from pathlib import Path
from rich import print


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



	if not model_path.exists():
		print("Modelo no encontrados para la empresa seleccionada.")
		return


	save_data = joblib.load(model_path)
	model = save_data['model']
	features = save_data['features']
	user_input = {} #diccionario para guardar las respuetas del usuario y poder hacer la prediccion

	print(f"\n\nIngresa los datos requeridos de la empresa {empresas[ticker]}")
	print("\n\nEs recomendable entrar a las siguientes links para poder conocer los datos historicos de la empresa.")
	print("\n\nhttps://mx.investing.com/")
	print("\n\nhttps://es.finance.yahoo.com/")

	
	for feature in features:
		while True:
			try: 
				value = float(input(f"\n\nIngresa el valor de '{feature}':"))
				user_input[feature] = value
				break
			except ValueError:
				print("\n\nValor invalido, intenta nuevamente.")


			

	user_df = pd.DataFrame([user_input])
	pred = model.predict(user_df)[0]
	if pred == 1:
		print("\n\nEl precio de la accion va a subir, es recomendable invertir.")
	else: 
		print("\n\nEl precio de la accion bajara, no es recomendable invertir.")



