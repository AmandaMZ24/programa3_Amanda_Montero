# JUEGO SUDOKU. ELABORADO POR AMANDA MONTERO Z. FECHA DE ENTREGA: 1/12/2021


import random
from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM, Toplevel, Menu, messagebox
from tkinter.constants import DISABLED
import webbrowser
import time
import pickle

# ventana de menu
ventana1 = Tk()
ventana1.title("Sudoku")
ventana1.geometry("500x50")
ventana1.resizable(False, False)

#menu
menubar = Menu(ventana1)




facil = {1: ["806705000",
     "025380690",
     "700000020",
     "003817000",
     "679000418",
     "000946300",
     "060000004",
     "087094250",
     "000502706"],
 2: ["600009780",
     "030702490",
     "090300060",
     "023817950",
     "000000000",
     "061524370",
     "070003040",
     "046108030",
     "089200007"],
 3: ["531080000",
     "984500063",
     "260009518",
     "019800602",
     "308100459",
     "056920070",
     "192750006",
     "873610025",
     "605390007"]}

MARGIN = 20  # Pixels around the board
SIDE = 50  # Width of every board cell.
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9  # Width and height of the whole board


class SudokuError(Exception):
    """
    An application specific error.
    """
    pass


class SudokuUI(Frame):
    """
    The Tkinter UI, responsible for drawing the board and accepting user input.
    """
    def __init__(self, parent, game):
        self.game = game
        Frame.__init__(self, parent)
        self.parent = parent

        self.row, self.col = -1, -1

        self.__initUI()
        

    def __initUI(self):
        global jugadas
        global x
        global y
        global juego

        juego = True

        self.parent.title("Sudoku")
        self.pack()
        self.canvas = Canvas(self,
                             width=1000,
                             height=650)
        self.canvas.pack()

        
        clear_button = Button(self, bg="#56B2B0",
                              text="BORRAR JUEGO",
                              command=self.__clear_answers)
        clear_button.configure(width=20, height=2, font=("Comic Sans MS", 10, "bold"))
        clear_button.place(x=250, y=500)

        deshacer_boton = Button(self, bg="#00FFF9", width=20, height=2, font=("Comic Sans MS", 10, "bold"),
                                text="DESHACER JUGADA",
                                command=self.deshacer_mov)
        deshacer_boton.place(x=450, y=500)

        rehacer_boton = Button(self, bg="#00FFF9", width=20, height=2, font=("Comic Sans MS", 10, "bold"),
                                text="REHACER JUGADA")
        rehacer_boton.place(x=650, y=500)


        # guardar partida

        # def guardar_juego1():
        #     archivo_juego = open("sudoku2021jugadas.dat", "wb")
        #     pickle.dump(self.matrix, archivo_juego)
        #     opcion = messagebox.askquestion(
        #         title="SALIR", message="¿Va a continuar jugando? SI/NO")
        #     if opcion == "yes":
        #         pass
        #     elif opcion == "no":
        #         self.destroy()
        guardar_boton = Button(self, bg="#CFCFCF", width=20, height=2, font=("Comic Sans MS", 10, "bold"),
                               text="GUARDAR PARTIDA"
                               )
        guardar_boton.place(x=250, y=570)

        # cargar partida
        # def cargar_juego1():
        #     archivo_juego = open("sudoku2021jugadas.dat", "rb")
        #     self.matrix = pickle.load(archivo_juego)
        #     self.update()
                

        cargar_boton = Button(self, bg="#CFCFCF", width=20, height=2, font=("Comic Sans MS", 10, "bold"),
                              text="CARGAR PARTIDA")
        cargar_boton.place(x=450, y=570)


        
    
        self.__draw_grid()
        self.__draw_puzzle()

        jugadas = []

        x = self.canvas.bind("<Button-1>", self.__cell_clicked)
        y = self.canvas.bind("<Key>", self.__key_pressed)
        
        
        

    def __draw_grid(self):
        """
        Draws grid divided with blue lines into 3x3 squares
        """
        for i in range(10):
            color = "#9D0000" if i % 3 == 0 else "gray"

            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color, width=3)

            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color, width=3)

    def __draw_puzzle(self):
        self.canvas.delete("numbers")
        for i in range(9):
            for j in range(9):
                answer = self.game.puzzle[i][j]
                if answer != 0:
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2
                    original = self.game.start_puzzle[i][j]
                    color = "black" if answer == original else "sea green"
                    self.canvas.create_text(
                        x, y, text=answer, tags="numbers", fill=color, font=("Comic Sans MS", 16)
                    )

    def __draw_cursor(self):
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                outline="red", tags="cursor"
            )

    def __draw_victory(self):
        # create a oval (which will be a circle)
        x0 = y0 = MARGIN + SIDE * 2
        x1 = y1 = MARGIN + SIDE * 7
        self.canvas.create_oval(
            x0, y0, x1, y1,
            tags="victory", fill="dark orange", outline="orange"
        )
        # create text
        x = y = MARGIN + 4 * SIDE + SIDE / 2
        self.canvas.create_text(
            x, y,
            text="¡EXCELENTE! \nJUEGO COMPLETADO", tags="victory",
            fill="white", font=("Arial", 16)
        )

    def __cell_clicked(self, event):
        global jugadas
        global row
        global col
        if self.game.game_over:
            return
        x, y = event.x, event.y
        if (MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN):
            self.canvas.focus_set()

            # get row and col numbers from x,y coordinates
            row, col = int((y - MARGIN) / SIDE), int((x - MARGIN) / SIDE)

            # if cell was selected already - deselect it
            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            elif self.game.puzzle[row][col] == 0:
                self.row, self.col = row, col
        else:
            self.row, self.col = -1, -1

        self.__draw_cursor()
        jugadas.append([row, col])
        
        #print(jugadas)

    def __key_pressed(self, event):
        global jugadas
        global char
        if self.game.game_over:
            return
        if self.row >= 0 and self.col >= 0 and event.char in "1234567890":
            self.game.puzzle[self.row][self.col] = int(event.char)
            self.col, self.row = -1, -1
            self.__draw_puzzle()
            self.__draw_cursor()
            if self.game.check_win():
                self.__draw_victory()
        jugadas[-1].append(event.char)

        print(jugadas)

    def __clear_answers(self):
        self.game.start()
        self.canvas.delete("victory")
        self.__draw_puzzle()

    def deshacer_mov(self):
        global jugadas
        
        self.canvas.delete("numbers")
        for i in range(jugadas[-1][0]):
            for j in range(jugadas[-1][1]):
                answer = ""
                if answer != 0:
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2
                    original = self.game.start_puzzle[i][j]
                    color = "black" if answer == original else "sea green"
                    self.canvas.create_text(
                        x, y, text=answer, tags="numbers", fill=color, font=("Comic Sans MS", 16)
                    )
        jugadas.pop(-1)
    

