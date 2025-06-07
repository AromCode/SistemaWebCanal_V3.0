from tkinter import Toplevel, Label, Entry, Button, Radiobutton, StringVar
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import hashlib
from conexion import MySQLConexion
from centrar_ventana import Centrar_Ventana

def registrar_usuario(usuario, contraseña, rol_val, ventana_registro):
    nuevo_usuario = usuario.get()
    nueva_contra = contraseña.get()
    rol = rol_val.get()

    # Validación campos vacíos
    if not nuevo_usuario or not nueva_contra:
        messagebox.showwarning("Advertencia", "Por favor, completar todos los campos")
        return

    # Encriptar la contraseña
    contra_encriptada = hashlib.sha256(nueva_contra.encode()).hexdigest()

    # Guardar el usuario en la base de datos
    conexion = MySQLConexion().ObtenerConexion()
    cursor = conexion.cursor()

    try:
        # Insertar nuevo usuario
        cursor.execute("INSERT INTO usuarios (usuario, contraseña, tipo_usuario) VALUES (%s, %s, %s)",
                       (nuevo_usuario, contra_encriptada, rol))
        conexion.commit()
        messagebox.showinfo("Éxito", "Usuario registrado con éxito")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al registrar el usuario: {err}")
    finally:
        cursor.close()
        conexion.close()

    ventana_registro.destroy()

def abrir_ventana_registro():
    ventana_registro = Toplevel()
    ventana_registro.title("Registro de Usuario")
    ventana_registro.iconbitmap("Imagen/login.ico")
    ventana_registro.resizable(0,0)
    Centrar_Ventana(ventana_registro, 400, 450)

    imagen =  Image.open("Imagen/logo.png")
    imagen = imagen.resize((150, 150))
    imagen_tk = ImageTk.PhotoImage(imagen)

    label = Label(ventana_registro, image=imagen_tk)
    label.pack(pady=20)
    label.image = imagen_tk

    # Etiquetas y campos de entrada
    texto = Label(ventana_registro, text="Formulario de Registro", font=("Arial", 18, "bold"))
    texto.pack(pady=3)

    Label(ventana_registro, text="Nombre de usuario: ", font=("Arial", 11)).place(x=55, y=260)
    txt1 =  Entry(ventana_registro, font=11, width=15)
    txt1.place(x=198, y=260)

    Label(ventana_registro, text="Contraseña: ", font=("Arial", 11)).place(x=55, y=300)
    txt2 =  Entry(ventana_registro, show="*", font=11, width=15)
    txt2.place(x=198, y=300)

    rol_val  = StringVar(value="Usuario")
    Radiobutton(ventana_registro, text="Administrador", variable=rol_val, value="Administrador", font=("Arial", 11)).place(x=80, y=345)
    Radiobutton(ventana_registro, text="Usuario", variable=rol_val, value="Usuario", font=("Arial", 11)).place(x=230, y=345)
    
    #botones de acción
    boton = Button(ventana_registro, text="Registrar", font=("Arial", 11, "bold"), command=lambda: registrar_usuario(txt1, txt2, rol_val, ventana_registro))
    boton.config(width=10)
    boton.place(x=150, y=390)

    ventana_registro.mainloop()