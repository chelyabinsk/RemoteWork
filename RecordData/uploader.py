# -*- coding: utf-8 -*-
"""
Script to compress all of the new files and upload to GDrive, then to remove all old data
"""
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
import os,shutil

#import py7zr
import tarfile
import datetime

gauth = GoogleAuth()
scope = ['https://www.googleapis.com/auth/drive']
gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name('../client_secrets.json',scope)

drive = GoogleDrive(gauth)

def make_ping():
    file_list = drive.ListFile({'q':"'1al2IsjvVWEFgRPjAj6Rj8wmTGJzuXqBQ' in parents and trashed=false"}).GetList()
    for file1 in file_list:
        #print('title: %s, id: %s' % (file1['title'],file1['id']))
        if file1['title'] == 'ping.txt':
            file1.Delete()
        
    
    file1 = drive.CreateFile(
            {'title':'ping.txt',
                              'parents':[{'id':'1al2IsjvVWEFgRPjAj6Rj8wmTGJzuXqBQ'}]
                              }
            )
    file1.Upload()

def upload_youtube_data():  
    todaydate = datetime.datetime.today().strftime('%Y-%m-%d')
    zip_filename = '{}.tar.gz'.format(todaydate)
    
    # Create an archive
    with tarfile.open(zip_filename, 'w:gz') as archive:
        archive.add('../cron_scraper.log')
        try:
            archive.add('../cron_updater.log')
        except:
            pass
        archive.add('errors.log')
        archive.add('comments/')
        archive.add('viewers/')
    
    # Upload archive
    file1 = drive.CreateFile(
            {'title':zip_filename,
                              'parents':[{'id':'1A_AtZGmB8S34HB4TC1URyjT9HHvOn_o2'}]
                              }
            )
    file1.SetContentFile(zip_filename)
    file1.Upload()
    
    remove_files = True
    
    if remove_files:
        # Remove all old files
        folders = ['viewers','comments']
        for folder in folders:
            for filename in os.listdir(folder):
                file_path = os.path.join(folder,filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path,e))
        # Remove archive
        if os.path.exists(zip_filename):
            os.remove(zip_filename)
        else:
            print('Cannot delete archive {}, doesn`t exist'.format(zip_filename))

def share_error(error):  
    # Upload archive
    file1 = drive.CreateFile(
            {'title':error,
                              'parents':[{'id':'1Us3pMvn7H6Bga9WcK_NyMqkS0jhy9zI5'}]
                              }
            )
    file1.SetContentFile(error)
    file1.Upload()

def test():
    todaydate = datetime.datetime.today().strftime('%Y-%m-%d')
    zip_filename = '{}.tar.gz'.format(todaydate)
    with tarfile.open(zip_filename, 'w:gz') as archive:
        archive.add('../cron_scraper.log')
        try:
            archive.add('../cron_updater.log')
        except:
            pass
        archive.add('errors.log')
        archive.add('comments/')
        archive.add('viewers/')
#test()

#upload_youtube_data()