class SudokuBoard(object):
    """
    Sudoku Board representation
    """
    def __init__(self, board_file):
        self.board = self.__create_board(board_file)

    def __create_board(self, board_file):
        board = []
        for line in board_file:
            line = line.strip()
            if len(line) != 9:
                raise SudokuError(
                    "Each line in the sudoku puzzle must be 9 chars long."
                )
            board.append([])

            for c in line:
                if not c.isdigit():
                    raise SudokuError(
                        "Valid characters for a sudoku puzzle must be in 0-9"
                    )
                board[-1].append(int(c))

        if len(board) != 9:
            raise SudokuError("Each sudoku puzzle must be 9 lines long")
        return board


class SudokuGame(object):
    """
    A Sudoku game, in charge of storing the state of the board and checking
    whether the puzzle is completed.
    """
    def __init__(self, board_file):
        self.board_file = board_file
        self.start_puzzle = SudokuBoard(board_file).board

    def start(self):
        self.game_over = False
        self.puzzle = []
        for i in range(9):
            self.puzzle.append([])
            for j in range(9):
                self.puzzle[i].append(self.start_puzzle[i][j])
        self.juego=False

    def check_win(self):
        for row in range(9):
            if not self.__check_row(row):
                return False
        for column in range(9):
            if not self.__check_column(column):
                return False
        for row in range(3):
            for column in range(3):
                if not self.__check_square(row, column):
                    return False
        self.game_over = True
        return True

    def __check_block(self, block):
        return set(block) == set(range(1, 10))

    def __check_row(self, row):
        return self.__check_block(self.puzzle[row])

    def __check_column(self, column):
        return self.__check_block(
            [self.puzzle[row][column] for row in range(9)]
        )

    def __check_square(self, row, column):
        return self.__check_block(
            [
                self.puzzle[r][c]
                for r in range(row * 3, (row + 1) * 3)
                for c in range(column * 3, (column + 1) * 3)
            ]
        )


