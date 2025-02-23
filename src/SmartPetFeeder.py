import os
import sys
from AtlasClient import AtlasClient
from cron import set_cron_jobs
from dotenv import load_dotenv


class SmartPetFeeder:
    def __init__(self):
        self.USER_EMAIL = sys.argv[1]
        self.ATLAS_URI = os.getenv("ATLAS_URI")
        self.DB_NAME = os.getenv("DB_NAME")
        self.CRON_SCRIPT_PATH = os.getenv("CRON_SCRIPT_PATH")

    def setup(self):
        try:
            self.atlas_client = AtlasClient(self.ATLAS_URI, self.DB_NAME)
            self.atlas_client.ping()
        except Exception as e:
            raise e
            sys.exit(1)

        # Add RPi mac address to database
        self.atlas_client.add_mac_address(self.USER_EMAIL)

        # Get the user's schedules and create cron jobs
        results = self.atlas_client.get_schedules(self.USER_EMAIL)
        set_cron_jobs(results, self.CRON_SCRIPT_PATH)

    def run(self):
        self.setup()

        self.atlas_client.listen_for_changes(self.USER_EMAIL, self.CRON_SCRIPT_PATH)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <email>")
        sys.exit(1)

    load_dotenv()

    try:
        spf = SmartPetFeeder()
        spf.run()
    except Exception as e:
        raise e
