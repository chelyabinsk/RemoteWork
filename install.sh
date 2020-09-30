#write out current crontab
#crontab -l > mycron
mycron=""
#echo new cron into cron file
echo "* * * * * cd '$PWD/RecordData' && $(which python3) check_run_status.py >> '$PWD/cron_scraper.log' 2>&1" >> mycron
echo "0 */2 * * * cd '$PWD' && $(which python3) updater.py >> '$PWD/cron_updater.log' 2>&1" >> mycron
#install new cron file
crontab mycron
rm mycron*