class Jugadas_hechas:
    def __init__(self, row, col, elemento):
        self.fila = row
        self.columna = col
        self.elemento = elemento

    def obtener_jugada_hecha(self):
        return self.fila, self.columna, self.elemento

# clase para implementar función rehacer jugadas


class Jugadas_eliminadas:
    def __init__(self, fila, columna, elemento):
        self.fila = fila
        self.columna = columna
        self.elemento = elemento

    def obtener_jugada_eliminada(self):
        return self.fila, self.columna, self.elemento


# definición de las pilas
pila_jugadas_hechas = []
pila_jugadas_eliminadas = []

# ejemplo de jugadas hechas: cada jugada hecha se agrega a la pila
j = Jugadas_hechas(3, 6, 9)
pila_jugadas_hechas.append(j)
j = Jugadas_hechas(2, 6, 4)
pila_jugadas_hechas.append(j)
j = Jugadas_hechas(1, 2, 2)
pila_jugadas_hechas.append(j)

# seleccionamos botón DESHACER JUGADA
ultima_jugada = pila_jugadas_hechas.pop()


ultima_jugada = pila_jugadas_hechas.pop()


# las jugadas eliminadas se guardan en la pila de jugadas elimiinadas en caso
# de que seleccionemos botón REHACER JUGADA

je = Jugadas_eliminadas(
    ultima_jugada.fila, ultima_jugada.columna, ultima_jugada.elemento)
pila_jugadas_eliminadas.append(je)

# seleccionamos botón REHACER JUGADA
ultima_jugada = pila_jugadas_eliminadas.pop()
#print(ultima_jugada.obtener_jugada_eliminada())

#iniciar juego
juego = False
def __iniciar_juego():
    global juego
    juego = True


def jugar():
    global iniciar_boton
    if __name__ == '__main__':
        x = random.choice(list(facil.keys()))
        board_name = facil[x]
        game = SudokuGame(board_name)
        game.start()

        root = Toplevel(ventana1)
        SudokuUI(root, game)
        root.geometry("1000x650")
        root.resizable(False, False)

        # iniciar partida
        iniciar_boton = Button(root, bg="#BB00C9", width=20, height=2, font=("Comic Sans MS", 10, "bold"),
                            text="INICIAR JUEGO", command=__iniciar_juego())
        iniciar_boton.place(x=50, y=500)


        root.mainloop()


def showMessage(titulo, mensaje):
    messagebox.showinfo(titulo, mensaje)


# JUGAR
jugar_menu = Menu(menubar, tearoff=0)

jugar_menu.add_command(label="Jugar", command=jugar)

menubar.add_cascade(label="Jugar", menu=jugar_menu)


# CONFIGURAR
configurar_menu = Menu(menubar, tearoff=0)
configurar_menu.add_command(
    label="Reloj", command=lambda: showMessage("Reloj", "*agregar opciones*"))
configurar_menu.add_command(label="Desplegar mejor jugador", command=lambda: showMessage(
    "Desplegar mejor jugador", "*agregar opciones*"))
menubar.add_cascade(label="Configurar", menu=configurar_menu)


# AYUDA
def ayuda():
    webbrowser.open_new('manual_de_usuario_2048.pdf')


help_menu = Menu(menubar, tearoff=0)

help_menu.add_command(label="Manual de usuario",
                      command=lambda: ayuda())

menubar.add_cascade(label="Ayuda", menu=help_menu)


# ACERCA DE
info_menu = Menu(menubar, tearoff=0)

info_menu.add_command(label="Acerca de",
                      command=lambda: showMessage("Acerca de", "Programa: Sudoku. \n Versión: 1.7.1.\n Fecha de creación: 1/12/2021 \n Elaborado por: Amanda Montero Z."))

menubar.add_cascade(label="Acerca de", menu=info_menu)


def salir1():
    opcion = messagebox.askquestion(
        title="SALIR", message="¿Está seguro de cerrar el juego? SI/NO")
    if opcion == "yes":
        ventana1.destroy()
    elif opcion == "no":
        pass
# SALIR


exit_menu = Menu(menubar, tearoff=0)

exit_menu.add_command(label="Salir",
                      command=salir1)

menubar.add_cascade(label="Salir", menu=exit_menu)
ventana1.config(menu=menubar)

ventana1.mainloop()
