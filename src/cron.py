import subprocess
from dotenv import load_dotenv
import os

load_dotenv()
CRON_SCRIPT = os.getenv("CRON_SCRIPT")


def format_cron_jobs(results, SCRIPT_PATH):
    cron_jobs = []
    schedules = results["schedule"]

    for schedule in schedules:
        days = schedule["days"]
        time = schedule["time"].split(":")
        feeding_amount = schedule["feedingAmount"]

        for day in days:
            cron_jobs.append(
                f"{time[1]} {time[0]} * * {day} {SCRIPT_PATH} {feeding_amount}"
            )

    return cron_jobs


def set_cron_jobs(results, SCRIPT_PATH):
    cron_jobs = format_cron_jobs(results, SCRIPT_PATH)

    with open("cron_jobs.txt", "w") as f:
        for job in cron_jobs:
            f.write(job + "\n")

    result = subprocess.run([CRON_SCRIPT], capture_output=True, text=True)
    print(result.stdout)
