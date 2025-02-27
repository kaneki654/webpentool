import requests
import time
import os
import subprocess
import sys
import shutil
import urllib.request
import zipfile
import platform

def check_sqlw():
    if os.name == "nt":
        rootdir = "C:\\"

    print(f"searching for SQLMap in {rootdir} please wait.. ") 

    for dirpath, dirnames, filenames in os.walk(rootdir):
        if "sqlmap" in dirnames:
            sqlth = os.path.join(dirpath, "sqlmap")
            sqlpy = os.path.join(sqlth, "sqlmap.py")
            if os.path.exists(sqlpy):
                print(f"SQLMap is already in your directory at: {sqlth}")   
                os.system(f"python {sqlpy} --wizard")
            else:
                print("SQLMap is not installed on your system")
                return False

def check_sql():
    try:
        subprocess.run(["sqlmap", "--wizard"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("SQLMap is already installed.")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("SQLMAP is not installed.")
        use = platform.system()
        if use == 'Windows':
            Wintyp()
        elif use == 'Linux':
            linuxtyp()
        else:
            print('unavailable operating system')
        return False
def Wintyp():
    if check_sqlw():
        print("SQLMap is already on your system")
    else:
        print("proceeding installation of sqlmap")
        time.sleep(2)
        print('Welcome to the installation of sqlmap for windows')
        time.sleep(2)
        a = "https://github.com/sqlmapproject/sqlmap/archive/master.zip"
        s = "sqlmap-master.zip"
        e = "sqlmap-master"

        print("Installing SQLMap...")
        urllib.request.urlretrieve(a, s)

        print("Extracting SQLMap")
        with zipfile.ZipFile(s, 'r') as zip_ref:
            zip_ref.extractall()
        
        os.remove(s)

        if os.path.exists("sqlmap"):
            shutil.rmtree("sqlmap")
        shutil.move(e, "sqlmap")

        print("SQLMap has been successfully Installed")
        time.sleep(2)
        successWintyp()

def successWintyp():
    rt = input("Do you want to add sqlmap in yout system path?(y/n)").strip().lower()
    if rt == 'y':
        adsql()
    elif rt == 'n':
        print("okay")
        time.sleep(2)
        os.system("python ../wpt.py")
    else:
        print('unavailable choice')
        successWintyp()

def adsql(): 
    cp = os.environ.get('PATH', '')

    sqlpath = os.path.abspath('sqlmap')
    if sqlpath not in cp:
        os.environ['PATH'] = f"{sqlpath};{cp}"
        print(f"Added {sqlpath} to the system PATH")
    else:
        print('SQLMap is already in the system PATH')      

def installation_package():
    print("Trying to install SQLMap using package manager")
    try:
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run(["sudo", "apt", "install", "-y", "sqlmap"], check=True)
        print("SQLMap installed successfully using package manager")    
        return True
    except subprocess.CalledProcessError:
        print('Failed to Download SQLMap using package manager')
        return False

def Linxtypgit():
    o = "https://github.com/sqlmapproject/sqlmap/archive/master.tar.gz"
    t = "slqmap-master.tar.gz"
    v = "sqlmap-master"

    print('Downloading SQLMap from github')
    urllib.request.urlretrieve(o, t)

    print("Extracting SQLMap...")
    with tarfile.open(t, 'r:gz') as tar_ref:
        tar_ref.extractall()
    

    os.remove(t)

    if os.path.exists("sqlmap"):
        shutil.rmtree("sqlmap")
    shutil.move(v, "sqlmap")
    print("SQLMap has been installed successfully from github")

    addpath = input("Do you want to add SQLMap to your system PATH? (y/n)").strip().lower()
    if addpath == 'y':
        addsqlpath()
    
def addsqlpath():
    sqlmapath = os.path.abspath("sqlmap")
    shellprof = os.path.expanduser("~/.bashrc")
    if not os.path.exists(shellprof):
        shellprof = os.path.expanduser("~/.zshrc")
    with open(shellprof, "a") as f:
       f.write(f"\nexport PATH=\"$PATH:{sqlmapath}\"\n")
    print(f"Added {sqlmapath} to the system PATH. please restart your system first")

def linuxtyp():
    print('Welcome tot the installation of sqlmap for windows')
    time.sleep(2)
    if not installation_package():
        Linxtypgit()
    print("Installation complete. Returning to the script")

    