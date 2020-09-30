# -*- coding: utf-8 -*-
"""
Check whether the scraper is running. If not then start the scraper
I assume that the working directory is set correctly...
"""
import time
#from subprocess import Popen, DEVNULL
import os
import datetime
from uploader import make_ping,upload_youtube_data,share_error
import logging
from importlib import reload


def exec_run():
    import find_steams
    # Create a logging instance
    logger = logging.getLogger('YouTubeScraper')
    logger.setLevel(logging.DEBUG) 
    
    # Assign a file-handler to that instance
    fh = logging.FileHandler("errors.log")
    fh.setLevel(logging.DEBUG) 
    
    # Format your logs (optional)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter) # This will set the format to the file handler
    
    # Add the handler to your logging instance
    logger.addHandler(fh)
    
    try:
        S = find_steams.StreamWorker()
        S.start()
    except Exception as e:
        logger.exception(e) # Will send the errors to the file
        share_error('errors.log')
    
    while 1:
    
        now = datetime.datetime.now()
        
        if now.minute % 15 == 0:
            make_ping()
        if now.hour == 2 and now.minute == 4:
            upload_youtube_data()
        if now.hour == 2 and now.minute == 5:
            S.stop()
            find_steams = reload(find_steams)
            
            try:
                S = find_steams.StreamWorker()
                S.start()
            except Exception as e:
                logger.exception(e) # Will send the errors to the file
                share_error('errors.log')
        
        
        time.sleep(40)
    
do_run = False
if os.path.exists('last_run.txt'):
    with open('last_run.txt','r') as f:
        last_time = eval(f.read())
    if time.time() - last_time > 120:
        do_run = True
else:
    do_run = True
    
if do_run:
    exec_run()
    