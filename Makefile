# Makefile to install the remote processing script
# [x] Set cron to check that the script is running (every minute) 
# [x] Set cron to run the updater script at 2:05AM
# [x] Set cron to upload data to GDrive and remove all old data

current_dir = $(shell pwd)

# Create cron tasks
addcron: install.sh
	pip install -i https://test.pypi.org/simple/ YTLiveScrape --user
	pip install upgrade -i https://test.pypi.org/simple/ YTLiveScrape --user
	pip install pandas
	pip install nltk
	pip install pymystem3 --user
	#pip install py7zr --user
	#pip install tarfile --user
	pip install PyDrive --user
	chmod +x install.sh
	sh "$(current_dir)/$<"
