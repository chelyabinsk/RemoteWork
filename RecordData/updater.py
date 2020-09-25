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
    new_json = r.json()
    return new_json

def local_version():
    with open('../version.info','r') as f:
        return json.loads(f.read())
    
def create_version():
#    version = {'version':2}
#    changed_files = {'newfiles':[{'none':'none'}]}
    data = {'version':2,'newfiles':[{'none':'none'}]}
    with open('../version.info','w') as f:
        f.write(json.dumps(data))
a= new_version()
create_version()
b = local_version()

        