from tkinter import *
from tkinter import ttk


def construir_tabla(frame, columnas_vista, datos):
        tabla = ttk.Treeview(frame, columns=columnas_vista, show="headings")
        tabla.pack(padx=10, pady=10, fill="both", expand=True)
        for col in columnas_vista:
            tabla.heading(col, text=col)
            tabla.column(col, width=100)
        for fila in datos:
            tabla.insert("", END, values=fila)
        return tabla