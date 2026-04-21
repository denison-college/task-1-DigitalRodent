# IMPORTANT MESSAGE
"""I followed an online tutorial to complete this part of my assessment task"""
"""URL found below"""
"""https://www.youtube.com/watch?v=st4bnpt6j1U"""

# Import Modules
import random
import time
import sys
import os

difficulty = None
gameLogic = None
gameDict = None
chooseDif = None
startTime = None

# Functions
def runGame(Name):
    global chooseDif, gameLogic, gameDict, startTime, difficulty
    """Run the game"""
    difficulty = {
        "I'm Too Young to Die": {'Rows': 10, 'Cols': 10, 'Mines': 10},
        "Hurt Me Plenty": {'Rows': 15, 'Cols': 15, 'Mines': 20},
        "Ultra-Violence": {'Rows': 20, 'Cols': 20, 'Mines': 40},
        "Nightmare": {'Rows': 30, 'Cols': 26, 'Mines': 200},
    }


    chooseDif = chooseDifficulty()
    gameLogic = createGameLogic(chooseDif, difficulty)
    gameDict = createGameDict(gameLogic)
    startTime = time.perf_counter()

    RUNGAME = True
    while RUNGAME:
        printGameScreen(gameLogic, gameDict, startTime)
        selection, action = makeSelection(gameDict)
        processSelection(selection, action, gameLogic, gameDict)
        RUNGAME = checkForWinLose(gameLogic, gameDict)


def chooseDifficulty():
    """Select the Minesweeper difficulty"""
    while True:
        print('Difficulty')
        print("1. I'm Too Young to Die")
        print("2. Hurt Me Plenty")
        print("3. Ultra-Violence")
        print("4. Nightmare")
        print('\n')

        answer = input('Please enter your difficulty level: ').strip()

        if answer == '1':
            return "I'm Too Young to Die"
        elif answer == '2':
            return "Hurt Me Plenty"
        elif answer == '3':
            return "Ultra-Violence"
        elif answer == '4':
            return "Nightmare"
        else:
            print("Invalid choice. Please choose 1, 2, 3, or 4.")


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
    for mine in range(difficulty[chosenDif]['Mines']):
        validChoice = False
        while not validChoice:
            x = random.randint(0, difficulty[chosenDif]['Rows'] - 1)
            y = random.randint(0, difficulty[chosenDif]['Cols'] - 1)

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
                    if y != 0 and gameLogic[x - 1][y - 1] == 'X':
                        cellCount += 1
                    if y != len(gameLogic[0]) - 1 and gameLogic[x - 1][y + 1] == 'X':
                        cellCount += 1

                if y != 0 and gameLogic[x][y - 1] == 'X':
                    cellCount += 1
                if y != len(gameLogic[0]) - 1 and gameLogic[x][y + 1] == 'X':
                    cellCount += 1

                if x != len(gameLogic) - 1:
                    if gameLogic[x + 1][y] == 'X':
                        cellCount += 1
                    if y != 0 and gameLogic[x + 1][y - 1] == 'X':
                        cellCount += 1
                    if y != len(gameLogic[0]) - 1 and gameLogic[x + 1][y + 1] == 'X':
                        cellCount += 1

                if cellCount > 0:
                    gameLogic[x][y] = str(cellCount)


def createGameDict(gameLogic):
    ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    cellDict = {}
    for x, row in enumerate(gameLogic):
        for y, cell in enumerate(row):
            cellDict[(x, y)] = {
                'cell Ref': ALPHABET[y] + str(x + 1),
                'Cell Value': gameLogic[x][y],
                'Cell Vis': 'Hidden'
            }
    return cellDict


def makeSelection(gamedictionary):
    while True:
        answer = input(
            'Enter a cell to uncover (A1, B2, etc.) or flag with "F A1" / "flag A1": '
        ).strip()

        action = 'uncover'
        cell_ref = answer.upper()

        parts = answer.split()
        if len(parts) == 2 and parts[0].lower() in ('f', 'flag'):
            action = 'flag'
            cell_ref = parts[1].upper()

        for keys, values in gamedictionary.items():
            if cell_ref == values['cell Ref']:
                return keys, action

        print("Invalid cell reference. Please try again.")


