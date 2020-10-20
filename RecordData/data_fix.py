import pandas as pd
import numpy as np
import datetime
#import github
import requests
import base64

import json
from http import HTTPStatus
import subprocess as cmd

import glob
from pathlib import Path

def gen_file(repo):
        todaydate = datetime.datetime.today().strftime('%Y-%m-%d')
        df = pd.read_csv(glob.glob('viewers/*.txt')[0],sep="\t")
        sub_df = df.loc[(df['live']==True) ,['timestamp','viewers','channel_name']]
        #sub_df = df[['timestamp','viewers','channel_name']]
        sub_df[['timestamp']] = pd.to_datetime(sub_df['timestamp']+60*60*2,unit='s')
        sub_df = sub_df.sort_values('timestamp')
        tmp = list(sub_df['timestamp'])[0].date()
        year = tmp.year
        month = str(tmp.month).rjust(2,'0')
        day = str(tmp.day).rjust(2,'0')
        out_name = '../../{}/data/{}-{}-{}.csv'.format(repo,year,month,day)
        export_df = sub_df.pivot_table(values='viewers', index=['timestamp'],columns='channel_name', aggfunc=np.sum)
        export_df.to_csv(out_name)
        print(out_name)
        return out_name,tmp

def update_date(m,d,y,raw_url,repo):
        r = requests.get(raw_url)
        if r.status_code == 200:
            file = r.text
        good_dates_line = file[:file.find('];')+3]
        other_file = file[file.find('];')+3:]
        good_dates_line = good_dates_line.replace('];',",'{}/{}/{}'];".format(m,d,y))
        final_file = good_dates_line + other_file
        with open('../../{}/calendar.js'.format(repo).format(repo),'w') as f:
                f.write(final_file)
        return './../{}/calendar.js'.format(repo)
        #tmp = f

def gh_procedure():
        todaydate = glob.glob('viewers/*.txt')[0]
        with open('../gh.token','r') as f:
            tmp = f.read().split("\n")
            email = tmp[1]
            token = tmp[0]
            url = tmp[2]
            repo = tmp[3]
            raw_url = tmp[4]

        try:
            cp = cmd.run('cd ../..; git clone {}'.format(url),check=True,shell=True)
        except:
            cp = cmd.run('rm ../../{} -rf'.format(repo),check=True,shell=True)
            cp = cmd.run('cd ../..; git clone {}'.format(url),check=True,shell=True)
        #print('../..; git clone {}'.format(url)) 
        a=gen_file(repo)
        year = a[1].year
        month = str(a[1].month).rjust(2,'0')
        day = str(a[1].day).rjust(2,'0')
        b=update_date(month,day,year,raw_url,repo)

        home = str(Path.home())
        
        with open('{}/.git-credentials'.format(home),'w') as f:
            f.write('https://{}:{}@github.com\n'.format(email,token))
        try:
            #print("add files")
            cmd.run('cd ../../{}; git add .'.format(repo),check=True,shell=True)
            #print("commit")
            cmd.run('cd ../../{}; git commit -am "{} upload"'.format(repo,todaydate),check=True,shell=True)
            #print("push")
            cmd.run("""cd ../../{}; git push https://{}:{}@github.com/{}/{}.git""".format(repo,email,token,email,repo),check=True,shell=True)
        except:
            print("oh dear! git fucked up")
        cp = cmd.run('rm ../../{} -rf'.format(repo),check=True,shell=True)

#gh_procedure()

