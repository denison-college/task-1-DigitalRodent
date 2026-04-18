# IMPORTANT MESSAGE
"""I followed an online tutorial to complete this part of my assessment task"""
"""URL found below"""
"""https://www.youtube.com/watch?v=st4bnpt6j1U"""

# Import Modules
import random
import time
import sys
import os

# Functions
def chooseDifficulty():
    """Select the Minesweeper difficulty"""
    validChoise = False
    while not validChoise:
        print('Difficulty')
        print("1. I'm Too Young to Die")
        print("2. Hurt Me Plenty")
        print("3. Ultra-Violence")
        print("4. Nightmare")
        print('\n')

        answer = input('Please enter your difficulty level: ')

        if answer == '1':
            return "I'm Too Young to Die"
        elif answer == '2':
            return "Hurt Me Plenty"
        elif answer == '3':
            return "Ultra-Violence"
        else:
            return "Nightmare"


def createGameLogic(chosenDif, difficulty):
    logicList = []
    for row in range(difficulty[chosenDif]['Rows']):
        rowList = []
        for col in range(difficulty[chosenDif]['Cols']):
            rowList.append(' ')
        logicList.append(rowList)

    insertMines(chosenDif, difficulty, logicList)
    adjacentCells(logicList)

    return logicList


def insertMines(chosenDif, difficulty, gameLogic):
    """Randomly selects and postions the mines onto the game grid"""
    for mine in range (difficulty[chosenDif]['Mines']):
        validChoice = False
        while not validChoice:
            x = random.randint(0, difficulty[chosenDif]['Rows']-1)
            y = random.randint(0, difficulty[chosenDif]['Cols']-1)

            if gameLogic[x][y] == ' ':
                validChoice = True

        gameLogic[x][y] = 'X'


def adjacentCells(gameLogic):
    for x, row in enumerate(gameLogic):
        for y, cell in enumerate(row):
            if cell == ' ':
                cellCount = 0

                if x != 0:
                    if gameLogic[x - 1][y] == 'X':
                        cellCount += 1
                    if y != 0:
                        if gameLogic[x-1][y-1] == 'X':
                            cellCount += 1
                        if y != len(gameLogic[0])-1:
                            if gameLogic[x-1][y+1] == 'X':
                                cellCount += 1

                if y != 0:
                    if gameLogic[x][y-1] == 'X':
                        cellCount += 1
                    if y != len(gameLogic[0])-1:
                        if gameLogic[x][y+1] == 'X':
                            cellCount += 1

                if x != len(gameLogic) - 1:
                    if gameLogic[x + 1][y] == 'X':
                        cellCount += 1
                    if y != 0:
                        if gameLogic[x + 1][y - 1] == 'X':
                            cellCount += 1
                        if y != len(gameLogic[0]) - 1:
                            if gameLogic[x + 1][y + 1] == 'X':
                                cellCount += 1
                if cellCount > 0:
                    gameLogic[x][y] = str(cellCount)


def createGameDict(gameLogic):
    ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    cellDict = {}
    for x, row in enumerate(gameLogic):
        for y, cell in enumerate(row):
            cellDict[(x, y)] = {'cell Ref': ALPHABET[y] + str(x+1), 'cell Value': gameLogic[x][y], 'Cell Vis': 'Hidden'}
    return cellDict


def makeSelecion(gamedictionary):
    validChoice = False
    while not validChoice:
        answer = input('Please Select a Cell to uncover (A1, B2, C3, etc.): ')
        for keys, values in gamedictionary.items():
            if answer in values['cell Ref'] and values['Cell Vis'] == 'Hidden':
                validChoice = True
                answerGrid = keys
                print(answerGrid)
                break

    return answerGrid


def inputSelectionOntoGameLogic(selection, gameLogic, gameDict):
    x, y = selection
    if gameLogic[x][y] == ' ':
        gameLogic[x][y] = '_'
        gameDict[(x, y)]['Cell Vis'] = 'Uncovered'
    elif gameLogic[x][y].isdigit():
        gameDict[(x, y)]['Cell Vis'] = 'Uncovered'
    elif gameLogic[x, y] == 'X':
        gameDict[(x, y)]['Cell Vis'] = 'Uncovered'


def printGameScreen(gameLogic, gameDict):
    ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    print (' Minesweeper '.center(100, '_'))
    print ('Cells Remaining: ')
    topLine = '   |'
    for i in range(len(gameLogic[0])):
        topLine += f' {ALPHABET[i]} |'
    print(topLine)
    rowLine = ''
    for i, row in enumerate(gameLogic):
        rowLine = f'{i+1}'.ljust(3, ' ') + '|'
        for j, cell in enumerate(row):
            if gameDict[(i, j)]['Cell Vis'] != 'Hidden':
                rowLine += f'{gameLogic[i][j]}'.center(3, ' ')+ '|'
            else:
                rowLine += f' # |'
        print(rowLine)


