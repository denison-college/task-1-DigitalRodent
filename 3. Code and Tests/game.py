# IMPORTANT MESSAGE
"""I followed an online tutorial to complete this part of my assessment task"""
"""URL found below"""
"""https://www.youtube.com/watch?v=st4bnpt6j1U"""

# Import modules used for randomness, timing, and saving scores.
# Import modules used for randomness, timing, screen clearing, and saving scores.
import random
import time
import os
import score

# Global state used throughout the game.
difficulty = None
gameLogic = None
gameDict = None
chooseDif = None
startTime = None
playerName = None


def clear_screen():
    # Clear the terminal screen on Windows or Unix-like systems.
    os.system("cls" if os.name == "nt" else "clear")


def runGame(Name):
    global chooseDif, gameLogic, gameDict, startTime, difficulty, playerName
    """Run the game"""
    # Store the player's name and define the available difficulty presets.
    playerName = Name

    difficulty = {
        "I'm Too Young to Die": {"Rows": 10, "Cols": 10, "Mines": 10},
        "Hurt Me Plenty": {"Rows": 15, "Cols": 15, "Mines": 20},
        "Ultra-Violence": {"Rows": 20, "Cols": 20, "Mines": 40},
        "Nightmare": {"Rows": 30, "Cols": 26, "Mines": 200},
    }

    # Ask for difficulty, create the board, and begin the timer.
    chooseDif = chooseDifficulty()
    gameLogic = createGameLogic(chooseDif, difficulty)
    gameDict = createGameDict(gameLogic)
    startTime = time.perf_counter()

    # Main gameplay loop.
    running = True
    while running:
        clear_screen()
        printGameScreen(gameLogic, gameDict, startTime)
        selection, action = makeSelection(gameDict)
        processSelection(selection, action, gameLogic, gameDict)
        running = checkForWinLose(gameLogic, gameDict, startTime)


def chooseDifficulty():
    """Select the Minesweeper difficulty"""
    # Keep asking until the player enters a valid choice.
    while True:
        print("Difficulty")
        print("1. I'm Too Young to Die")
        print("2. Hurt Me Plenty")
        print("3. Ultra-Violence")
        print("4. Nightmare")
        print()

        answer = input("Please enter your difficulty level: ").strip()

        if answer == "1":
            return "I'm Too Young to Die"
        if answer == "2":
            return "Hurt Me Plenty"
        if answer == "3":
            return "Ultra-Violence"
        if answer == "4":
            return "Nightmare"

        clear_screen()
        time.sleep(1)
        clear_screen()


def createGameLogic(chosenDif, difficulty):
    logicList = []
    for _ in range(difficulty[chosenDif]["Rows"]):
        logicList.append([" "] * difficulty[chosenDif]["Cols"])

    insertMines(chosenDif, difficulty, logicList)
    adjacentCells(logicList)
    return logicList


def insertMines(chosenDif, difficulty, gameLogic):
    """Randomly select and position mines onto the game grid"""
    mines_to_place = difficulty[chosenDif]["Mines"]

    placed = 0
    while placed < mines_to_place:
        x = random.randint(0, difficulty[chosenDif]["Rows"] - 1)
        y = random.randint(0, difficulty[chosenDif]["Cols"] - 1)

        if gameLogic[x][y] == " ":
            gameLogic[x][y] = "X"
            placed += 1


def adjacentCells(gameLogic):
    rows = len(gameLogic)
    cols = len(gameLogic[0])

    for x in range(rows):
        for y in range(cols):
            if gameLogic[x][y] != " ":
                continue

            count = 0
            for nx in range(max(0, x - 1), min(rows, x + 2)):
                for ny in range(max(0, y - 1), min(cols, y + 2)):
                    if (nx, ny) != (x, y) and gameLogic[nx][ny] == "X":
                        count += 1

            if count > 0:
                gameLogic[x][y] = str(count)


def createGameDict(gameLogic):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    cellDict = {}

    for x, row in enumerate(gameLogic):
        for y, _ in enumerate(row):
            cellDict[(x, y)] = {
                "cell Ref": alphabet[y] + str(x + 1),
                "Cell Value": gameLogic[x][y],
                "Cell Vis": "Hidden",
            }

    return cellDict


