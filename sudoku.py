########################
#       MODULOS        #
########################
import tkinter as tk
from tkinter import StringVar, messagebox
import random
import time
import pickle
import pygame
import webbrowser

########################
#    PROGRAMA FUENTE   #
########################

# VENTANA MENU
ventana1 = tk.Tk()
ventana1.title("Sudoku")
ventana1.geometry("500x50")
ventana1.resizable(False, False)


# Para iniciar la partida
inicio = False

# colores y letras GUI


def juego_principal():

    ventana = tk.Toplevel(ventana1)
    ventana.title("Sudoku")
    ventana.geometry("750x650")
    ventana.main_grid = tk.Frame(
        ventana, bd=3, width=270, height=220)
    ventana.main_grid.place(x=170, y=80)
    ventana.resizable(False, False)
    pygame.mixer.init()

    # TÍTULO
    texto_2048 = "Sudoku"
    etiqueta_titulo = tk.Label(
        ventana, text=texto_2048, font=("Berlin Sans FB", 35))
    etiqueta_titulo.place(x=270, y=7)

    # NOMBRE JUGADOR
    texto_nombre = "Nombre del jugador"
    etiqueta_nombre = tk.Label(ventana, text=texto_nombre)
    etiqueta_nombre.place(x=500, y=18)

    nombre = tk.StringVar()
    nombre.set("")

    nombreEntry = tk.Entry(ventana, width=15, font=("Arial", 18, ""),
                           textvariable=nombre)
    nombreEntry.place(x=500, y=38)
    print(nombre.get())

    # TIMER
    hora = StringVar()
    minuto = StringVar()
    segundo = StringVar()

    hora.set("00")
    minuto.set("00")
    segundo.set("00")

    horaEntry = tk.Entry(ventana, width=3, font=("Arial", 18, ""),
                         textvariable=hora)
    horaEntry.place(x=20, y=20)

    minutoEntry = tk.Entry(ventana, width=3, font=("Arial", 18, ""),
                           textvariable=minuto)
    minutoEntry.place(x=90, y=20)

    segundoEntry = tk.Entry(ventana, width=3, font=("Arial", 18, ""),
                            textvariable=segundo)
    segundoEntry.place(x=140, y=20)

    def submit():
        global temp
        try:
            temp = int(hora.get())*3600 + int(minuto.get()) * \
                60 + int(segundo.get())
        except:
            print("Please input the right value")

        while temp > -1:
            mins, secs = divmod(temp, 60)
            horas = 0
            if mins > 60:
                horas, mins = divmod(mins, 60)

            hora.set("{0:2d}".format(horas))
            minuto.set("{0:2d}".format(mins))
            segundo.set("{0:2d}".format(secs))

            ventana.update()
            time.sleep(1)

            if (temp == 0):
                opcion = messagebox.askquestion(
                    "Tiempo terminado", "Tiempo expirado. ¿Desea continuar la misma partida: SI O NO?.")

                if opcion == "yes":
                    pass
                elif opcion == "no":
                    partida_nueva()

            temp -= 1

    btn = tk.Button(ventana, text='Set Time Countdown', bd='5',
                    command=submit)
    btn.place(x=20, y=45)

    # casillas

    # Update GUI

    # MOVIMIENTOS

    # if inicio == False:
    #     error1 = messagebox.showwarning(
    #         title="No ha iniciado la partida", message="Para iniciar el juego seleccione el botón correspondiente.")
    #     if error1 == "Ok":
    #         pass
    # x = nombre.get()
    # if x == "":
    #     error = messagebox.showwarning(
    #         title="No ha ingresado su nombre.", message="Para iniciar el juego ingrese su nombre.")
    #     if error == "Ok":
    #         pass

    # check if any moves are possible

    def sonido():
        pygame.mixer.music.load("K3RTHA7-game-win-horns.mp3")
        pygame.mixer.music.play(loops=0)

    # check if game is over

    def salir():
        opcion = messagebox.askquestion(
            title="SALIR", message="¿Está seguro de terminar el juego? SI/NO")
        if opcion == "yes":
            ventana.destroy()
        elif opcion == "no":
            pass

    # funciones botones (ventana juego)

    # INICIAR PARTIDA

    def iniciar_partida1():
        global inicio
        inicio = True
        if temp != 0:
            submit()

    # PARTIDA NUEVA

    def partida_nueva():
        global inicio

        if inicio == False:
            messagebox.showinfo(title="No se ha iniciado el juego",
                                message="No se ha iniciado el juego")
        else:
            mensaje = messagebox.askquestion(
                title="Terminar partida actual", message="¿Está seguro de terminar la partida actual? SI/NO")
            if mensaje == "yes":
                ventana.destroy()
                inicio = False
                juego_principal()
            else:
                pass

    # GUARDAR JUEGO

    def guardar_juego1():
        archivo_juego = open("2048juegoactual.dat", "wb")
        pickle.dump(ventana.matrix, archivo_juego)
        opcion = messagebox.askquestion(
            title="SALIR", message="¿Va a continuar jugando? SI/NO")
        if opcion == "yes":
            pass
        elif opcion == "no":
            ventana.destroy()

    # CARGAR JUEGO

    def cargar_juego1():
        if inicio == False:
            archivo_juego = open("2048juegoactual.dat", "rb")
            ventana.matrix = pickle.load(archivo_juego)
            ventana.update()
        else:
            x = messagebox.showinfo(
                title="ERROR", message="Ya hay una partida en curso")

    # TOP 10
    t10 = {"Amanda": "00:20:37"}

    def top10():
        x = messagebox.showinfo(title="MEJORES JUGADORES", message=t10)

    # menú principal (JUGAR)

    # INICIAR PARTIDA
    iniciar_partida = tk.Button(ventana, bg="#82FF4C", width=10, height=2, font=("Comic Sans MS", 10, "bold"), text='INICIAR \n PARTIDA', bd='5',
                                command=iniciar_partida1)
    iniciar_partida.place(x=20, y=500)

    # PARTIDA NUEVA
    nueva_partida = tk.Button(ventana, bg="#4CFFC0", width=10, height=2, font=("Comic Sans MS", 10, "bold"), text='PARTIDA \n NUEVA', bd='5',
                              command=partida_nueva)
    nueva_partida.place(x=165, y=500)

    # SALIR
    boton_salir = tk.Button(ventana, bg="#FF4D4D", width=10, height=2, font=("Comic Sans MS", 10, "bold"), text='SALIR', bd='5',
                            command=salir)
    boton_salir.place(x=310, y=500)

    # VER TOP 10
    boton_top10 = tk.Button(ventana, bg="#FFE54D", width=10, height=2, font=("Comic Sans MS", 10, "bold"), text='TOP \n 10', bd='5',
                            command=top10)
    boton_top10.place(x=455, y=500)

    #GUARDAR JUEGO
    btn_guardar = tk.Button(ventana, bg="#1EC9FF", width=10, height=2, font=("Comic Sans MS", 10, "bold"), text='GUARDAR \n JUEGO', bd='5',
                            command=guardar_juego1)
    btn_guardar.place(x=165, y=575)

    # CARGAR JUEGO
    btn_cargar = tk.Button(ventana, bg="#834FFF", width=10, height=2, font=("Comic Sans MS", 10, "bold"), text='CARGAR \n PARTIDA', bd='5',
                           command=cargar_juego1)
    btn_cargar.place(x=310, y=575)

    ventana.mainloop()

