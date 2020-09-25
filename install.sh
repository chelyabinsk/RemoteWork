#write out current crontab
crontab -l > mycron
#echo new cron into cron file
echo "* * * * * cd $PWD/RecordData && $(which python3) check_run_status.py >> $PWD/cron.log 2>&1" >> mycron
echo "00 09 * * 1-5 echo hi" >> mycron
#install new cron file
crontab mycron
rm mycron*