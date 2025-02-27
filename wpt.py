import time
import requests
import os
import platform
from oth.instsqlmap import *

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

banner = rf'''
__        __   _     ____          _____           _     
\ \      / /__| |__ |  _ \ ___ _ _|_   _|__   ___ | |___ 
 \ \ /\ / / _ \ '_ \| |_) / _ \ '_ \| |/ _ \ / _ \| / __|
  \ V  V /  __/ |_) |  __/  __/ | | | | (_) | (_) | \__ \
   \_/\_/ \___|_.__/|_|   \___|_| |_|_|\___/ \___/|_|___/
'''

def mainzap():
    print(banner)
    print('''
    (1) REVERSEIP
    (2) PATHFINDER
    (3) SQLMAP
    (4) SPIDER
    (5) LARVA
    ''')

def choice():
    mainzap()
    cho = input("choose 1: ").strip().lower()

    if cho == '1':
        try:
            os.system('python tools/astro.py')
        except KeyboardInterrupt:
            clear()
            print('session interrupted')
    
    elif cho == '2':
        try:
            print('first create a txt file')
            do = input('name.txt(with .txt): ').strip().lower()
            con = input('paste the domains: ').strip().lower()

            with open(do, 'w') as file:
                file.write(con)

            print('done')

            try:
                fu = input('type run: ').strip().lower()

                if fu == 'run':
                    os.system('python tools/StarPathFinder.py')
                else:
                    print('try again')
                    choice()
            except KeyboardInterrupt:
                print('keys interrupted') 
        except KeyboardInterrupt:
            print('session interrupted')
    elif cho == '3':
        check_sql()
    elif cho == '4':
        os.system('python tools/spider.py')
    elif cho == '5':
        os.system('python tools/larva.py')
    else:
        print("unknown choice")
        choice()

if __name__ == "__main__":
    choice()