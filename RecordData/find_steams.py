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

import threading

from YTLiveScrape.live_chat_worker import LiveMachine

import nltk
#import pandas as pd
nltk.download("stopwords")
#--------#

from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation

#Create lemmatizer and stopwords list
mystem = Mystem() 
russian_stopwords = stopwords.words("russian")

class StreamWorker():
    def __init__(self):
        self.streams = {}
        self.active_streams = {}
        self.channels = self.check_channel_list()
        self.checked_channels = False
        self.cookies = None
        self.stopping = False
        self.check_channels()
        
    
    def start(self):
        x = threading.Thread(target=self.main_loop)
        x.daemon = True
        x.start()
        
    def stop(self):
        self.stopping = True
        
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
            
    #Preprocess function
    def preprocess_text(self,text):
        try:
            tokens = mystem.lemmatize(text.lower())
        except AttributeError:
            return text        
        tokens = [token for token in tokens if token not in russian_stopwords\
                  and token != " " \
                  and token.strip() not in punctuation]
        
        text = " ".join(tokens)
        r = re.compile("[а-яА-Я\s]+")
        text = " ".join(re.findall(r, text))
    #    text = [w for w in filter(r.match, text)]    
        return text
    
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
                    comment['clean'] = self.preprocess_text(comment['message'])
                    self.write_file('{}.txt'.format(comments_filename),comment)
                    
            stats = L.get_stats()
            for stat in stats:
                stat['channel_id'] = L.channel_id
                stat['channel_name'] = L.video_author
                stat['video'] = L.video_id
                self.write_file('{}.txt'.format(viewers_filename),stat)
            if not stats == []:
                #print('{} has {} viewers'.format(L.video_name,stats[-1]['viewers']))
                pass
    
    def update_status_file(self):
        with open('last_run.txt','w') as f:
            f.write(str(time.time()))
    
    def stop_all_workers(self):
        for worker in self.active_streams.keys():
            L = self.active_streams[worker]['machine']
            L.stop_scrape()
        self.active_streams = {}
    
    def main_loop(self):
        while 1:
            self.update_status_file()
            
            if self.stopping:
                print('Stopping all workers')
                self.stop_all_workers()
                print("Stopping the main loop")                
                break
            
            # Run loop every minute
            # check whether any of the streams are within 2 minutes of the start
            now = datetime.datetime.now()
            
            self.update_workers()
            
            #print()
            #print(now)
            for video_id in self.streams.keys():
                minutes_to_start = (self.streams[video_id]['start_time']-time.time())/60
                if minutes_to_start > 0:
                    #print('{} to start in {:.2f} minutes'.format(video_id,minutes_to_start))
                    pass
                if minutes_to_start < 2:
                    if not video_id in self.active_streams.keys():
#                        print(minutes_to_start)
                        self.start_scraper(video_id)
            #print()
            if (now.minute == 59 or now.minute in (0,1,2)) and self.checked_channels == False:
                self.check_channel_list()
                self.check_channels()
                self.checked_channels = True
            
            if (now.minute == 59 or now.minute in (0,1,2)) and self.checked_channels == True:
                self.checked_channels = False
            
            self.write_output()
            time.sleep(60)
    