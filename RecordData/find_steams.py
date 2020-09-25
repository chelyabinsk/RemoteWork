# -*- coding: utf-8 -*-
"""
Script to identify whether a channel has a stream 

Check each channel at 5 to (whatever hour) to see whether it has a livestream schedulued

Start the scraper 2 minutes before the scheduled start
"""
import os
import requests 
import re
import time
import datetime
import logging

from YTLiveScrape.live_chat_worker import LiveMachine

class StreamWorker():
    def __init__(self):
        self.streams = {}
        self.active_streams = {}
        self.channels = self.check_channel_list()
        self.checked_channels = False
        self.cookies = None        
        self.check_channels()
        
        self.main_loop()        
        
        
    def check_channels(self):
        base_url = 'https://www.youtube.com/channel/{}'

        for channel in self.channels:
            url = base_url.format(channel)
            r = requests.get(url)

            
            matches = re.findall('("startTime":"[0-9]+"(.*?)videoId":"[Aa0-zZ9_-]+")',r.text)
            if matches == []:
                # Find all live videos
                matches = re.findall('([0-9]+ watching(.*?)videoId":"[aA0-zZ9_-]+")',r.text)
                for m in matches:
                    video_match = re.findall('videoId":"[Aa0-zZ9_-]+',m[0])
                    
                    video_id = video_match[0].replace('videoId":"','')
                    start_time = time.time()
                    
                    self.streams[video_id] = {'start_time':int(start_time)}
            else:                
                # Find all scheduled videos
                for m in matches:
                    video_match = re.findall('videoId":"[Aa0-zZ9_-]+',m[0])
                    time_match = re.findall('startTime":"[0-9]+',m[0])
                    
                    video_id = video_match[0].replace('videoId":"','')
                    start_time = time_match[0].replace('startTime":"','')
                    
                    self.streams[video_id] = {'start_time':int(start_time)}
                
                # Find all live videos
                matches = re.findall('([0-9]+ watching(.*?)videoId":"[aA0-zZ9_-]+")',r.text)
                if matches != []:
                    for m in matches:
                        video_match = re.findall('videoId":"[Aa0-zZ9_-]+',m[0])
                        
                        video_id = video_match[0].replace('videoId":"','')
                        start_time = time.time()
                        
                        self.streams[video_id] = {'start_time':int(start_time)}
    
    def check_channel_list(self):
        return ['UCdubelOloxR3wzwJG9x8YqQ','UCQ4YOFsXjG9eXWZ6uLj2t2A','UCo4GExFphiUnNiMMExvFWdg','UCgxTPTFbIbCWfTR9I2-5SeQ']
    
    def write_file(self,filename,data):
        import os
        if not os.path.exists(filename):
            with open(filename,'w',encoding='utf-8') as f:
                line = ''
                for key in data.keys():
                    line += key + "\t"
                line = line[:-1]
                line +=  "\n"
                f.write(line)
        with open(filename,'a',encoding='utf-8') as f:
            line = ''
            for key in data.keys():
                tmp = str(data[key])
                line += tmp.replace("\n","") + "\t"
            line = line[:-1]
            line +=  "\n"
            f.write(line)
    
    def start_scraper(self,link):
        
        L = LiveMachine(link,cookies=self.cookies)
        if not self.cookies is None:
            self.cookies = L.session.cookies
        
        if L.has_data:
            L.request_stats()
            if L.comments_enabled:
                L.request_comments()
                pass
            
            if L.is_a_stream:
                details = {'machine':L}                
                self.active_streams[link] = details
                print('Added video {}'.format(link))
            else:
                self.streams.pop(link)
                print('Removed {} due to not being a valid stream'.format(link))
        
    
    def update_workers(self):
        # Manage the active_streams dictionary to only keep streams that are active
        tmp = dict(self.active_streams)
        for worker in tmp.keys():
            L = tmp[worker]['machine']
            if L.initialised:
                if not L.stats_running:
                    self.active_streams.pop(worker)
                    print('Removed video {}'.format(worker))
                    
    def create_path(self,path):
        if not os.path.exists(path):
            os.makedirs(path)
    
    def write_output(self):
        # Function to handle all of the writing to the file
        # Go through all of the active machines and grab their outputs
        todaydate = datetime.datetime.today().strftime('%Y-%m-%d')
        
        comments_filename = 'comments/{}'.format(todaydate)
        viewers_filename = 'viewers/{}'.format(todaydate)
        
        self.create_path('comments')
        self.create_path('viewers')
        
        for worker in self.active_streams.keys():
            L = self.active_streams[worker]['machine']
            
            if L.comments_enabled:                
                comments = L.get_comments()
                for comment in comments:
                    comment['channel'] = L.channel_id
                    comment['channel_name'] = L.video_author
                    comment['video'] = L.video_id
                    self.write_file('{}.txt'.format(comments_filename),comment)
                    
            stats = L.get_stats()
            for stat in stats:
                stat['channel_id'] = L.channel_id
                stat['channel_name'] = L.video_author
                stat['video'] = L.video_id
                self.write_file('{}.txt'.format(viewers_filename),stat)
            if not stats == []:
                print('{} has {} viewers'.format(L.video_name,stats[-1]['viewers']))
    
    def update_status_file(self):
        with open('last_run.txt','w') as f:
            f.write(str(time.time()))
    
    def main_loop(self):
        while 1:
            self.update_status_file()
            # Run loop every minute
            # check whether any of the streams are within 2 minutes of the start
            now = datetime.datetime.now()
            
            self.update_workers()
            
            print()
            print(now)
            for video_id in self.streams.keys():
                minutes_to_start = (self.streams[video_id]['start_time']-time.time())/60
                if minutes_to_start > 0:
                    print('{} to start in {:.2f} minutes'.format(video_id,minutes_to_start))
                if minutes_to_start < 2:
                    if not video_id in self.active_streams.keys():
#                        print(minutes_to_start)
                        self.start_scraper(video_id)
            print()
            if (now.minute == 59 or now.minute in (0,1,2)) and self.checked_channels == False:
                self.check_channel_list()
                self.check_channels()
                self.checked_channels = True
            
            if (now.minute == 59 or now.minute in (0,1,2)) and self.checked_channels == True:
                self.checked_channels = False
            
            # Stop at 2:05
            if now.hour == 2 and now.minute == 5:
                exit()
            
            self.write_output()
            time.sleep(60)

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
    S = StreamWorker()
except Exception as e:
    logger.exception(e) # Will send the errors to the file


