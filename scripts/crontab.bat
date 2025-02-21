@echo off
REM Define the cron jobs file path
set CRON_FILE=cron_jobs.txt

REM Check if the cron_jobs.txt file exists
if exist "%CRON_FILE%" (
    echo "%CRON_FILE% found. Setting up scheduled tasks..."
    
    REM Display the cron jobs (this will print the contents of cron_jobs.txt)
    echo "Scheduled cron jobs in %CRON_FILE%:"
    type "%CRON_FILE%"
    
    REM Read each line from cron_jobs.txt and set it up as a scheduled task
    for /f "tokens=1-6" %%i in (%CRON_FILE%) do (
        REM %%i=minute, %%j=hour, %%k=day, %%l=month, %%m=weekday, %%n=command
        REM Convert the weekday to Task Scheduler format
        set DAY_OF_WEEK=%%m

        REM Convert days of the week to Task Scheduler's /d option (MON, TUE, WED, THU, FRI, SAT, SUN)
        if /i "%%m"=="monday" set DAY_OF_WEEK=MON
        if /i "%%m"=="tuesday" set DAY_OF_WEEK=TUE
        if /i "%%m"=="wednesday" set DAY_OF_WEEK=WED
        if /i "%%m"=="thursday" set DAY_OF_WEEK=THU
        if /i "%%m"=="friday" set DAY_OF_WEEK=FRI
        if /i "%%m"=="saturday" set DAY_OF_WEEK=SAT
        if /i "%%m"=="sunday" set DAY_OF_WEEK=SUN

        REM Create a scheduled task for each line, setting up the task time and command
        schtasks /create /tn "MyTask %%m %%i %%j %%k %%l" /tr "%%n" /sc weekly /st %%j:%%i /d %DAY_OF_WEEK%
    )
    
    echo "Scheduled tasks set up."
) else (
    echo "%CRON_FILE% is invalid or does not exist."
)