def processSelection(selection, action, gameLogic, gameDict):
    x, y = selection
    cell_info = gameDict[(x, y)]

    if action == 'flag':
        if cell_info['Cell Vis'] == 'Uncovered':
            print("You cannot flag an uncovered cell.")
            return

        if cell_info['Cell Vis'] == 'Flagged':
            cell_info['Cell Vis'] = 'Hidden'
            print(f"{cell_info['cell Ref']} unflagged.")
        else:
            cell_info['Cell Vis'] = 'Flagged'
            print(f"{cell_info['cell Ref']} flagged.")
        return

    if cell_info['Cell Vis'] == 'Flagged':
        print("That cell is flagged. Unflag it before uncovering.")
        return

    if cell_info['Cell Vis'] == 'Uncovered':
        print("That cell is already uncovered.")
        return

    cell_info['Cell Vis'] = 'Uncovered'

    if gameLogic[x][y] == ' ':
        gameLogic[x][y] = '_'
        checkAllAdjacentCells((x, y), gameLogic, gameDict)


def printGameScreen(gameLogic, gameDict, startTime):
    ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    remainingCells = countRemainingCells(gameDict)
    elapsedTime = time.perf_counter() - startTime
    flagCount = countFlags(gameDict)
    totalFlagsAllowed = difficulty[chooseDif]['Mines']
    flagsRemaining = totalFlagsAllowed - flagCount

    print(' Minesweeper '.center(100, '_'))
    print(f'Cells Remaining: {remainingCells}')
    print(f'Flags Placed: {flagCount}')
    print(f'Flags Remaining: {flagsRemaining}')
    print(f'Time Elapsed: {formatElapsedTime(elapsedTime)}')
    topLine = '   |'
    for i in range(len(gameLogic[0])):
        topLine += f' {ALPHABET[i]} |'
    print(topLine)

    for i, row in enumerate(gameLogic):
        rowLine = f'{i + 1}'.ljust(3, ' ') + '|'
        for j, cell in enumerate(row):
            vis = gameDict[(i, j)]['Cell Vis']
            if vis == 'Uncovered':
                rowLine += f'{gameLogic[i][j]}'.center(3, ' ') + '|'
            elif vis == 'Flagged':
                rowLine += ' F '.center(3, ' ') + '|'
            else:
                rowLine += ' # |'
        print(rowLine)


def countRemainingCells(gameDict):
    remaining = 0
    for cell in gameDict.values():
        if cell['Cell Value'] != 'X' and cell['Cell Vis'] == 'Hidden':
            remaining += 1
    return remaining


def countFlags(gameDict):
    flags = 0
    for cell in gameDict.values():
        if cell['Cell Vis'] == 'Flagged':
            flags += 1
    return flags