def checkAllAdjacentCells(cellCoord, gameLogic, GameDict):
    x, y = cellCoord
    nx, ny = x, y


    if nx != 0:
        if gameLogic[nx-1][ny] == ' ' or gameLogic[nx-1][ny].isdigit()\
                and gameDict[(nx-1, ny)]['Cell Vis'] == 'Hidden':
            gameDict[(nx-1, ny)]['Cell Vis'] = 'Uncovered'
            if gameLogic[nx-1][ny] == ' ':
                gameLogic[nx-1][ny] = '_'
                checkAllAdjacentCells((nx-1, ny), gameLogic, GameDict)
        if ny != 0:
            if gameLogic[nx - 1][ny - 1] == ' ' or gameLogic[nx - 1][ny - 1].isdigit()\
                    and gameDict[(nx - 1, ny - 1)]['Cell Vis'] == 'Hidden':
                gameDict[(nx - 1, ny - 1)]['Cell Vis'] = 'Uncovered'
                if gameLogic[nx - 1][ny - 1] == ' ':
                    gameLogic[nx - 1][ny - 1] = '_'
                    checkAllAdjacentCells((nx - 1, ny - 1), gameLogic, GameDict)
        if ny != len(gameLogic[0])-1:
            if gameLogic[nx - 1][ny + 1] == ' ' or gameLogic[nx - 1][ny + 1].isdigit()\
                    and gameDict[(nx - 1, ny + 1)][
                'Cell Vis'] == 'Hidden':
                gameDict[(nx - 1, ny + 1)]['Cell Vis'] = 'Uncovered'
                if gameLogic[nx - 1][ny + 1] == ' ':
                    gameLogic[nx - 1][ny + 1] = '_'
                    checkAllAdjacentCells((nx - 1, ny + 1), gameLogic, GameDict)

    if nx != len(gameLogic) - 1:
        if gameLogic[nx+1][ny] == ' ' or gameLogic[nx+1][ny].isdigit()\
                and gameDict[(nx+1, ny)]['Cell Vis'] == 'Hidden':
            gameDict[(nx+1, ny)]['Cell Vis'] = 'Uncovered'
            if gameLogic[nx+1][ny] == ' ':
                gameLogic[nx+1][ny] = '_'
                checkAllAdjacentCells((nx+1, ny), gameLogic, GameDict)
        if ny != 0:
            if gameLogic[nx + 1][ny - 1] == ' ' or gameLogic[nx + 1][ny - 1].isdigit()\
                    and gameDict[(nx + 1, ny - 1)]['Cell Vis'] == 'Hidden':
                gameDict[(nx + 1, ny - 1)]['Cell Vis'] = 'Uncovered'
                if gameLogic[nx + 1][ny - 1] == ' ':
                    gameLogic[nx + 1][ny - 1] = '_'
                    checkAllAdjacentCells((nx + 1, ny - 1), gameLogic, GameDict)
        if ny != len(gameLogic[0])-1:
            if gameLogic[nx + 1][ny + 1] == ' ' or gameLogic[nx + 1][ny + 1].isdigit()\
                    and gameDict[(nx + 1, ny + 1)][
                'Cell Vis'] == 'Hidden':
                gameDict[(nx + 1, ny + 1)]['Cell Vis'] = 'Uncovered'
                if gameLogic[nx + 1][ny + 1] == ' ':
                    gameLogic[nx + 1][ny + 1] = '_'
                    checkAllAdjacentCells((nx + 1, ny + 1), gameLogic, GameDict)

        if ny != 0:
            if gameLogic[nx][ny - 1] == ' ' or gameLogic[nx][ny - 1].isdigit()\
                    and gameDict[(nx, ny - 1)]['Cell Vis'] == 'Hidden':
                gameDict[(nx, ny - 1)]['Cell Vis'] = 'Uncovered'
                if gameLogic[nx][ny - 1] == ' ':
                    gameLogic[nx][ny - 1] = '_'
                    checkAllAdjacentCells((nx, ny - 1), gameLogic, GameDict)
        if ny != len(gameLogic[0])-1:
            if gameLogic[nx][ny + 1] == ' ' or gameLogic[nx][ny + 1].isdigit()\
                    and gameDict[(nx, ny + 1)]['Cell Vis'] == 'Hidden':
                gameDict[(nx, ny + 1)]['Cell Vis'] = 'Uncovered'
                if gameLogic[nx][ny + 1] == ' ':
                    gameLogic[nx][ny + 1] = '_'
                    checkAllAdjacentCells((nx, ny + 1), gameLogic, GameDict)



# Dictionaries and Lists
difficulty = {
    "I'm Too Young to Die": {'Rows': 10, 'Cols': 10, 'Mines': 10},
    "Hurt Me Plenty": {'Rows': 15, 'Cols': 15, 'Mines': 20},
    "Ultra-Violence": {'Rows': 20, 'Cols': 20, 'Mines': 40},
    "Nightmare": {'Rows': 30, 'Cols': 26, 'Mines': 200},
}

# Variables
chooseDif = chooseDifficulty()
gameLogic = createGameLogic(chooseDif, difficulty)
gameDict = createGameDict(gameLogic)
for key, value in gameDict.items():
    print(key, value)

# Call Functions

# rungame

for _ in gameLogic:
    print(_)

printGameScreen(gameLogic, gameDict)
selection = makeSelecion(gameDict)
inputSelectionOntoGameLogic(selection, gameLogic, gameDict)
printGameScreen(gameLogic, gameDict)