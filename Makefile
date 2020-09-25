# Makefile to install the remote processing script
# [x] Set cron to check that the script is running (every minute) 
# [•] Set cron to run the updater script at 3AM
# [•] Set cron to upload data to GDrive and remove all old data

current_dir = $(shell pwd)

# Create cron tasks
addcron: install.sh
	chmod +x install.sh
	$(current_dir)/$<