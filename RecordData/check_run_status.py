# -*- coding: utf-8 -*-
"""
Check whether the scraper is running. If not then start the scraper
I assume that the working directory is set correctly...
"""
import time
from subprocess import Popen, DEVNULL

with open('last_run.txt','r') as f:
    l = eval(f.read())

#print(time.time() - l)
#if time.time() - l > -1:
if time.time() - l > 120:
    Popen(['nohup', '/usr/bin/python3' ,'find_steams.py'], stdout=DEVNULL, stderr=DEVNULL)
#    Popen(['nohup', '/usr/bin/python3' ,'hi.py'], stdout=DEVNULL, stderr=DEVNULL)
exit()        