def makeSelection(gamedictionary):
    while True:
        answer = input(
            'Enter a cell to uncover (A1, B2, etc.) or flag with "F A1" / "flag A1": '
        ).strip()

        action = "uncover"
        cell_ref = answer.upper()

        parts = answer.split()
        if len(parts) == 2 and parts[0].lower() in ("f", "flag"):
            action = "flag"
            cell_ref = parts[1].upper()

        for keys, values in gamedictionary.items():
            if cell_ref == values["cell Ref"]:
                return keys, action

        print("Invalid cell reference. Please try again.")


def processSelection(selection, action, gameLogic, gameDict):
    x, y = selection
    cell_info = gameDict[(x, y)]

    if action == "flag":
        # Prevent flagging a cell that has already been uncovered.
        if cell_info["Cell Vis"] == "Uncovered":
            print("You cannot flag an uncovered cell.")
            time.sleep(1)
            clear_screen()
            return

        # Toggle the flag state.
        if cell_info["Cell Vis"] == "Flagged":
            cell_info["Cell Vis"] = "Hidden"
            print(f"{cell_info['cell Ref']} unflagged.")
        else:
            cell_info["Cell Vis"] = "Flagged"
            print(f"{cell_info['cell Ref']} flagged.")

        time.sleep(1)
        clear_screen()
        return

    # Prevent uncovering flagged or already uncovered cells.
    if cell_info["Cell Vis"] == "Flagged":
        print("That cell is flagged. Unflag it before uncovering.")
        time.sleep(1)
        clear_screen()
        return

    if cell_info["Cell Vis"] == "Uncovered":
        print("That cell is already uncovered.")
        time.sleep(1)
        clear_screen()
        return

    # Mark the selected cell as uncovered.
    cell_info["Cell Vis"] = "Uncovered"

    # If the cell is empty, reveal neighboring cells recursively.
    if gameLogic[x][y] == " ":
        gameLogic[x][y] = "_"
        checkAllAdjacentCells((x, y), gameLogic, gameDict)

    clear_screen()


def printGameScreen(gameLogic, gameDict, startTime):
    # Show the current board and game statistics.
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    remainingCells = countRemainingCells(gameDict)
    flagCount = countFlags(gameDict)
    totalFlagsAllowed = difficulty[chooseDif]["Mines"]
    flagsRemaining = totalFlagsAllowed - flagCount
    elapsedTime = time.perf_counter() - startTime

    print(" Minesweeper ".center(100, "_"))
    print(f"Cells Remaining: {remainingCells}")
    print(f"Flags Placed: {flagCount}")
    print(f"Flags Remaining: {flagsRemaining}")
    print(f"Time Elapsed: {formatElapsedTime(elapsedTime)}")

    topLine = "   |"
    for i in range(len(gameLogic[0])):
        topLine += f" {alphabet[i]} |"
    print(topLine)

    for i, row in enumerate(gameLogic):
        rowLine = f"{i + 1}".ljust(3, " ") + "|"
        for j, _ in enumerate(row):
            vis = gameDict[(i, j)]["Cell Vis"]
            if vis == "Uncovered":
                rowLine += f"{gameLogic[i][j]}".center(3, " ") + "|"
            elif vis == "Flagged":
                rowLine += " F ".center(3, " ") + "|"
            else:
                rowLine += " # |"
        print(rowLine)


def countRemainingCells(gameDict):
    remaining = 0
    for cell in gameDict.values():
        if cell["Cell Value"] != "X" and cell["Cell Vis"] == "Hidden":
            remaining += 1
    return remaining


def countFlags(gameDict):
    flags = 0
    for cell in gameDict.values():
        if cell["Cell Vis"] == "Flagged":
            flags += 1
    return flags


