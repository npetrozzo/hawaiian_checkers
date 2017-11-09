from gameBoard import *
from darkPlayer import *
import random


def main():
    limit = int(raw_input("Enter depth limit: "))
    gameboard = gameBoard.gameBoard(8)
    gameboard.startState()

    
    lightAgent = Player(LIGHTPLAYER, 1)
    darkAgent = Player(DARKPLAYER, 1)

    # first round
    darkMove = darkAgent.generateFirstMove_Dark()
    print "Dark player removes: " + str(darkMove)
    gameboard.updateBoard(darkMove, None, DARK)
    gameboard.drawBoard()
    firstmove = lightAgent.generateFirstMove_Light(darkMove, gameboard)
    print "Light player removes: " + str(firstmove)
    gameboard.updateBoard(firstmove, None, LIGHT)
    gameboard.drawBoard()

    while not lightAgent.win(gameboard) and not darkAgent.win(gameboard):
        lightAgent.roundIncrement()
        darkAgent.roundIncrement()
        darkMove = darkAgent.minimax(DARKPLAYER, gameboard, limit)[1]
        print "This is Dark player's move: "+ str(darkMove)
        gameboard.updateBoard(darkMove[0], darkMove[1], DARK)
        gameboard.drawBoard()
        if check_Win(lightAgent, darkAgent, gameboard):
            break
        lightMove = lightAgent.minimax(LIGHTPLAYER, gameboard, limit)[1]
        print "This is Light player's move: "+ str(lightMove)
        gameboard.updateBoard(lightMove[0], lightMove[1], LIGHT)
        gameboard.drawBoard()
        if check_Win(lightAgent, darkAgent, gameboard):
            break

def check_Win(light, dark, gameboard):
    if light.win(gameboard):
        print "Light wins! \n"
        print "Light # static evals: " + str(light.total_eval)
        print "Light # cutoffs: " + str(light.cutoffs)
        if light.branch_factor:
             print "Light average branching factor: " + str(sum(light.branch_factor) / float(len(light.branch_factor)))
        print "Dark # static evals: " + str(dark.total_eval)
        print "Dark # cutoffs: " + str(dark.cutoffs)
        if dark.branch_factor:
            print "Dark average branching factor: " + str(sum(dark.branch_factor) / float(len(dark.branch_factor)))
        return True
    if dark.win(gameboard):
        print "Dark wins! \n"
        print "Light # static evals: " + str(light.total_eval)
        print "Light # cutoffs: " + str(light.cutoffs)
        if light.branch_factor:
            print "Light average branching factor: " + str(sum(light.branch_factor) / float(len(light.branch_factor)))
        print "Dark # static evals: " + str(dark.total_eval)
        print "Dark # cutoffs: " + str(dark.cutoffs)
        if dark.branch_factor:
             print "Dark average branching factor: " + str(sum(dark.branch_factor) / float(len(dark.branch_factor)))
        return True
    return False

main()
