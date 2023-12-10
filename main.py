from tkinter import *
from tkinter import ttk

class Game:
    def __init__(self, root):
        self.frm = ttk.Frame(root)
        self.frm.grid()
        self.buttonGrid = [
            [Button(self.frm, width = 2, height = 1, relief=SUNKEN
                , font = ("New Times Roman", 80, "bold"))
                for j in range(3)] for i in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttonGrid[i][j].grid(column = j, row = i)
                self.buttonGrid[i][j].config(
                    command = (lambda a,b: lambda: self.move(a,b))(i,j))
        self.reset()
        
    def reset(self):
        isXmove = True
        self.grid = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        self.movesLeft = 9
        for row in self.buttonGrid:
            for btn in row:
                btn.config(text=" ")

    def move(self, row, col):
        if self.movesLeft == 0:
            self.reset()
            return
        if self.grid[row][col] != 0: return
        self.movesLeft -= 1
        if self.isXmove:
            self.buttonGrid[row][col].config(text="X")
            self.grid[row][col] = 1
        else:
            self.buttonGrid[row][col].config(text="O")
            self.grid[row][col] = 2
        if (e:=self.checkWin()) != 0:
            if e == 1:
                print("X wins!")
                self.movesLeft = 0
            elif e == 2:
                print("O wins!")
                self.movesLeft = 0
            else:
                print("Tie! No winner.")
        self.isXmove = not self.isXmove

    def checkWin(self) -> int:
        grid = self.grid
        for i in range(3):
            if grid[i][i] == 0:
                continue
            if grid[0][i] == grid[1][i] and grid[1][i] == grid[2][i]:
                return grid[0][i]
            if grid[i][0] == grid[i][1] and grid[i][1] == grid[i][2]:
                return grid[i][0]
        if grid[0][0] == grid[1][1] and grid[1][1] == grid[2][2] \
            or grid[2][0] == grid[1][1] and grid[1][1] == grid[0][2]:
                return grid[1][1]
        if self.movesLeft == 0:
            return 4
        return 0

root = Tk()
game = Game(root)
root.mainloop()
