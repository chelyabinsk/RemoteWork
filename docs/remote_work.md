# Introduction

RecordData task aims to record data on livestreams performance from a number of YouTube channels. Results are uploaded daily to my GoogleDrive folder. Naturally, I cannot share the `client_secrets.json` file hence this code will not run without it. The main scraper code can be found in the [YTLiveScrape](https://github.com/BambooFlower/LiveYoutube-Scraper) repository.

## High-level overview
The main flow of the program is summarised in the following section

1. Every hour check each YouTube channel in question to see if it has any livestreams in coming. If  they do then save the start time and the video link into the `self.streams`dictionary
2. Create an infinite loop in a separate thread
3. For each stream in `self.streams` which is about to start in 5 minutes create an instance of the YTLiveScrape worker and append the `self.active_streams` dictionary
4. Save comments and stats for each worker in `self.active_streams`
5. If stream has stopped remove it from the `self.active_streams` dictionary
6. If current time is 2:00AM create a zip file and upload it to GDrive
7. GOTO 3.

## Description of the functions

### start()
The function that starts the main loop in the thread. Used to initiliase the task.

### stop()
The function to stop the execution of the main loop by setting the `self.running` boolean to `False`.

### check_channels()
Function to update the `self.streams` dictionary by visiting each of the channels in `self.channels` and recording their start time and a link to the video.

### check_channel_list()
A very lazy function to return the ids of the channels I want to scrape. In the future I will read an external text file.

### write_file()
A small helper function to write a dictionary as tab separated value file (tsv).

### start_scraper(link)
The function to initialise the YTLiveScraper on the livestream located at the given link. If the link is valid then the `self.active_streams` dictionary is appended. On the other hand, if it was found that the given link is not valid then it is also removed from the `self.streams` dictionary. 

### update_workers()
A housekeeping function to ensure that only actively running streams are kept in the `self.active_streams` dictionary.

### create_path(path)
A helper function to create a path if it does not already exist.

### preprocess_text(text)
Since the original purpose of this project was to collect comments to train a machine to identify the source of the message I found that it is much simpler to do basic tokenisation and removal of the stop words at the data collecting step.

### write_output()
A general function which iterates through all of the active workers in the `self.active_streams` and writes the comments and stats to the appropriate output files. An origin of the data is also added as well as the preprocessed text along side the original comment. The output files are saved in the `comments/` and `viewers/` folders which are created if they do not already exist.

### update_status_file()
A small helper function which writes the current epoch time into the `last_run.txt`. I use this to check whether the current worker is active or not. I know that this is not ideal, but hey, it works. I will improve it when I find a better alternative.

### stop_all_workers()
This function iterates through all of the active scraper workers in the `self.active_streams` and for each calls the `stop_scrape()` function. Once that function is called within the worker, that worker is terminated and the `self.active_streams` dictionary is made empty. This is a very convoluted way to stop all of the scrapes that are in the separate threads. I am looking for a better solution to this. I found that daemon threads die with the parent, so I might restructure my program to take advatage of that.

### main_loop()
As the name suggest this is loop which is called within the thread initialised by the `start()` function. Every 60 seconds it checks whether there is a need to write an output, check the channels or update the current dictionary of the active threads.
