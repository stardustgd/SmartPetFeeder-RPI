from pymongo import MongoClient
from getmac import get_mac_address
from cron import set_cron_jobs
from dotenv import load_dotenv
import os


class AtlasClient:
    def __init__(self, atlas_uri, dbname):
        load_dotenv()
        self.mongodb_client = MongoClient(atlas_uri)
        self.database = self.mongodb_client[dbname]
        self.CRON_SCRIPT_PATH = os.getenv("CRON_SCRIPT_PATH")

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
    
    def get_manualFeedingAmount(self, user_email):
        collection = self.get_collection("manualFeedings")

        return collection.find_one({"user": user_email})['manualFeedingAmount']
    
    def listen_for_changes(self, user_email, collection_name):
        # collections = ["schedules", "manualFeedings"]
        collection = self.get_collection(collection_name)

        pipeline = [
            {"$match": {
                "fullDocument.user": user_email, 
                "operationType": {"$in": ["update"]}  
            }}
        ]

        with collection.watch(pipeline=pipeline, full_document='updateLookup') as stream:
            for change in stream:
                operation_type = change["operationType"]
                if collection_name == "schedules":
                    if operation_type == "update":
                        set_cron_jobs(change["fullDocument"], self.CRON_SCRIPT_PATH)
                elif collection_name == "manualFeedings":
                    if operation_type == "update":
                        feedingAmount = change['fullDocument']['manualFeedingAmount']
                        if (change['fullDocument']['buttonToFeed']):
                            print("Do Smth with feedingAmount Here: ")
                            print(feedingAmount)
                        collection.update_one(
                            {"_id": change['fullDocument']["_id"]}, 
                            {"$set": {"buttonToFeed": False}}
                        )
                        