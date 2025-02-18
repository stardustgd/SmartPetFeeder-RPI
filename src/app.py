from AtlasClient import AtlasClient
from dotenv import load_dotenv
import os

load_dotenv()

ATLAS_URI = os.getenv("ATLAS_URI")
DB_NAME = os.getenv("DB_NAME")

atlas_client = AtlasClient(ATLAS_URI, DB_NAME)
atlas_client.ping()

atlas_client.add_mac_address("")
