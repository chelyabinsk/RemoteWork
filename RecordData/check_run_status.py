# -*- coding: utf-8 -*-
"""
Check whether the scraper is running. If not then start the scraper
I assume that the working directory is set correctly...
"""
import time
from subprocess import Popen, DEVNULL
import os
import datetime
from uploader import make_ping,upload_youtube_data

now = datetime.datetime.now()

if now.minute % 15 == 0:
    make_ping()
if now.hour == 2 and now.minute == 4:
    upload_youtube_data()

Popen(['nohup', '../install.sh'], stdout=DEVNULL, stderr=DEVNULL)

do_run = False
if os.path.isfile('last_run.txt'):
    with open('last_run.txt','r') as f:
        l = eval(f.read())
    #print(time.time()-l)
    if time.time() - l > 120:
        do_run = True
else:
    do_run = True

if do_run:
    Popen(['nohup', '/opt/anaconda3/bin/python3' ,'find_steams.py'], stdout=DEVNULL, stderr=DEVNULL)
#    pass
#    Popen(['nohup', '/usr/bin/python3' ,'hi.py'], stdout=DEVNULL, stderr=DEVNULL)
        
exit()        