def formatElapsedTime(seconds):
    minutes = int(seconds // 60)
    remainingSeconds = seconds % 60
    return f"{minutes:02d}:{remainingSeconds:05.2f}"


def checkAllAdjacentCells(cellCoord, gameLogic, gameDict):
    x, y = cellCoord
    nx, ny = x, y

    if nx != 0:
        if (gameLogic[nx - 1][ny] == ' ' or gameLogic[nx - 1][ny].isdigit()) and gameDict[(nx - 1, ny)]['Cell Vis'] == 'Hidden':
            gameDict[(nx - 1, ny)]['Cell Vis'] = 'Uncovered'
            if gameLogic[nx - 1][ny] == ' ':
                gameLogic[nx - 1][ny] = '_'
                checkAllAdjacentCells((nx - 1, ny), gameLogic, gameDict)
        if ny != 0:
            if (gameLogic[nx - 1][ny - 1] == ' ' or gameLogic[nx - 1][ny - 1].isdigit()) and gameDict[(nx - 1, ny - 1)]['Cell Vis'] == 'Hidden':
                gameDict[(nx - 1, ny - 1)]['Cell Vis'] = 'Uncovered'
                if gameLogic[nx - 1][ny - 1] == ' ':
                    gameLogic[nx - 1][ny - 1] = '_'
                    checkAllAdjacentCells((nx - 1, ny - 1), gameLogic, gameDict)
        if ny != len(gameLogic[0]) - 1:
            if (gameLogic[nx - 1][ny + 1] == ' ' or gameLogic[nx - 1][ny + 1].isdigit()) and gameDict[(nx - 1, ny + 1)]['Cell Vis'] == 'Hidden':
                gameDict[(nx - 1, ny + 1)]['Cell Vis'] = 'Uncovered'
                if gameLogic[nx - 1][ny + 1] == ' ':
                    gameLogic[nx - 1][ny + 1] = '_'
                    checkAllAdjacentCells((nx - 1, ny + 1), gameLogic, gameDict)

    if nx != len(gameLogic) - 1:
        if (gameLogic[nx + 1][ny] == ' ' or gameLogic[nx + 1][ny].isdigit()) and gameDict[(nx + 1, ny)]['Cell Vis'] == 'Hidden':
            gameDict[(nx + 1, ny)]['Cell Vis'] = 'Uncovered'
            if gameLogic[nx + 1][ny] == ' ':
                gameLogic[nx + 1][ny] = '_'
                checkAllAdjacentCells((nx + 1, ny), gameLogic, gameDict)
        if ny != 0:
            if (gameLogic[nx + 1][ny - 1] == ' ' or gameLogic[nx + 1][ny - 1].isdigit()) and gameDict[(nx + 1, ny - 1)]['Cell Vis'] == 'Hidden':
                gameDict[(nx + 1, ny - 1)]['Cell Vis'] = 'Uncovered'
                if gameLogic[nx + 1][ny - 1] == ' ':
                    gameLogic[nx + 1][ny - 1] = '_'
                    checkAllAdjacentCells((nx + 1, ny - 1), gameLogic, gameDict)
        if ny != len(gameLogic[0]) - 1:
            if (gameLogic[nx + 1][ny + 1] == ' ' or gameLogic[nx + 1][ny + 1].isdigit()) and gameDict[(nx + 1, ny + 1)]['Cell Vis'] == 'Hidden':
                gameDict[(nx + 1, ny + 1)]['Cell Vis'] = 'Uncovered'
                if gameLogic[nx + 1][ny + 1] == ' ':
                    gameLogic[nx + 1][ny + 1] = '_'
                    checkAllAdjacentCells((nx + 1, ny + 1), gameLogic, gameDict)

    if ny != 0:
        if (gameLogic[nx][ny - 1] == ' ' or gameLogic[nx][ny - 1].isdigit()) and gameDict[(nx, ny - 1)]['Cell Vis'] == 'Hidden':
            gameDict[(nx, ny - 1)]['Cell Vis'] = 'Uncovered'
            if gameLogic[nx][ny - 1] == ' ':
                gameLogic[nx][ny - 1] = '_'
                checkAllAdjacentCells((nx, ny - 1), gameLogic, gameDict)

    if ny != len(gameLogic[0]) - 1:
        if (gameLogic[nx][ny + 1] == ' ' or gameLogic[nx][ny + 1].isdigit()) and gameDict[(nx, ny + 1)]['Cell Vis'] == 'Hidden':
            gameDict[(nx, ny + 1)]['Cell Vis'] = 'Uncovered'
            if gameLogic[nx][ny + 1] == ' ':
                gameLogic[nx][ny + 1] = '_'
                checkAllAdjacentCells((nx, ny + 1), gameLogic, gameDict)


def checkForWinLose(gameLogic, gameDict):
    TOTALMINES = difficulty[chooseDif]['Mines']
    TOTALCELLS = difficulty[chooseDif]['Rows'] * difficulty[chooseDif]['Cols']
    AVCELLS = TOTALCELLS - TOTALMINES
    visibleCells = 0

    for values in gameDict.values():
        if values['Cell Vis'] == 'Uncovered':
            visibleCells += 1
        if values['Cell Value'] == 'X' and values['Cell Vis'] == 'Uncovered':
            print("Game Over, You Lost!")
            time.sleep(2)
            return False

    if visibleCells == AVCELLS:
        print("Congratulations, You Won!")
        time.sleep(2)
        return False
    else:
        return True