def formatElapsedTime(seconds):
    minutes = int(seconds // 60)
    remainingSeconds = seconds % 60
    return f"{minutes:02d}:{remainingSeconds:05.2f}"


def checkAllAdjacentCells(cellCoord, gameLogic, gameDict):
    rows = len(gameLogic)
    cols = len(gameLogic[0])
    x, y = cellCoord

    for nx in range(max(0, x - 1), min(rows, x + 2)):
        for ny in range(max(0, y - 1), min(cols, y + 2)):
            if (nx, ny) == (x, y):
                continue

            if gameDict[(nx, ny)]["Cell Vis"] != "Hidden":
                continue

            if gameLogic[nx][ny] == "X":
                continue

            gameDict[(nx, ny)]["Cell Vis"] = "Uncovered"

            if gameLogic[nx][ny] == " ":
                gameLogic[nx][ny] = "_"
                checkAllAdjacentCells((nx, ny), gameLogic, gameDict)


def revealAllMines(gameDict):
    for values in gameDict.values():
        if values["Cell Value"] == "X":
            values["Cell Vis"] = "Uncovered"


def saveResult(result, startTime):
    elapsed_time = time.perf_counter() - startTime
    score.add_score(playerName, result, elapsed_time, chooseDif)


def checkForWinLose(gameLogic, gameDict, startTime):
    totalMines = difficulty[chooseDif]["Mines"]
    totalCells = difficulty[chooseDif]["Rows"] * difficulty[chooseDif]["Cols"]
    safeCells = totalCells - totalMines

    uncoveredSafeCells = 0

    for values in gameDict.values():
        if values["Cell Vis"] == "Uncovered" and values["Cell Value"] != "X":
            uncoveredSafeCells += 1

        if values["Cell Value"] == "X" and values["Cell Vis"] == "Uncovered":
            revealAllMines(gameDict)
            printGameScreen(gameLogic, gameDict, startTime)
            saveResult("Lost", startTime)
            print('''
             .d8888b.         d8888 888b     d888 8888888888       .d88888b.  888     888 8888888888 8888888b.  888 
            d88P  Y88b       d88888 8888b   d8888 888             d88P" "Y88b 888     888 888        888   Y88b 888 
            888    888      d88P888 88888b.d88888 888             888     888 888     888 888        888    888 888 
            888            d88P 888 888Y88888P888 8888888         888     888 Y88b   d88P 8888888    888   d88P 888 
            888  88888    d88P  888 888 Y888P 888 888             888     888  Y88b d88P  888        8888888P"  888 
            888    888   d88P   888 888  Y8P  888 888             888     888   Y88o88P   888        888 T88b   Y8P 
            Y88b  d88P  d8888888888 888   "   888 888             Y88b. .d88P    Y888P    888        888  T88b   "  
             "Y8888P88 d88P     888 888       888 8888888888       "Y88888P"      Y8P     8888888888 888   T88b 888 ''')
            time.sleep(1)
            print("YOU FAILED")
            time.sleep(2)
            return False

    if uncoveredSafeCells == safeCells:
        printGameScreen(gameLogic, gameDict, startTime)
        saveResult("Won", startTime)
        print('''
         .d8888b.   .d88888b.  888b    888  .d8888b.  8888888b.         d8888 88888888888 888     888 888             d8888 88888888888 8888888 .d88888b.  888b    888  .d8888b.  888 
        d88P  Y88b d88P" "Y88b 8888b   888 d88P  Y88b 888   Y88b       d88888     888     888     888 888            d88888     888       888  d88P" "Y88b 8888b   888 d88P  Y88b 888 
        888    888 888     888 88888b  888 888    888 888    888      d88P888     888     888     888 888           d88P888     888       888  888     888 88888b  888 Y88b.      888 
        888        888     888 888Y88b 888 888        888   d88P     d88P 888     888     888     888 888          d88P 888     888       888  888     888 888Y88b 888  "Y888b.   888 
        888        888     888 888 Y88b888 888  88888 8888888P"     d88P  888     888     888     888 888         d88P  888     888       888  888     888 888 Y88b888     "Y88b. 888 
        888    888 888     888 888  Y88888 888    888 888 T88b     d88P   888     888     888     888 888        d88P   888     888       888  888     888 888  Y88888       "888 Y8P 
        Y88b  d88P Y88b. .d88P 888   Y8888 Y88b  d88P 888  T88b   d8888888888     888     Y88b. .d88P 888       d8888888888     888       888  Y88b. .d88P 888   Y8888 Y88b  d88P  "  
         "Y8888P"   "Y88888P"  888    Y888  "Y8888P88 888   T88b d88P     888     888      "Y88888P"  88888888 d88P     888     888     8888888 "Y88888P"  888    Y888  "Y8888P"  888 ''')
        time.sleep(1)
        print("YOU WON")
        time.sleep(2)
        return False

    return True


