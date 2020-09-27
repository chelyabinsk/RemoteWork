# -*- coding: utf-8 -*-
"""
Basic updater script

I am using my GitHub to host the latest version of the code

If new version is found on github then referenced files are replaced in the folder
"""

import requests
import json
from urllib.request import urlopen

base_url = 'https://raw.githubusercontent.com/chelyabinsk/RemoteWork/master/'

def new_version():
    r = requests.get(base_url+'version.info')
    new_json = r.json()
    return new_json

def local_version():
    with open('version.info','r') as f:
        return json.loads(f.read())
    
def create_version():
    data = {'version':2,'newfiles':[{'localfile':'hello.txt','remotefile':'https://raw.githubusercontent.com/chelyabinsk/RemoteWork/master/Makefile'}]}
    with open('version.info','w') as f:
        f.write(json.dumps(data))
#create_version()
new_files = new_version()
local_files = local_version()

if new_files['version'] > local_files['version']:
    # Download all of the new files
    for file in new_files['newfiles']:
        data = urlopen(file['remotefile'])
        with open(file['localfile'],'w') as f:
            for line in data:
                decoded_line = line.decode('utf-8')
                f.write(decoded_line)
    # Update the version.info file
    data = urlopen(base_url + 'version.info')
    with open('version.info','w') as f:
        for line in data:
            decoded_line = line.decode('utf-8')
            f.write(decoded_line)
exit()
