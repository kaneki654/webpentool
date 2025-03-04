import time
import requests
import os
import platform
from oth.instsqlmap import *
import subprocess

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
GITHUB_REPO_URL = "https://github.com/kaneki654/webpentool.git"
BRANCH = "main"

def pull_latest_changes():
    try:
        os.chdir(REPO_DIR)
        if not os.path.isdir(os.path.join(REPO_DIR, ".git")):
            print("Error: This is not a Git repository.")
            return
        subprocess.run(["git", "pull", "origin", BRANCH], check=True)
        print("Successfully pulled the latest changes.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to pull changes: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

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
    (6) DEFACE LISTER
    (X) UPDATE
    ''')

def choice():
    mainzap()
    cho = input("choose 1: ").strip().lower()

    if cho == '1':
        try:
            print('''
            (1) REVERSE IP(only 1 domain)
            (2) REVERSE IP(using txt lists)
            (3) SCANNER
            ''')
            echo = input('choose: ').strip().lower()
            if echo == '1': 
                os.system('python tools/astro.py')
            elif echo == '2':
                os.system('python tools/rever.py')
            elif echo == '3':
                os.system('python tools/mass-web-ip-scanner.py')
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
    elif cho == '6':
        os.system('python tools/mass-deface-lister.py')
    elif cho == 'x':
        pull_latest_changes()
    else:
        print("unknown choice")
        choice()

if __name__ == "__main__":
    choice()