# BARRA DE MENU PRINCIPAL


def showMessage(titulo, mensaje):
    messagebox.showinfo(titulo, mensaje)


menubar = tk.Menu(ventana1)


# JUGAR
jugar_menu = tk.Menu(menubar, tearoff=0)

jugar_menu.add_command(label="Jugar",
                       command=juego_principal)

menubar.add_cascade(label="Jugar", menu=jugar_menu)


# CONFIGURAR
configurar_menu = tk.Menu(menubar, tearoff=0)
configurar_menu.add_command(
    label="Reloj", command=lambda: showMessage("Reloj", "*agregar opciones*"))
configurar_menu.add_command(label="Desplegar mejor jugador", command=lambda: showMessage(
    "Desplegar mejor jugador", "*agregar opciones*"))
menubar.add_cascade(label="Configurar", menu=configurar_menu)


# AYUDA
def ayuda():
    webbrowser.open_new('manual_de_usuario_2048.pdf')


help_menu = tk.Menu(menubar, tearoff=0)

help_menu.add_command(label="Manual de usuario",
                      command=lambda: ayuda())

menubar.add_cascade(label="Ayuda", menu=help_menu)


# ACERCA DE
info_menu = tk.Menu(menubar, tearoff=0)

info_menu.add_command(label="Acerca de",
                      command=lambda: showMessage("Acerca de", "Programa: Juego 2048. \n Versión: 1.0.0.\n Fecha de creación: 07/11/2021 \n Elaborado por: Amanda Montero Z."))

menubar.add_cascade(label="Acerca de", menu=info_menu)


def salir1():
    opcion = messagebox.askquestion(
        title="SALIR", message="¿Está seguro de cerrar el juego? SI/NO")
    if opcion == "yes":
        ventana1.destroy()
    elif opcion == "no":
        pass
# SALIR


exit_menu = tk.Menu(menubar, tearoff=0)

exit_menu.add_command(label="Salir",
                      command=salir1)

menubar.add_cascade(label="Salir", menu=exit_menu)
ventana1.config(menu=menubar)

# INFO TIMER “2048configuración.dat”
# INFO TOP 10 “2048top10.dat”.


ventana1.mainloop()
