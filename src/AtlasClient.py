from pymongo import MongoClient
from getmac import get_mac_address


class AtlasClient:
    def __init__(self, atlas_uri, dbname):
        self.mongodb_client = MongoClient(atlas_uri)
        self.database = self.mongodb_client[dbname]

    def ping(self):
        self.mongodb_client.admin.command("ping")

    def get_collection(self, collection_name):
        collection = self.database[collection_name]
        return collection

    def add_mac_address(self, user_email):
        collection = self.get_collection("usersRPI")
        mac_address = get_mac_address()

        # Add mac_address with email if it doesn't already exist
        collection.update_one(
            {"email": user_email},
            {"$setOnInsert": {"email": user_email, "mac_address": mac_address}},
            upsert=True,
        )
