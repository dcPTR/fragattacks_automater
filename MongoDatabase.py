import os

import pymongo as pymongo


class MongoDatabase:
    def __init__(self):
        self.client = pymongo.MongoClient(f"mongodb+srv://dev:{os.environ.get('famongopaswd')}@fragattacks.tvqp8ai.mongodb.net/?retryWrites"
                                          "=true&w=majority")
        self.db = self.client["fragattacks"]
        self.collection = self.db["test_results"]

    def clear_collection(self):
        self.collection.delete_many({})

    def insert_data(self, data):
        print(data)
        self.collection.insert_one(data)

    def find_device_by_name(self, device_name):
        return self.collection.find({"device.name": device_name})

    def get_all_data(self):
        return self.collection.find()

    def close_connection(self):
        self.client.close()
