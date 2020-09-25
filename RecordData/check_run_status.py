# -*- coding: utf-8 -*-
"""
Check whether the scraper is running. If not then start the scraper
I assume that the working directory is set correctly...
"""
import time
from subprocess import Popen, DEVNULL
import os

do_run = False
if os.path.isfile('last_run.txt'):
    with open('last_run.txt','r') as f:
        l = eval(f.read())
    if time.time() - l > 120:
        do_run = True
else:
    do_run = True

if do_run:
    Popen(['nohup', '/opt/anaconda3/bin/python3' ,'find_steams.py'], stdout=DEVNULL, stderr=DEVNULL)
#    Popen(['nohup', '/usr/bin/python3' ,'hi.py'], stdout=DEVNULL, stderr=DEVNULL)
exit()        
