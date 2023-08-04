from tkinter import *
from random import *

SCORE = 0
SIZE = 500
GRID_LEN = 4
GRID_PADDING = int(40 / GRID_LEN)
TILES_PER_MOVE = 1

BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
BACKGROUND_COLOR_DICT = {   2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563", \
                            32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72", 256: "#edcc61", \
                            512: "#edc850", 1024: "#edc53f", 2048: "#edc22e", 4096: "#00ff00", \
                            8192: "#00dd00" }
CELL_COLOR_DICT = { 2: "#776e65", 4: "#776e65", 8: "#f9f6f2", 16: "#f9f6f2", \
                    32: "#f9f6f2", 64: "#f9f6f2", 128: "#f9f6f2", 256: "#f9f6f2", \
                    512: "#f9f6f2", 1024: "#f9f6f2", 2048: "#f9f6f2", 4096: "#f9f6f2", \
                    8192: "#f9f6f2" }
for i in range(14, 2048):
    BACKGROUND_COLOR_DICT[2 ** i] = "#00c000"
    CELL_COLOR_DICT[2 ** i] = "#f9f6f2"
    
FONT = ("Verdana", int(80 / GRID_LEN), "bold")

KEY_UP_ALT = "\'\\uf700\'"
KEY_DOWN_ALT = "\'\\uf701\'"
KEY_LEFT_ALT = "\'\\uf702\'"
KEY_RIGHT_ALT = "\'\\uf703\'"
KEY_UNDO_ALT = "\'\\uf704\'"

KEY_UP = "'w'"
KEY_DOWN = "'s'"
KEY_LEFT = "'a'"
KEY_RIGHT = "'d'"
KEY_UNDO = "'u'"
KEY_RESET = "'r'"



def new_game(n):
    if n == 4:
        return [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    matrix = []
    for i in range(n):
        matrix.append([0] * n)
    return matrix



def empty_spaces(mat):
    sum = 0
    for i in range(len(mat)):
        sum = sum + mat[i].count(0)
    return sum

def add_two(mat):
    global TILES_PER_MOVE
    temp = TILES_PER_MOVE
    if empty_spaces(mat) < TILES_PER_MOVE:
        TILES_PER_MOVE = empty_spaces(mat)
    for i in range(TILES_PER_MOVE):
        a = randint(0, len(mat) - 1)
        b = randint(0, len(mat) - 1)
        while mat[a][b] != 0:
            a = randint(0, len(mat) - 1)
            b = randint(0, len(mat) - 1)
        n = randint(0, 100)
        if n > 90:
            mat[a][b] = 4
        else:
            mat[a][b] = 2
    TILES_PER_MOVE = temp
    return mat



def game_state(mat):
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] >= 2048:
                return 'win'
    for i in range(len(mat)-1): 
        for j in range(len(mat[0]) - 1):
            if mat[i][j] == mat[i + 1][j] or mat[i][j + 1] == mat[i][j]:
                return 'not over'
    for i in range(len(mat)): 
        for j in range(len(mat[0])):
            if mat[i][j] == 0:
                return 'not over'
    for k in range(len(mat) - 1): 
        if mat[len(mat) - 1][k] == mat[len(mat) - 1][k + 1]:
            return 'not over'
    for j in range(len(mat)-1): 
        if mat[j][len(mat) - 1] == mat[j + 1][len(mat) - 1]:
            return 'not over'
    return 'lose'



def reverse(mat):
    new = []
    for i in range(len(mat)):
        new.append([])
        for j in range(len(mat[0])):
            new[i].append(mat[i][len(mat[0]) - j - 1])
    return new



def transpose(mat):
    new = []
    for i in range(len(mat[0])):
        new.append([])
        for j in range(len(mat)):
            new[i].append(mat[j][i])
    return new



def cover_up(mat):
    new = []
    for i in range(GRID_LEN):
        new1 = []
        for j in range(GRID_LEN):
            new1.append(0)
        new.append(new1)
    done = False
    for i in range(GRID_LEN):
        count = 0
        for j in range(GRID_LEN):
            if mat[i][j] != 0:
                new[i][count] = mat[i][j]
                if j != count:
                    done = True
                count += 1
    return (new, done)

