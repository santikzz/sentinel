import subprocess
import time
from datetime import datetime
import os

SAVE_DIR = 'entries'

def save_entries():
    
    
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    
    # subprocess.run() executes a command and waits for it to complete, capturing its output
    # -c to get as CVS, * to get ALL entries

    # output = str(str(subprocess.check_output(['autorunsc64.exe', '-c'])).strip().replace(r"\r", "").split(r"\n"))
    result = subprocess.run(['autorunsc64.exe', '-c'], capture_output=True, text=True)
    output = result.stdout

    # timestamp = str(int(time.time()))                    # '1719681175'
    timestamp = datetime.now().strftime('%Y-%m-%m-%f')     # '2024-06-06-368334'

    full_path = f'{SAVE_DIR}/{timestamp}_entries.csv'
    with open(full_path, 'w') as f:
        f.write(output)

    # with open(full_path, 'w', newline='', encoding='utf-8') as f:
    #     csv_writer = csv.writer(f)
    #     csv_writer.writerow(['Time','Entry Location','Entry','Enabled','Category','Profile','Description','Company','Image Path','Version','Launch String'])

    #     lines = output.strip().splitlines()
    #     for line in lines:
    #         data = line.split('\t')
    #         csv_writer.writerow(data)
    
    return full_path

def list_entries():
    if not os.path.exists(SAVE_DIR):
        return None
    return sorted(os.listdir(SAVE_DIR))

def compare(file1, file2):

    with open(file1, 'r') as f1, open(file2,'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

    lines1_stripped = [line.strip() for line in lines1]
    lines2_stripped = [line.strip() for line in lines2]

    new_lines = set(lines1_stripped) - set(lines2_stripped)
    missing_lines = set(lines2_stripped) - set(lines1_stripped)

    # print(f"New lines in {file1} compared to {file2}:\n")
    # for line in new_lines:
    #     print(line)

    # print(f"\nMissing lines in {file1} compared to {file2}:\n")
    # for line in missing_lines:
    #     print(line)

    return new_lines, missing_lines
    

def print_entries(entries):
    
    
    for entry in entries:
        cols = entry.split(',')
        for col in cols:
            print(col.strip())

if __name__ == '__main__':

    new = save_entries()

    entries = list_entries()
    # print(entries)

    old = entries[len(entries)-2]
    new = entries[len(entries)-1]

    print(f'{old=}, {new=}')
    print('\n')

    new_lines, missing_lines = compare(f'{SAVE_DIR}/{new}', f'{SAVE_DIR}/{old}')

    print_entries(new_lines)

    print("DONE")