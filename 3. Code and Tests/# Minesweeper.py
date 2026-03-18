# Import area
import rich
import time
import sys 
import os

# Minesweeper
def begin():
    #welcome and options page 1
    intro = 'Welcome to'
    for char in intro:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.2)

    time.sleep(1)
    print('\n')
    title = (r'''
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
    for t1 in title:
        sys.stdout.write(t1)
        sys.stdout.flush()
        time.sleep(0.001)
    print('\n')
    time.sleep(2)
    intro2 = 'Thank you for willingly participating'
    for bark in intro2:
        sys.stdout.write(op1)
        sys.stdout.flush()
        time.sleep(0.1)
    print('\n)')
    print('Options')
    print('1. Play Game')
    print('2. Access Scoreboard')
    print('3. Exit')
    print('\n')

    Option = input('Choose an option:')
    if Option == '1':
        quit()
    if Option == '2':
        quit()
    if Option == '3':
        quit()

    input('press enter to exit')

begin()