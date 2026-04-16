# Import area
# import rich
import time
import sys 
import os

def text_print(text, delay):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)

def play():
    os.system('clear')
    text_print("We are so glad you're here...", 0.1)
    time.sleep(1)
    print('\n')
    text_print("Please fill out the form below to continue", 0.1)
    time.sleep(1)

    print('\n')
    print('''
    ______________________________________________________________________________________________
                                   Legally Binding Consent form                                   
    ==============================================================================================''')

    FN = input('First Name: ')
    SN = input('Surname Name: ')
    print('\n')
    DOB = input('Date of Birth: ')
    print('\n')
    COO = input('Country of Origin: ')
    PC = input('Postal Code: ')
    print('\n')
    print('\n')

#Minesweeper
#welcome and options page 1
time.sleep(2)
def startup2():
    print('Welcome to')
    print(r''' 
    
    888b     d888 d8b                                                                                      
    8888b   d8888 Y8P                                                                                      
    88888b.d88888                                                                                          
    888Y88888P888 888 88888b.   .d88b.  .d8888b  888  888  888  .d88b.   .d88b.  88888b.   .d88b.  888d888 
    888 Y888P 888 888 888 "88b d8P  Y8b 88K      888  888  888 d8P  Y8b d8P  Y8b 888 "88b d8P  Y8b 888P"   
    888  Y8P  888 888 888  888 88888888 "Y8888b. 888  888  888 88888888 88888888 888  888 88888888 888     
    888   "   888 888 888  888 Y8b.          X88 Y88b 888 d88P Y8b.     Y8b.     888 d88P Y8b.     888     
    888       888 888 888  888  "Y8888   88888P'  "Y8888888P"   "Y8888   "Y8888  88888P"   "Y8888  888     
                                                                                 888                       
                                                                                 888                       
                                                                                 888                       ''')
    print('Thank you for willingly participating')
    print('\n')
def startup():
    text_print("Welcome to", 0.2)
    time.sleep(1)

    print('\n')
    text_print(r'''
    888b     d888 d8b                                                                                      
    8888b   d8888 Y8P                                                                                      
    88888b.d88888                                                                                          
    888Y88888P888 888 88888b.   .d88b.  .d8888b  888  888  888  .d88b.   .d88b.  88888b.   .d88b.  888d888 
    888 Y888P 888 888 888 "88b d8P  Y8b 88K      888  888  888 d8P  Y8b d8P  Y8b 888 "88b d8P  Y8b 888P"   
    888  Y8P  888 888 888  888 88888888 "Y8888b. 888  888  888 88888888 88888888 888  888 88888888 888     
    888   "   888 888 888  888 Y8b.          X88 Y88b 888 d88P Y8b.     Y8b.     888 d88P Y8b.     888     
    888       888 888 888  888  "Y8888   88888P'  "Y8888888P"   "Y8888   "Y8888  88888P"   "Y8888  888     
                                                                                 888                       
                                                                                 888                       
                                                                                 888                       ''', 0.001)

    print('\n')
    time.sleep(2)
    text_print('Thank you for willingly participating', 0.1)
    print('\n')
    time.sleep(0.5)
def mainmenu():
    print('Options')
    print('1. Play Game')
    print('2. Access Scoreboard')
    print('3. Exit')
    print('\n')

#Options
    Option = input('Please choose an option:')
    if Option == '1':
        play()
    elif Option == '2':
        quit()
#Quitting system
# Y options
    elif Option == '3':
        text_print('Really? ', 0.1)
        Option2 = input ( 'Y/N ')
        if Option2 == 'Y':
            text_print('Are you sure? ' , 0.1)
        elif Option2 == 'y':
            text_print('Are you sure? ' , 0.1)
def Quit_Option():
    Option3 = input ( 'Y/N ')
        if Option3 == 'Y':
            print('Fine')
            time.sleep(0.5)
            text_print("Now Exiting the program...", 0.2)
            time.sleep(2)
        elif Option3 == 'y':
            print('Fine')
            time.sleep(0.5)
            text_print("Now Exiting the program...", 0.2)
            time.sleep(2)
            quit()
#N options
        elif Option3 == 'N':
            print('Marvelous!')
            time.sleep(3)
            os.system('clear')
            startup2()
            mainmenu()
    elif Option2 == 'N':
        print('Fantastic!')
        time.sleep(3)
        os.system('clear')
        startup2()
        mainmenu()

    #user puts in invalid request
    else:
        print('Invalid Option')
        time.sleep(3)
        os.system('clear')
        startup2()
        mainmenu()
startup()
mainmenu()
