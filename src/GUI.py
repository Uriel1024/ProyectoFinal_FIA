import os 
import tkinter as tk
from tkinter import messagebox, simpledialog
import seleccion  # Importamos tu archivo selección.py renombrado a módulo
import threading  # Para que el gráfico no congele la interfaz

# Funciones de UI
def ver_empresas():
    empresas = seleccion.listar_empresas()
    texto = "\n".join([f"{k}: {v}" for k, v in empresas.items()])
    messagebox.showinfo("Empresas Disponibles", texto)

def ver_historico():
    emp = simpledialog.askstring("Ingresar ticker", "Escribe el ticker (por ejemplo: AAPL):")
    if emp:
        try:
            threading.Thread(target=seleccion.mostrar_grafico, args=(emp.upper(),), daemon=True).start()
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo para {emp.upper()}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def salir():
    ventana.destroy()

# Ventana principal
ventana = tk.Tk()
ventana.title("Análisis de Acciones")
ventana.geometry("400x300")
ventana.configure(bg="black")

# Estilos
estilo_boton = {
    "font": ("Arial", 12, "bold"),
    "fg": "white",
    "bg": "#B22222",  # Rojo oscuro
    "activebackground": "#FF0000",
    "activeforeground": "black",
    "width": 30,
    "height": 2,
    "bd": 0
}

# Título
titulo = tk.Label(ventana, text="Menú de Análisis", font=("Arial", 16, "bold"), bg="black", fg="red")
titulo.pack(pady=20)

# Botones
btn1 = tk.Button(ventana, text="1. Ver empresas disponibles", command=ver_empresas, **estilo_boton)
btn1.pack(pady=5)

btn2 = tk.Button(ventana, text="2. Ver gráfico histórico", command=ver_historico, **estilo_boton)
btn2.pack(pady=5)

btn3 = tk.Button(ventana, text="Salir", command=salir, **estilo_boton)
btn3.pack(pady=20)

# Ejecutar
ventana.mainloop()
