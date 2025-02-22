from cron import set_cron_jobs
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

    def get_schedules(self, user_email):
        collection = self.get_collection("schedules")

        return collection.find_one({"user": user_email})

    def get_manual_feeding_amount(self, user_email):
        collection = self.get_collection("manualFeedings")

        return collection.find_one({"user": user_email})["manualFeedingAmount"]

    def listen_for_changes(self, user_email, CRON_SCRIPT_PATH):
        collection = self.get_collection("schedules")

        pipeline = [
            {
                "$match": {
                    "fullDocument.user": user_email,
                    "operationType": {"$in": ["update"]},
                }
            }
        ]

        with collection.watch(
            pipeline=pipeline, full_document="updateLookup"
        ) as stream:
            for change in stream:
                operation_type = change["operationType"]

                if operation_type == "update":
                    print("change")
                    set_cron_jobs(change["fullDocument"], CRON_SCRIPT_PATH)
