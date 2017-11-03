DARK = 'X'
LIGHT = 'O'
EMPTY = '.'
import sys
sys.path.append('./')

class gameBoard:

    def __init__(self, width = 8):
        self.width = width

    def startState(self):
        self.board = [[LIGHT for x in range(self.width)]for y in range(self.width)]
        for j in range (len(self.board)):
            if j % 2 :
                i = 1
            else:
                i = 0
            while i < len(self.board) :
                self.board[j][i] = DARK
                i += 2
        return self.board

    def drawBoard(self):
        for row in self.board:
            for col in row:
                print col,
            print

    def updateBoard(self, remove, add, identity):
        self.board[remove[0]-1][remove[1]-1] = EMPTY
        if add:
            self.board[add[0]-1][add[1]-1] = identity
            #moving south
            if remove[0] < add[0]:
                i = remove[0]
                while (i < add[0]-1):
                    self.board[i][add[1]-1] = EMPTY
                    i += 1
            #moving north
            if remove[0] > add[0]:
                i = remove[0]-2
                while (i > add[0]-1):
                    self.board[i][add[1]-1] = EMPTY
                    i -= 1
            #moving east
            if remove[1] < add[1]:
                i = remove[1]
                while(i < add[1]-1):
                    self.board[add[0]-1][i] = EMPTY
                    i += 1
            #moving west
            if remove[1] > add[1]:
                i = remove[1]-2
                while(i > add[1]-1):
                    self.board[add[0]-1][i] = EMPTY
                    i -= 1
        return self.board

    def getGameState(self):
        return self.board

    def getCellInfo (self, position):
        return self.board[position[0]-1][position[1]-1]

    def getEmptyCell(self):
        emptyCells = []
        for i in range (len(self.board)):
            for j in range (len(self.board[0])):
                if self.board[i][j] == EMPTY:
                    position = (i+1, j+1)
                    emptyCells.append(position)
        return emptyCells

    def getDarkCell(self):
        darkCells = []
        for i in range (len(self.board)):
            for j in range (len(self.board[0])):
                if self.board[i][j] == DARK:
                    position = (i+1, j+1)
                    darkCells.append(position)
        return darkCells

    def getLightCell(self):
        lightCells = []
        for i in range (len(self.board)):
            for j in range (len(self.board[0])):
                if self.board[i][j] == LIGHT:
                    position = (i+1, j+1)
                    lightCells.append(position)
        return lightCells
