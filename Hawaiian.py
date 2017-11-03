from gameBoard import *
from darkPlayer import *
import random

def getIdentity():
    '''
    Get agent's identity based on user input
    '''
    opponent_piece = raw_input("Choose your color, light or dark? ")
    if opponent_piece.upper() == "DARK":
        opponent = DARKPLAYER
        identity = LIGHTPLAYER
        return identity
    elif opponent_piece.upper() == "LIGHT":
        opponent = LIGHTPLAYER
        identity = DARKPLAYER
        return identity
    else:
        print "Invalid input. Please enter again: "
        return getIdentity()

def firstRound(agent, opponent, gameboard):
    # if computer agent is LIGHTPLAYER, ask for the move from the LIGHTPLAYER before the first move of agent
    if not agent.identity :
        # ask for DARKPLAYER's move
        s = raw_input("Which piece do you want to remove? (Format: row, col)")
        pieces = s.split(",")
        darkmove = (int (pieces[0]), int (pieces[1]))
        print "You want to remove: "+ str(darkmove)
        gameboard.updateBoard(darkmove, None, opponent.identity)
        gameboard.drawBoard()
        firstmove = agent.generateFirstMove_Light(darkmove, gameboard)
        print "I want to remove: " + str(firstmove)
        gameboard.updateBoard(firstmove,None, agent.identity)
        gameboard.drawBoard()
    # if computer agent is DARKPLAYER, ask for the move from the LIGHTPLAYER after the first move of agent
    else:
        firstmove = agent.generateFirstMove_Dark()
        print "I want to remove: " + str(firstmove)
        gameboard.updateBoard(firstmove, None, agent.identity)
        gameboard.drawBoard()
        #ask for LIGHTPLAYER's move
        s = raw_input("Which piece do you want to remove? (Format: row, col)")
        pieces = s.split(",")
        darkmove = (int (pieces[0]), int (pieces[1]))
        print "You want to remove: "+ str(darkmove)
        gameboard.updateBoard(darkmove, None, opponent.identity)
        gameboard.drawBoard()

def askForMove(opponent, gameboard):
    s = raw_input("Which piece do you want to move? (Format: row, col)")
    pieces = s.split(",")
    start = (int (pieces[0]), int (pieces[1]))
    s = raw_input("which position do you want to jump to: ")
    pieces = s.split(",")
    end = (int (pieces[0]), int (pieces[1]))
    legal = opponent.testLegalMove(gameboard,opponent.identity,start, end)
    if legal:
        return (start, end)
    else:
        print "Invalid move. Try again."
        return askForMove(opponent, gameboard)

def main():
    identity = getIdentity()
    agent = Player(identity, 1)
    opponent = Player(not identity, 1)
    gameboard = gameBoard.gameBoard(8)
    gameboard.startState()
    firstRound(agent, opponent, gameboard)
    while not agent.win(gameboard) and not opponent.win(gameboard):
        agent.roundIncrement()
        opponent.roundIncrement()
        if agent.identity:
            move = agent.minimax(agent.identity, gameboard,4)[1]
            print "This is my move: "+ str(move)
            gameboard.updateBoard(move[0], move[1], DARK)
            gameboard.drawBoard()
            if check_Win(agent, opponent,gameboard):
                break
            move = askForMove(opponent, gameboard)
            print "This is your move: " + str(move)
            gameboard.updateBoard(move[0], move[1], LIGHT)
            gameboard.drawBoard()
            if check_Win(agent, opponent,gameboard):
                break
        else:
            move = askForMove(opponent, gameboard)
            print "This is your move: " + str(move)
            gameboard.updateBoard(move[0], move[1] , DARK)
            gameboard.drawBoard()
            if check_Win(agent, opponent,gameboard):
                break
            move = agent.minimax(agent.identity, gameboard, 4)[1]
            print "This is my move: "+ str(move)
            gameboard.updateBoard(move[0], move[1], LIGHT)
            gameboard.drawBoard()
            if check_Win(agent, opponent, gameboard):
                break

def check_Win(agent, opponent,gameboard):
    if agent.win(gameboard):
        print "I Win! \n"
        return True
    if opponent.win(gameboard):
        print "You win! \n"
        return True
    return False

main()
