import pymongo


class DBConnect:
    def __init__(self, mongo_address, database_name):
        self.mongo_address = mongo_address
        self.database_name = database_name

    def __enter__(self):
        self.mongo = mongo = pymongo.MongoClient(self.mongo_address)
        self.db = mongo[self.database_name]
        return self.db

    def __exit__(self, _type, _value, _traceback):
        if self.mongo: self.mongo.close()
