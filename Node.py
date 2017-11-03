import sys
sys.path.append('./')
class Node:

    def __init__(self, gameBoard, parentNode, level,move):
        self.gameBoard = gameBoard
        self.parentNode = parentNode
        self.level = level
        self.move = move
