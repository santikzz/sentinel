import os
import sys

from colorama import Fore, Style, Back, init
from colorama import just_fix_windows_console

from utils import *
from download import *
from snapshot import *

if __name__ == '__main__':

    just_fix_windows_console()
    os.system('cls')
    banner()

    check_binaries() # check if autoruns64.exe exists
    forceCompare = False

    latest = get_last_snapshot()
    if latest != None:
        print(f'[+] LATEST SNAPSHOT: {latest}')
    
    if sys.argv[1] == '--save':
        print('[+] SAVING CURRENT REGISTRY SNAPSHOT...') 
        current = take_snapshot(save_snapshot=True)
        print(f'[+] SAVED SNAPSHOT IN: {current}')
        # entries = list_saved_snapshots()
        # old = entries[len(entries)-2]
        # new = entries[len(entries)-1]

    if sys.argv[1] == '--nosave':
       print('[+] CAPTUTING CURRENT REGISTRY SNAPSHOT...')
       current = take_snapshot(save_snapshot=False)
       forceCompare = True
    
    if len(sys.argv) == 3 and sys.argv[2] == '--compare' or forceCompare:
        print('\n=================== COMPARING SNAPSHOTS ===================')
        print(f'CURRENT:\t{current}\nPREVIOUS:\t{latest}')
        print('===========================================================\n')

        print('[+] COMPARING SNAPSHOTS...\n')
        new_lines, missing_lines = compare(current, latest)
        print_entries(new_lines, missing_lines)

        print(Fore.CYAN+"\n[+] DONE!"+Fore.RESET)

        if forceCompare:
            os.remove(current)