# -*- coding: utf-8 -*-
"""
Basic updater script

I am using my GitHub to host the latest version of the code

If new version is found on github then referenced files are replaced in the folder
"""

import requests
import json

base_url = 'https://raw.githubusercontent.com/chelyabinsk/RemoteWork/master/'

def new_version():
    r = requests.get(base_url+'version.info')
    print(r.text)
    
def create_version():
    version = {'version':2}
    changed_files = [{'none':'none'}]
    data = {'data':[version,changed_files]}
    with open('version.info','w') as f:
        f.write(json.dumps(data))
#new_version()
create_version()