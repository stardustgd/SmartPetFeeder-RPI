from AtlasClient import AtlasClient
from cron import set_cron_jobs
from dotenv import load_dotenv
import os
import sys

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <email>")
    sys.exit(1)

load_dotenv()

USER_EMAIL = sys.argv[1]
ATLAS_URI = os.getenv("ATLAS_URI")
DB_NAME = os.getenv("DB_NAME")
CRON_SCRIPT_PATH = os.getenv("CRON_SCRIPT_PATH")

atlas_client = AtlasClient(ATLAS_URI, DB_NAME)
atlas_client.ping()

# Add mac address for the user if it doesn't already exist
atlas_client.add_mac_address(USER_EMAIL)

# Get the user's schedules and create cron jobs
results = atlas_client.get_schedules(USER_EMAIL)
set_cron_jobs(results, CRON_SCRIPT_PATH)

atlas_client.listen_for_changes(USER_EMAIL, CRON_SCRIPT_PATH)
