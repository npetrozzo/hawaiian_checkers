import sys
sys.path.append("./")
import gameBoard
import copy
from random import randint
import math
from Node import *
import util

DARKPLAYER = 1
LIGHTPLAYER = 0
DARK = 'X'
LIGHT = 'O'
EMPTY = '.'
MAX = 1
MIN = 0
POSSIBLE_FIRST_MOVE_DARK = [(8,8),(1,1),(5,5),(4,4)]

class Player:

    def __init__(self, identity, round ):
        '''
        identity : int (DARKPLAYER or LIGHTPLAYER)
        round : int
        '''
        self.identity = identity
        self.round = round

    def minimax(self, identity, gameBoard, depth_limit, alpha = -9999, beta = 9999, move=None,level=0 ):
        '''
        Minimax algorithm with alpha-beta pruning
        identity : int (DARKPLAYER or LIGHTPLAYER)
        gameBoard : gameBoard
        depth_limit : int
        move : (int,int)
        level : int
        '''    
        if identity:
            cell = DARK
        else:
            cell = LIGHT
        if level == depth_limit:
            return self.evaluation(gameBoard,identity), move
        possibleMoves = self.availableMoves(gameBoard, identity)
        frontier = util.Queue()
        currentState = Node(gameBoard,None,level,move)
        for start in possibleMoves.keys():
            for end in possibleMoves[start]:
                if end:
                    game = copy.deepcopy(gameBoard)
                    game.board = game.updateBoard(start,end,cell)
                    newNode = Node(game, currentState, currentState.level+1,(start,end))
                    frontier.push(newNode)
        if self.tellMinMax(level+1) :
            currentBestValue = -9999
            bestMove = currentState.move
            while not frontier.isEmpty():
                currentNode = frontier.pop()
                if identity:
                    newID = LIGHTPLAYER
                else:
                    newID = DARKPLAYER
                bestValue, move = self.minimax(newID, currentNode.gameBoard,depth_limit, alpha, beta, currentNode.move,currentNode.level)
                move = currentNode.move
                if self.win(currentNode.gameBoard):
                    bestValue = -9999
                if bestValue > alpha:
                    alpha = bestValue
                    bestMove = move
                if alpha >= beta:
                    return beta, bestMove
            return alpha, bestMove
        else:
            currentBestValue = 9999
            bestMove = currentState.move
            while not frontier.isEmpty():
                currentNode = frontier.pop()
                if identity:
                    newID = LIGHTPLAYER
                else:
                    newID = DARKPLAYER
                bestValue, move = self.minimax(newID,currentNode.gameBoard,depth_limit,alpha, beta,currentNode.move,currentNode.level)
                move =currentNode.move
                if self.win(currentNode.gameBoard):
                    bestValue = 9999
                if bestValue < beta:
                    beta = bestValue
                    bestMove = move
                if beta <= alpha:
                    return alpha, bestMove
            return beta, bestMove

    def tellMinMax(self, level):
        '''
        Given level, return FALSE if MIN level, and TRUE if MAX level
        '''
        if level % 2 == 0 and level:
            return MIN
        return MAX

    def evaluation(self, gameBoard,identity):
        '''
        Evaluate a gameBoard based on identity. Evaluation based on remaining dark and light pieces.
        '''
        darkCells = gameBoard.getDarkCell()
        lightCells = gameBoard.getLightCell()
        darkScore = len(darkCells)
        lightScore = len(lightCells)
        if not identity:
            return darkScore - lightScore
        else:
            return lightScore - darkScore
    def generateFirstMove_Dark(self):
        '''
        Generate the first move for DARKPLAYER
        '''
        i = randint(0,3)
        return POSSIBLE_FIRST_MOVE_DARK[i]

    def generateFirstMove_Light(self, darkMove, gameBoard):
        '''
        Generate the first move for LIGHTPLAYER. Must be piece adjacent to the piece DARKPLAYER removed
        '''
        adjs = [1,-1]
        light_moves = []
        light_move = ()
        for adj in adjs:
            if (not darkMove[0] + adj == gameBoard.width + 1) and darkMove[0] + adj:
                light_move = (darkMove[0]+adj, darkMove[1])
                light_moves.append(light_move)
            if (not darkMove[1] + adj == gameBoard.width + 1) and darkMove[1] + adj:
                light_move = (darkMove[0], darkMove[1]+adj)
                light_moves.append(light_move)
        i = randint(0,len(light_moves)-1)
        return light_moves[i]

    def win(self, gameBoard):
        '''
        Given gameBoard, determine who wins.
        '''
        if self.identity:
            newID = LIGHTPLAYER
        else:
            newID = DARKPLAYER
        otherP_possibleMoves = self.availableMoves(gameBoard, newID)
        for move in otherP_possibleMoves.keys():
            if otherP_possibleMoves[move] :
                return False
        return True

    def getEast (self, gameBoard, move):
        if not move[1] == gameBoard.width:
            eastMove = (move[0], move[1]+1)
            return gameBoard.getCellInfo(eastMove), eastMove
        return None, None

    def getWest (self, gameBoard, move):
        if not move[1] == 1:
            westMove = (move[0], move[1]-1)
            return gameBoard.getCellInfo(westMove), westMove
        return None, None

    def getNorth(self, gameBoard, move):
        if not move[0] == 1:
            northMove = (move[0]-1, move[1])
            return gameBoard.getCellInfo(northMove), northMove
        return None, None

    def getSouth(self, gameBoard, move):
        if not move[0] == gameBoard.width:
            southMove = (move[0]+1, move[1])
            return gameBoard.getCellInfo(southMove), southMove
        return None, None

    def availableMoves(self, gameBoard, identity):
        '''
        Given gameBoard and identity, returns dictionary of legal moves.
        '''
        result = {}
        if identity:
            moveable = gameBoard.getDarkCell()
            jumpOver = LIGHT
        else:
            moveable = gameBoard.getLightCell()
            jumpOver = DARK
        for move in moveable:
            eastMove = []
            westMove = []
            northMove = []
            southMove = []
            eastMove = self.jumpToEast(eastMove, gameBoard, identity, jumpOver, move)
            westMove = self.jumpToWest(westMove, gameBoard, identity, jumpOver, move)
            northMove = self.jumpToNorth(northMove, gameBoard, identity, jumpOver, move)
            southMove = self.jumpToSouth(southMove, gameBoard, identity, jumpOver, move)
            result[move] = eastMove + westMove + northMove + southMove
        return result

    def jumpToEast(self, result, gameBoard, identity, jumpOver, moveable):
        game = copy.deepcopy(gameBoard)
        eastCell, eastPosition = self.getEast(gameBoard, moveable)
        #if the cell in the east is opponent's check
        if  eastCell == jumpOver:
            emptyCell, emptyPosition = self.getEast(gameBoard, eastPosition)
            if  emptyCell == EMPTY:
                result.append(emptyPosition)
                game.updateBoard(eastPosition, emptyPosition, identity)
                self.jumpToEast(result, game, identity, jumpOver, emptyPosition)
        return result

    def jumpToWest (self, result, gameBoard, identity, jumpOver, moveable):
        game = copy.deepcopy(gameBoard)
        westCell, westPosition = self.getWest(gameBoard, moveable)
        #if the cell in the east is opponent's check
        if  westCell == jumpOver:
            emptyCell, emptyPosition = self.getWest(gameBoard, westPosition)
            if  emptyCell == EMPTY:
                result.append(emptyPosition)
                game.updateBoard(westPosition, emptyPosition, identity)
                self.jumpToWest(result, game, identity, jumpOver, emptyPosition)
        return result

    def jumpToNorth(self, result, gameBoard, identity, jumpOver, moveable):
        game = copy.deepcopy(gameBoard)
        northCell, northPosition = self.getNorth(gameBoard, moveable)
        #if the cell in the east is opponent's check
        if  northCell == jumpOver:
            emptyCell, emptyPosition = self.getNorth(gameBoard, northPosition)
            if  emptyCell == EMPTY:
                result.append(emptyPosition)
                game.updateBoard(northPosition, emptyPosition, identity)
                self.jumpToNorth(result, game, identity, jumpOver, emptyPosition)
        return result

    def jumpToSouth(self, result, gameBoard, identity, jumpOver, moveable):
        game = copy.deepcopy(gameBoard)
        southCell, southPosition = self.getSouth(gameBoard, moveable)
        #if the cell in the east is opponent's check
        if  southCell == jumpOver:
            emptyCell, emptyPosition = self.getSouth(gameBoard, southPosition)
            if  emptyCell == EMPTY:
                result.append(emptyPosition)
                game.updateBoard(southPosition, emptyPosition, identity)
                self.jumpToSouth(result, game, identity, jumpOver, emptyPosition)
        return result

        def testLegalMove(self, gameBoard, identity, start, end):
        '''
        Returns whether a given move is legal or not.
        '''
        availableMoves = self.availableMoves(gameBoard, identity)
        if start in availableMoves.keys():
            if end in availableMoves[start]:
                return True
        return False

    def roundIncrement(self):
        self.round += 1

    def getRound(self):
        return self.round
