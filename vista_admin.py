from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from construir_tabla import construir_tabla
from conexion import MySQLConexion
from centrar_ventana import Centrar_Ventana

def Abrir_dashboard_administrador(administrador):

    def limpiar_frame():
        for widget in contenido.winfo_children():
            widget.destroy()

    def mostrar_registrar():
        limpiar_frame()
        
        campos = ["Nombre", "Descripción", "Genero", "Tema",
                  "Conductor", "Duración", "Horario", "Plataforma"]
        
        entradas = {}

        Label(contenido, text="").pack(pady=5)

        # Crear las entradas para cada campo
        for campo in campos:
            Label(contenido, text=campo + ":", font=("Arial", 11, "bold")).pack()
            entry = Entry(contenido, width=40, font=11)
            entry.pack(pady=5)
            entradas[campo] = entry

        # Botón para registrar el programa
        boton_registrar = Button(contenido, font=("Arial", 11, "bold "), text="Registrar Programa", command =  lambda: Registrar_Programa(entradas))
        boton_registrar.pack(pady=(20,10))

    def Registrar_Programa(entradas):
        datos = {campo: entry.get().strip() for campo, entry in entradas.items()}

        # Verificar que los campos no estén vacíos
        for campo, valor in datos.items():
            if not valor:
                messagebox.showwarning("Cuidado...", f"\nEl campo '{campo}' es obligatorio")
                return

        try:
            conexion = MySQLConexion().ObtenerConexion()
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO programas (nombre, descripcion, genero, tema, conductor, duracion, horario, plataforma)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (datos["Nombre"], datos["Descripción"], datos["Genero"], datos["Tema"], datos["Conductor"],
                  datos["Duración"], datos["Horario"], datos["Plataforma"]))

            conexion.commit()
            conexion.close()
            cursor.close()
            messagebox.showinfo("Programa registrado con éxito", "¡El programa se ha registrado correctamente!")
            mostrar_programas()

            for entry in entradas.values():
                entry.delete(0, END)

        except Exception as e:
            messagebox.showerror("Error...", f"\nNo se pudo registrar el programa\n{e}")

    def mostrar_programas():
        limpiar_frame()
        Label(contenido, text="Programas Registrados", font=("Arial", 11, "bold")).pack(pady=10)

        columnas_bd = ["id",  "nombre", "descripcion", "genero", "tema", "conductor", "duracion", "horario", "plataforma"]
        columnas_vista = ["id",  "Nombre", "Descripción", "Género", "Tema", "Conductor", "Duración", "Horario", "Plataforma"]

        #cargar los datos desde mysql
        try:
            conexion = MySQLConexion().ObtenerConexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, descripcion, genero, tema, conductor, duracion, horario, plataforma FROM programas")
            programas = cursor.fetchall()
            cursor.close()
            conexion.close()

            tabla = construir_tabla(contenido, columnas_vista, programas)

        except Exception as e:
            messagebox.showerror("Error...\n", f"No se pudo cargar los programas\n{e}")
            return
        
        #botones de modificar y eliminar
        botones = Frame(contenido)
        botones.pack(pady=10)

        Button(botones, text="Modificar", font=("Arial", 11, "bold") , command=lambda: editar_elemento(tabla, "programas", columnas_bd)).pack(side=LEFT, padx=10)
        Button(botones, text="Eliminar", font=("Arial", 11, "bold") , command=lambda: eliminar_elemento(tabla, "programas")).pack(side=LEFT, padx=10)

    def editar_elemento(tabla, nombre_tabla, columnas):
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Selecciona uno", "Por favor selecciona un elemento para editar.")
            return

        valores = tabla.item(seleccionado)["values"]
        id_elemento = valores[0]

        ventana_editar = Toplevel()
        ventana_editar.title("Modificar Programa")
        ventana_editar.resizable(0,0)
        Centrar_Ventana(ventana_editar, 380, 580)
        entradas = []

        for i in range(1, len(columnas)):  # Empezamos en 1 para saltar el ID
            Label(ventana_editar, text=columnas[i], font=("Arial", 11, "bold")).pack()
            entrada = Entry(ventana_editar, font=("Arial", 11), width=40)
            entrada.insert(0, valores[i])
            entrada.pack(pady=10)
            entradas.append(entrada)

        def guardar():
            nuevos_valores = [entrada.get().strip() for entrada in entradas]
            if any(val == "" for val in nuevos_valores):
                messagebox.showwarning("Campos vacíos", "No puedes dejar campos vacíos.")
                return

            try:
                conexion = MySQLConexion().ObtenerConexion()
                cursor = conexion.cursor()

                set_clause = ", ".join([f"{columnas[i]} = %s" for i in range(1, len(columnas))])
                sql = f"UPDATE {nombre_tabla} SET {set_clause} WHERE id = %s"
                cursor.execute(sql, nuevos_valores + [id_elemento])
                conexion.commit()
                cursor.close()
                conexion.close()
                ventana_editar.destroy()

                messagebox.showinfo("Éxito", "Registro actualizado correctamente.")
                mostrar_programas() if nombre_tabla == "programas" else mostrar_usuarios()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo editar.\n{e}")

        Button(ventana_editar, text="Aplicar cambio", command=guardar, font=("Arial", 11, "bold")).pack(pady=10)

    def eliminar_elemento(tabla, nombre_tabla):
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Selecciona uno", "Selecciona un elemento para eliminar.")
            return

        valores = tabla.item(seleccionado)["values"]
        id_elemento = valores[0]

        confirmar = messagebox.askyesno("Confirmar", f"¿Eliminar registro con ID {id_elemento}?")
        if confirmar:
            try:
                conexion = MySQLConexion().ObtenerConexion()
                cursor = conexion.cursor()
                cursor.execute(f"DELETE FROM {nombre_tabla} WHERE id = %s", (id_elemento,))
                conexion.commit()
                cursor.close()
                conexion.close()
                tabla.delete(seleccionado)
                messagebox.showinfo("Eliminado", "El registro fue eliminado.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar.\n{e}")


    def mostrar_usuarios():
        limpiar_frame()
        Label(contenido, text="Ver usuarios registrados", font=("Arial", 11, "bold")).pack()

        columnas_bd = ["id",  "usuario", "contraseña", "tipo_usuario"]
        columnas_vista = ["id",  "Usuario", "Contraseña", "Rol"]

        #cargar los datos desde mysql
        try:
            conexion = MySQLConexion().ObtenerConexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT id, usuario, contraseña, tipo_usuario FROM usuarios")
            usuarios = cursor.fetchall()
            cursor.close()
            conexion.close()

            tabla = construir_tabla(contenido, columnas_vista, usuarios)

        except Exception as e:
            messagebox.showerror("Error...\n", f"No se pudo cargar los usuarios\n{e}")
            return
        
        #botones de modificar y eliminar
        botones = Frame(contenido)
        botones.pack(pady=10)

        Button(botones, text="Modificar", font=("Arial", 11, "bold") , command=lambda: editar_elemento(tabla, "usuarios", columnas_bd)).pack(side=LEFT, padx=10)
        Button(botones, text="Eliminar", font=("Arial", 11, "bold") , command=lambda: eliminar_elemento(tabla, "usuarios")).pack(side=LEFT, padx=10)

    def cerrar_sesion():
        ventana.destroy()


    # Creación de la ventana
    ventana = Tk()
    ventana.title("Dashboard Administrador")
    ventana.resizable(0, 0)
    Centrar_Ventana(ventana, 1120, 550)

    # Barra lateral izquierda
    menu_izq = Frame(ventana, width=200, height=550, bd=1, relief="solid")
    menu_izq.pack(side=LEFT, fill=Y)
    menu_izq.pack_propagate(False)

    # Imagen
    imagen = Image.open("Imagen/logo.png")
    imagen = imagen.resize((130, 130))
    imagen_tk = ImageTk.PhotoImage(imagen)

    label = Label(menu_izq, image=imagen_tk)
    label.pack(pady=20)
    label.image = imagen_tk

    # Iconos
    icono1 = PhotoImage(file="Imagen/nuevo_programa.png")
    icono2 = PhotoImage(file="Imagen/ver_programa.png")
    icono3 = PhotoImage(file="Imagen/ver_usuario.png")
    icono4 = PhotoImage(file="Imagen/salir.png")

    # Botones
    boton1 = Button(menu_izq, text="Registrar Programa", image=icono1, compound="left", command=mostrar_registrar, font=("Arial", 11, "bold"), padx=10, pady=10)
    boton1.pack(fill=X, pady=13)

    boton2 = Button(menu_izq, text="Ver Programas", image=icono2, compound="left", command=mostrar_programas, font=("Arial", 11, "bold"), padx=10, pady=10)
    boton2.pack(fill=X, pady=13)

    boton3 = Button(menu_izq, text="Ver usuarios", image=icono3, compound="left", command=mostrar_usuarios, font=("Arial", 11, "bold"), padx=10, pady=10)
    boton3.pack(fill=X, pady=13)

    boton4 = Button(menu_izq, text="Cerrar sesión", image=icono4, compound="left", command=cerrar_sesion, font=("Arial", 11, "bold"), padx=10, pady=10)
    boton4.pack(fill=X, pady=30)

    # Frame derecho
    contenido = Frame(ventana)
    contenido.pack(side=RIGHT, expand=True, fill=BOTH)

    ventana.mainloop()