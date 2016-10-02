#! /bin/sh -

logfile=~/telegram-bot/restart.log

# Don't allow the log file to grow beyond 10M. Preserve last 100 entries.
if [ $(stat --printf="%s" "$logfile") -ge $((10 * 1024 * 1024)) ]
then
  tmpfile=$(mktemp)
  tail -n 100 "$logfile" > "$tmpfile"
  mv "$tmpfile" "$logfile"
fi

if (! ps -Af | grep secretary[.]py | grep -v grep > /dev/null 2>&1 )
then
  cd ~/telegram-bot
  screen -d -m ./secretary.py # Start in a detached screen session.
  echo "restarting `date`" >> "$logfile"
fi
