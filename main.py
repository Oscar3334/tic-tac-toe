from tkinter import *
from copy import copy

class Game:
    def __init__(self, root, isAi=False):
        self.isAi = isAi
        self.frm = Frame(root, background = "white")
        self.frm.grid()
        self.buttonGrid = [
            [Button(self.frm, width = 2, height = 0, relief=FLAT
                , font = ("New Times Roman", 80, "bold")
                , borderwidth = 1, background = "white"
                , highlightthickness = 1)
                for j in range(3)] for i in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttonGrid[i][j].grid(column = j, row = i, padx=5, pady=5)
                self.buttonGrid[i][j].config(
                    command = (lambda a,b: lambda: self.move(a,b))(i,j))
        self.reset()
        
    def reset(self):
        self.isXmove = True
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
        if self.isAi and not self.isXmove:
            self.move(*self.findNextMove())

    def checkWin(self, grid=None) -> int:
        if grid == None:
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
    
    def findNextMove(self) -> tuple[int, int]:
        grid = copy(self.grid)
        func = None
        candidate = None
        xMove = self.isXmove
        print("max" if xMove else "min")
        if xMove:
            candidate = (-1, -1, -1000)
            func = lambda *x: max(x, key=lambda a: a[2])
        else:
            candidate = (-1, -1, 1000)
            func = lambda *x: min(x, key=lambda a: a[2])
        for i in range(3):
            for j in range(3):
                if grid[i][j] != 0: 
                    print("X", end = " ")
                    continue
                grid[i][j] = 1 if xMove else 2
                candidate = func(candidate, (i, j, (e:=self.minimax(grid, xMove, not xMove))))
                grid[i][j] = 0
                print(e, end = " ")
            print("")
        print(candidate)
        return candidate[:2]
    
    def minimax(self, grid, isMin, isXmove) -> int:
        state = self.checkWin()
        if state != 0:
            return (0, 1, -1, 0)[state]
        func = min if isMin else max
        candidate = -func(1000, -1000)
        #print(f"{grid} {candidate} {isMin} ")
        count = 0
        for i in range(3):
            for j in range(3):
                if grid[i][j] != 0:
                    continue
                count += 1
                grid[i][j] = 1 if isXmove else 2
                candidate = func(candidate, (e:=self.minimax(grid, not isMin, not isXmove)))
                grid[i][j] = 0
                #print(e, end=" ")
            #print("")
        if count == 0:
            return 0
        return candidate

root = Tk()
root.config(background = "white")
game = Game(root, True)
root.mainloop()