def merge(mat):
    done = False
    global SCORE
    for i in range(GRID_LEN):
         for j in range(GRID_LEN - 1):
             if mat[i][j] == mat[i][j + 1] and mat[i][j] != 0:
                 mat[i][j] *= 2
                 mat[i][j + 1] = 0
                 done = True
                 SCORE = SCORE + mat[i][j]
    return (mat, done)

def reset(mat):
    global GRID_LEN
    mat = [[0] * GRID_LEN] * GRID_LEN
    done = True
    return mat, done


def up(game):
        # return matrix after shifting up
        game = transpose(game)
        game, done = cover_up(game)
        temp = merge(game)
        game = temp[0]
        done = done or temp[1]
        game = cover_up(game)[0]
        game = transpose(game)
        return (game, done)

def down(game):
        game = reverse(transpose(game))
        game, done = cover_up(game)
        temp = merge(game)
        game = temp[0]
        done = done or temp[1]
        game = cover_up(game)[0]
        game = transpose(reverse(game))
        return (game, done)

def left(game):
        game, done = cover_up(game)
        temp = merge(game)
        game = temp[0]
        done = done or temp[1]
        game = cover_up(game)[0]
        return (game, done)

def right(game):
        game = reverse(game)
        game, done = cover_up(game)
        temp = merge(game)
        game = temp[0]
        done = done or temp[1]
        game = cover_up(game)[0]
        game = reverse(game)
        return (game, done)
    
def undo(game):
        game, done = cover_up(game)
        return (game, done)
    
class GameGrid(Frame):

    def __init__(self):
        Frame.__init__(self)

        self.grid()
        self.master.title('2048')
        self.master.bind("<Key>", self.key_down)

        self.commands = {   KEY_UP: up, KEY_DOWN: down, KEY_LEFT: left, KEY_RIGHT: right, KEY_UNDO: undo, KEY_RESET: reset,
                            KEY_UP_ALT: up, KEY_DOWN_ALT: down, KEY_LEFT_ALT: left, KEY_RIGHT_ALT: right, KEY_UNDO_ALT: undo }

        self.grid_cells = []
        self.init_grid()
        self.init_matrix()
        self.update_grid_cells()
        
        self.mainloop()

    def init_grid(self):
        background = Frame(self, bg = BACKGROUND_COLOR_GAME, width = SIZE, height = SIZE)
        background.grid()
        for i in range(GRID_LEN):
            grid_row = []
            for j in range(GRID_LEN):
                cell = Frame(background, bg = BACKGROUND_COLOR_CELL_EMPTY, width = SIZE / GRID_LEN, height = SIZE / GRID_LEN)
                cell.grid(row = i, column = j, padx = GRID_PADDING, pady = GRID_PADDING)
                t = Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=CENTER, font=FONT, width=8, height=4)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)


    def gen(self):
        return randint(0, GRID_LEN - 1)

    def init_matrix(self):
        self.matrix = new_game(GRID_LEN)

        for i in range(2):
            self.matrix=add_two(self.matrix)

    def update_grid_cells(self):
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(new_number), bg=BACKGROUND_COLOR_DICT[new_number], fg=CELL_COLOR_DICT[new_number])
        self.update_idletasks()
        
    def key_down(self, event):
        key = repr(event.char)
        if key in self.commands:
            self.matrix,done = self.commands[repr(event.char)](self.matrix)
            if done:
                self.matrix = add_two(self.matrix)
                self.update_grid_cells()
                done = False
                if game_state(self.matrix) == 'win':
                  self.grid_cells[1][1].configure(text = "You", bg = BACKGROUND_COLOR_CELL_EMPTY)
                  self.grid_cells[1][2].configure(text = "Win!", bg = BACKGROUND_COLOR_CELL_EMPTY)
                if game_state(self.matrix) == 'lose':
                    self.grid_cells[1][1].configure(text = "You", bg = BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text = "Lose!", bg = BACKGROUND_COLOR_CELL_EMPTY)

    def generate_next(self):
        index = (self.gen(), self.gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (self.gen(), self.gen())
        self.matrix[index[0]][index[1]] = 2

gamegrid = GameGrid()
