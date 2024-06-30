import requests
import os
import zipfile
import io

URL = "https://download.sysinternals.com/files/Autoruns.zip"

def check_binaries():

    if not os.path.exists('bin'):
        print('[!] BINARIES DIRECTORY NOT FOUND')
        os.mkdir('bin')
        download()
        
    else:

        if not os.path.exists('bin/autorunsc64.exe') or not os.path.exists('bin/autorunsc.exe'):
            print('[!] BINARIES autorunsc64.exe or autorunsc.exe NOT FOUND, DOWNLOADING...')
            download()
            
def download():    
    response = requests.get(URL)
    if response.status_code == 200:

        zip_file = io.BytesIO(response.content)

        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall('bin')

        print('[+] DOWNLOAD COMPLETE!')
    
    else:
        print('[!] DOWNLOAD FAILED!')