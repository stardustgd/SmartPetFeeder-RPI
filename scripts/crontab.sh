#!/bin/bash

CRON_FILE="cron_jobs.txt"

if [[ -f "$CRON_FILE" ]]; then
  cat "$CRON_FILE" | sort | uniq 
else
  echo "$CRON_FILE is invalid or does not exist"
fi
