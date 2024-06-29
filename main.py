import subprocess
from datetime import datetime
import os

from colorama import Fore, Style, Back, init
from colorama import just_fix_windows_console

from utils import *

SAVE_DIR = 'snapshots'

def take_snapshot():
    
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    
    # subprocess.run() executes a command and waits for it to complete, capturing its output
    # -ct to get as tab delimiting CVS, * to get ALL entries

    # timestamp = str(int(time.time()))                    # '1719681175'
    timestamp = datetime.now().strftime('%Y-%m-%m')     # '2024-06-06-368334'
    full_path = f'{SAVE_DIR}/{timestamp}_snapshot.csv'

    result = subprocess.check_output(['autorunsc64.exe', '-ct', '-o', full_path])
    
    # output = '\n'.join(result.decode('utf-16').splitlines()[6:])
    # with open(full_path, 'w') as f:
    #     f.write(output)

    return full_path
    

def list_snapshots():
    if not os.path.exists(SAVE_DIR):
        return []
    return sorted(os.listdir(SAVE_DIR))

def compare(new, old):

    with open(new, 'r') as f1, open(old,'r') as f2:
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

if __name__ == '__main__':

    just_fix_windows_console()
    os.system('cls')
    banner()

    print('[+] CAPTURING CURRENT REGISTRY SNAPSHOT...')
    latest = take_snapshot()

    entries = list_snapshots()
    old = entries[len(entries)-2]
    new = entries[len(entries)-1]

    print('\n=================== COMPARING SNAPSHOTS ===================')
    print(f'CURRENT:\t{new}\nPREVIOUS:\t{old}')
    print('===========================================================\n')

    print('[+] COMPARING SNAPSHOTS...\n')
    new_lines, missing_lines = compare(f'{SAVE_DIR}/{new}', f'{SAVE_DIR}/{old}')
    print_entries(new_lines, missing_lines)

    print(Fore.CYAN+"\n[+] DONE!"+Fore.RESET)