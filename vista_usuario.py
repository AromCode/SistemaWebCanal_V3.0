from tkinter import*
from PIL import Image, ImageTk
from tkinter import messagebox
from conexion import MySQLConexion
from construir_tabla import construir_tabla
from centrar_ventana import Centrar_Ventana

def Abrir_dashboard_usuario(usuario):

    def cerrar_sesion():
        ventana.destroy()

    def limpiar_frame():
        for widget in contenido.winfo_children():
            widget.destroy()

    #funciones necesarias
    def mostrar_programas():
        limpiar_frame()
        Label(contenido, text="Programas Registrados", font=("Arial", 11, "bold")).pack(pady=10)

        columnas_vista = ["id",  "Nombre", "Descripción", "Género", "Tema", "Conductor", "Duración", "Horario", "Plataforma"]

        #cargar los datos desde mysql
        try:
            conexion = MySQLConexion().ObtenerConexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, descripcion, genero, tema, conductor, duracion, horario, plataforma FROM programas")
            programas = cursor.fetchall()
            cursor.close()
            conexion.close()

            construir_tabla(contenido, columnas_vista, programas)

        except Exception as e:
            messagebox.showerror("Error...\n", f"No se pudo cargar los programas\n{e}")
            return

    #creacion de la ventana
    ventana =  Tk()
    ventana.title("Dashboard Usuario")
    ventana.resizable(0,0)
    Centrar_Ventana(ventana, 1120, 450)

    #barra lateral izquierda
    menu_izq  =  Frame(ventana, width=200, height=550, bd=1, relief="solid")
    menu_izq.pack(side=LEFT, fill=Y)
    menu_izq.pack_propagate(False)

    #imagen
    imagen =  Image.open("Imagen/logo.png")
    imagen = imagen.resize((150, 150))
    imagen_tk = ImageTk.PhotoImage(imagen)

    label = Label(menu_izq, image=imagen_tk)
    label.pack(pady=20)
    label.image = imagen_tk

    #iconos
    icono1 = PhotoImage(file="Imagen/ver_programa.png")
    icono2 = PhotoImage(file="Imagen/salir.png")

    #botones

    boton1 = Button(menu_izq, text="Ver Programas", image=icono1, compound="left", command=mostrar_programas, font=("Arial", 11, "bold"), padx=10, pady=10)
    boton1.pack(fill=X, pady=20)

    boton2 = Button(menu_izq, text="Cerrar sesión", image=icono2, compound="left", command=cerrar_sesion, font=("Arial", 11, "bold"), padx=10, pady=10)
    boton2.pack(fill=X, pady=37)

    #frame derecho
    contenido  =  Frame(ventana)
    contenido.pack(side=RIGHT, expand=True, fill=BOTH)

    ventana.mainloop()