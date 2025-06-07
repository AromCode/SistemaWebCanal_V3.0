from tkinter import*
from tkinter import messagebox
from PIL import Image, ImageTk
from conexion import MySQLConexion
from registrar import abrir_ventana_registro
from vista_admin import Abrir_dashboard_administrador
from vista_usuario  import  Abrir_dashboard_usuario
from hashlib import sha256
from centrar_ventana  import Centrar_Ventana

ventana = Tk()
ventana.title("Login y registro")
ventana.iconbitmap("Imagen/login.ico")
ventana.resizable(0,0)
Centrar_Ventana(ventana,400,450)

#métodos de validaciones
def Validar_login():
    user = txt1.get().strip()
    contra = txt2.get().strip()
    rol_seleccion  =  rol_val_login.get()

    #validacion si el campo está vacio
    if not user or not contra:
        messagebox.showwarning("Advertencia", "Por favor, completar todos los campos")
        return
    
    #conectar a la base de datos y verificar usuario
    conexion = MySQLConexion().ObtenerConexion()
    if conexion is None:
        messagebox.showerror("Error...\nNo se pudo conectar a la base de datos")
        return
    
    cursor = conexion.cursor()

    try:
        cursor.execute("SELECT * FROM usuarios WHERE usuario =  %s", (user,))
        sistemaweb_tv = cursor.fetchone()

        if sistemaweb_tv:
            contra = sha256(contra.encode()).hexdigest()
            contra_bd = sistemaweb_tv[2]
            rol_bd = sistemaweb_tv[3]

            if contra == contra_bd:
                if rol_seleccion == rol_bd:
                    messagebox.showinfo("Éxito", f"Bienvenido/a, {user}")
                    ventana.destroy()

                    if rol_bd == "Administrador":
                        Abrir_dashboard_administrador(user)
                    else:
                        Abrir_dashboard_usuario(user)
                else:
                    messagebox.showerror("Error", "Rol incorrecto\nIngrese con su rol asignado...")
            else:
                messagebox.showerror("Error", "Contraseña incorrecta")
        else:
            messagebox.showerror("Error", "Usuario no encontrado en el sistema")
    finally:
        cursor.close()
        conexion.close()

#insertar imagen
imagen =  Image.open("Imagen/logo.png")
imagen = imagen.resize((150, 150))
imagen_tk = ImageTk.PhotoImage(imagen)

label = Label(ventana, image=imagen_tk)
label.pack(pady=20)
label.image = imagen_tk

#insertar texto y widgets
texto = Label(ventana, text="Binvenido a '45 Megavisión'", font=("Arial", 18, "bold"))
texto.pack(pady=3)

Label(ventana, text="Nombre de usuario: ", font=("Arial", 11)).place(x=55, y=260)
txt1 =  Entry(ventana, font=11, width=15)
txt1.place(x=198, y=260)

Label(ventana, text="Contraseña: ", font=("Arial", 11)).place(x=55, y=300)
txt2 =  Entry(ventana, show="*", font=11, width=15)
txt2.place(x=198, y=300)

#opciones de inicio de sesión
rol_val_login  =  StringVar(value="Usuario")
Radiobutton(ventana, text="Administrador", variable=rol_val_login , value="Administrador", font=("Arial", 11)).place(x=80, y=345)
Radiobutton(ventana, text="Usuario", variable=rol_val_login , value="Usuario", font=("Arial", 11)).place(x=230, y=345)

#botones de acción
boton1 = Button(ventana, text="Iniciar Sesión", font=("Arial", 11, "bold "), width = 12, command=Validar_login)
boton1.place(x=80, y=390)

boton2 = Button(ventana, text="Registrarme", font=("Arial", 11, "bold"), width = 10, command=abrir_ventana_registro)
boton2.place(x=220, y=390)

ventana.mainloop()