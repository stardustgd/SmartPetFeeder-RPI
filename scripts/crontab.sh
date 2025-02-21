#!/bin/bash

CRON_FILE="cron_jobs.txt"

if [[ -f "$CRON_FILE" ]]; then
  crontab $CRON_FILE
else
  echo "$CRON_FILE is invalid or does not exist"
fi
