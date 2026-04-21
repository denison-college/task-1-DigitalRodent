# Import Modules
import time
import sys
import os
import game
import score


def text_print(text, delay):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)


def title():
    text_print("Welcome to", 0.1)
    time.sleep(1)
    print("\n")
    text_print(
        r'''
        888b     d888 d8b                                                                                      
        8888b   d8888 Y8P                                                                                      
        88888b.d88888                                                                                          
        888Y88888P888 888 88888b.   .d88b.  .d8888b  888  888  888  .d88b.   .d88b.  88888b.   .d88b.  888d888 
        888 Y888P 888 888 888 "88b d8P  Y8b 88K      888  888  888 d8P  Y8b d8P  Y8b 888 "88b d8P  Y8b 888P"   
        888  Y8P  888 888 888  888 88888888 "Y8888b. 888  888  888 88888888 88888888 888  888 88888888 888     
        888   "   888 888 888  888 Y8b.          X88 Y88b 888 d88P Y8b.     Y8b.     888 d88P Y8b.     888     
        888       888 888 888  888  "Y8888   88888P'  "Y8888888P"   "Y8888   "Y8888  88888P"   "Y8b.     888     
                                                                                     888                       
                                                                                     888                       
                                                                                     888                       '''
        .center(100, " "),
        0.001,
    )
    print("\n")


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def mainmenu():
    while True:

        print("Options")
        print("1. Play Game")
        print("2. Access Scoreboard")
        print("3. Exit")
        print()

        option = input("Please choose an option: ").strip()

        if option == "1":
            clear_screen()
            name = input("Please enter your name: ").strip()
            if not name:
                name = "Unknown"
            clear_screen()
            game.runGame(name)
            input("\nPress Enter to return to the main menu...")

        elif option == "2":
            clear_screen()
            score.show_scoreboard()
            input("\nPress Enter to return to the main menu...")

        elif option == "3":
            text_print("Now Exiting the program...", 0.1)
            time.sleep(0.5)
            break

        else:
            print("Invalid Option")
            time.sleep(2)


title()
mainmenu()
