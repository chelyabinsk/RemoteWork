# RemoteWork
My remote "server" code.

## Installation
Exctract all files and run `make` 

## What does it do
This repository creates a cron task that checks for updates every 2 hours. 
When a new update is detected, files are downloaded and "installed". This is what allows me to
upload and run the code remotely, the results are then uploaded to my GoogleDrive folder.

At the moment I am only using this repository to scrape data from a couple of YouTube live streaming channels.

The basic data flow is shown in the following [picture](doct/flow.png)

## Documentation
A more detailed documentation of the project can be found [here](https://chelyabinsk.github.io/RemoteWork/).
