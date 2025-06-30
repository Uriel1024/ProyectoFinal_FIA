import os
import tkinter as tk
from tkinter import messagebox, simpledialog
import threading
import pandas as pd
import joblib
from pathlib import Path
import seleccion  
import webbrowser

# Configuración de rutas
BASE_DIR = Path(__file__).resolve().parent  
MODEL_DIR = BASE_DIR / "model"

empresas = getattr(seleccion, 'empresas', {})
link_win = None  #Sirve para las ventanas de los links


def ver_empresas():
    texto = "\n".join([f"{k}: {v}" for k, v in empresas.items()])
    messagebox.showinfo("Empresas Disponibles", texto)


def ver_historico():
    emp = simpledialog.askstring(
        "Ingresar ticker",
        "Escribe el ticker (por ejemplo: AAPL):"
    )
    if not emp:
        return
    emp = emp.upper()
    if emp not in empresas:
        messagebox.showwarning(
            "Ticker no reconocido",
            f"'{emp}' no está en la lista."
        )
        return
    threading.Thread(
        target=lambda: seleccion.graphs(emp),
        daemon=True
    ).start()


def show_links():
    global link_win
    if link_win and link_win.winfo_exists():
        link_win.destroy()

    #Crea una nueva ventana para permitir el copiado de links
    link_win = tk.Toplevel(ventana)
    link_win.title("Fuentes de datos")
    link_win.configure(bg="#20232A")

    text = tk.Text(
        link_win,
        wrap="word",
        bg="#282C34",
        fg="white",
        bd=0,
        padx=10,
        pady=10
    )

    links = [
        "https://mx.investing.com/",
        "https://es.finance.yahoo.com/"
    ]

    text.insert("1.0", "Recomendado consultar datos históricos en:\n\n")
    for url in links:
        text.insert(
            tk.END,
            url + "\n",
            ("link",)
        )

    text.tag_configure(
        "link",
        foreground="#61AFEF",
        underline=True
    )
    text.tag_bind(
        "link",
        "<Button-1>",
        lambda e: webbrowser.open(
            text.get("insert linestart", "insert lineend")
        )
    )

    text.config(state="normal")  #Permitir selección
    text.pack(fill="both", expand=True)
    return link_win


def predecir_precio():
    emp = simpledialog.askstring(
        "Ingresar ticker",
        "Escribe el ticker (por ejemplo: AAPL):"
    )
    if not emp:
        return
    emp = emp.upper()
    if emp not in empresas:
        messagebox.showwarning(
            "Ticker no reconocido",
            f"'{emp}' no está en la lista."
        )
        return

    #Muestra los links en la terminal
    print("Fuentes recomendadas para datos históricos:")
    print("- https://mx.investing.com/")
    print("- https://es.finance.yahoo.com/")

#Se supone que se deberían poder copiar los links desde aquí xd
    win = show_links()

    model_path = MODEL_DIR / f"{emp}_model.pkl"
    if not model_path.exists():
        messagebox.showerror(
            "Modelo no encontrado",
            f"No hay modelo para {emp}"
        )
        if win and win.winfo_exists(): win.destroy()
        return

    save_data = joblib.load(model_path)
    model = save_data.get('model')
    features = save_data.get('features', [])

    try:
        features = list(features)
    except Exception:
        features = []

    if model is None or len(features) == 0:
        messagebox.showerror(
            "Error de modelo",
            "Estructura de modelo inválida o sin features."
        )
        if win and win.winfo_exists(): win.destroy()
        return

    user_input = {}
    for feat in features:
        val = simpledialog.askfloat(
            "Entrada de datos",
            f"Ingresa el valor de '{feat}' para {empresas[emp]}:"
        )
        if val is None:
            if win and win.winfo_exists(): win.destroy()
            return
        user_input[feat] = val

    df_user = pd.DataFrame([user_input])
    try:
        pred = model.predict(df_user)[0]
    except Exception as e:
        messagebox.showerror(
            "Error",
            f"No se pudo predecir: {e}"
        )
        if win and win.winfo_exists(): win.destroy()
        return

    if pred == 1:
        msg = (
            f"[✓]El modelo predice que el precio de {emp} subirá. "
            "Considera invertir."
        )
    else:
        msg = (
            f"[X]El modelo predice que el precio de {emp} bajará. "
            "Ten precaución."
        )
    messagebox.showinfo("Resultado de la predicción", msg)
    if win and win.winfo_exists():
        win.destroy()


def salir():
    ventana.destroy()

#Colores
enabled_color = "#2E7D32"
disable_color = "#B71C1C"

#Main window
ventana = tk.Tk()
ventana.title("STOCKIA – Análisis de Acciones")
ventana.geometry("420x460")
ventana.configure(bg="#20232A")

#Botones para las primeras tres opciones
estilo_boton = {
    "font": ("Segoe UI", 12, "bold"),
    "fg": "white",
    "bg": enabled_color,
    "activebackground": "#4CAF50",
    "activeforeground": "black",
    "width": 32,
    "height": 2,
    "bd": 0,
    "relief": "flat"
}


titulo = tk.Label(
    ventana,
    text="📊 STOCKIA – Menú de Análisis",
    font=("Segoe UI", 18, "bold"),
    bg="#20232A",
    fg="#4CAF50"
)
titulo.pack(pady=20)

btn1 = tk.Button(
    ventana,
    text="1. Ver empresas disponibles",
    command=ver_empresas,
    **estilo_boton
)
btn1.pack(pady=5)

btn2 = tk.Button(
    ventana,
    text="2. Ver gráfico histórico",
    command=ver_historico,
    **estilo_boton
)
btn2.pack(pady=5)

btn3 = tk.Button(
    ventana,
    text="3. Predecir precio de acciones",
    command=predecir_precio,
    **estilo_boton
)
btn3.pack(pady=5)

btn4 = tk.Button(
    ventana,
    text="Salir",
    command=salir,
    font=("Segoe UI", 12, "bold"),
    fg="white",
    bg=disable_color,
    activebackground="#D32F2F",
    width=32,
    height=2,
    bd=0
)
btn4.pack(pady=20)

ventana.mainloop()
