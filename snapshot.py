import subprocess
from datetime import datetime
import os
import time

from colorama import Fore, Style, Back, init
from colorama import just_fix_windows_console

from utils import *
from download import *

SAVE_DIR = 'snapshots'
LOG_DIR = 'log'

def take_snapshot(save_snapshot = False):
    
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    if(save_snapshot):
        timestamp = datetime.now().strftime('%Y-%m-%m')  # '2024-06-06-368334'
        full_path = f'{SAVE_DIR}/{timestamp}_snapshot.csv'
        subprocess.check_output(['bin/autorunsc64.exe', '-ct', '-o', full_path])
    
    else:
        timestamp = str(int(time.time()))
        full_path = f'{LOG_DIR}/{timestamp}_temp.csv'
        subprocess.check_output(['bin/autorunsc64.exe', '-ct', '-o', full_path])

    # output = '\n'.join(result.decode('utf-16').splitlines()[6:])
    # with open(full_path, 'w') as f:
    #     f.write(output)

    return full_path
    

def list_saved_snapshots():
    if not os.path.exists(SAVE_DIR):
        return []
    return sorted(os.listdir(SAVE_DIR))

def get_last_snapshot():
    snapshots = list_saved_snapshots()
    if len(snapshots) > 0:
        return f'{SAVE_DIR}/{snapshots[len(snapshots)-1]}'
    return None

def compare(current, latest):

    with open(current, 'r') as f1, open(latest,'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

    lines1_stripped = [line.strip() for line in lines1]
    lines2_stripped = [line.strip() for line in lines2]

    new_lines = set(lines1_stripped) - set(lines2_stripped)
    missing_lines = set(lines2_stripped) - set(lines1_stripped)

    # print(f"New lines in {new} compared to {old}:\n")
    # for line in new_lines:
    #     print(line)

    # print(f"\nMissing lines in {new} compared to {old}:\n")
    # for line in missing_lines:
    #     print(line)

    return new_lines, missing_lines


def print_entries(new_entries, missing_entries):
    
    headers = ['Timestamp','Entry Location','Entry Name','Enabled','Category','Profile','Description','Company','Image Path','Version','Launch String']
    
    if(len(new_entries) > 0):
        print(Fore.RED+"[!] NEW ENTRIES FOUND!"+Fore.RESET)
    else:
        print(Fore.GREEN+"[+] NO NEW ENTRIES FOUND!"+Fore.RESET)

    for entry in new_entries:
        cols = entry.split('\t')
        print(Fore.GREEN+'\n==================================================================')
        for idx, col, in enumerate(cols):
            print(f'{headers[idx]}:\t\t {col.strip()}')
        print('==================================================================\n'+Fore.RESET)

    if(len(missing_entries) > 0):
        print(Fore.RED+"[!] MISSING ENTRIES FOUND!"+Fore.RESET)
    else:
        print(Fore.GREEN+"[+] NO MISSING ENTRIES FOUND!"+Fore.RESET)

    for entry in missing_entries:
        cols = entry.split('\t')
        print(Fore.RED+'\n==================================================================')
        for idx, col, in enumerate(cols):
            print(f'{headers[idx]}:\t\t {col.strip()}')
        print('==================================================================\n'+Fore.RESET)