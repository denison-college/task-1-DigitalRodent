# Import Modules


# Functions
def createGameLogic(rows, colums):
    logicList = []
    for row in range(rows):
        rowList = []
        for col in range(colums):
            rowList.append(' ')
        logicList.append(rowList)
    return logicList

# Variables
gameLogic = createGameLogic

# Dictionaries and Lists
difficulty = {
    "I'm Too Young to Die": {'Rows': 10, 'Cols': 10, 'Mines': 10},
    "Hurt Me Plenty": {'Rows': 15, 'Cols': 15, 'Mines': 20},
    "Ultra-Violence": {'Rows': 20, 'Cols': 20, 'Mines': 40},
    "Nightmare": {'Rows': 30, 'Cols': 24, 'Mines': 200},
}


# Call Functions