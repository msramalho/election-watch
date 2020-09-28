from slugify import slugify
import uuid
from .misc import get_filter_by_day


class Task:
    # handles a collection task_name
    # each document is {_id: uuid, day: day of analysis, data: what to store for this day}
    def __init__(self, db, name, create=True, only_one=False):
        self.name = "task_%s" % slugify(name, separator="_")
        self.db = db
        self.only_one = only_one
        if create or self.exists(): self.create()

    def create(self):
        self.collection = self.db[self.name]
        # self.collection.create_index("day") # create index on day

    def exists(self):
        return self.name in self.db.list_collection_names()

    def exists_day(self, day):
        return self.collection.find_one({"day": get_filter_by_day(day)}) is not None

    def insert(self, day, data):
        if self.only_one:
            return self.collection.find_one_and_update({}, {"$set": {"day": day, "data": data}}, upsert=True)
        else:
            return self.collection.find_one_and_update({"day": get_filter_by_day(day)}, {"$set": {"day": day, "data": data}}, upsert=True)

    def get_last_n(self, n=30, withId=True):
        assert n > 0, "n must be greater than 0"
        # retrieve last n entries concatenated
        # self.collection.find({})
        res = list(self.collection.find({}, {"_id": withId, "day": 1, "data": 1}).sort([("day", -1)]).limit(n))
        print(res)
        return res

    def unzip_last_n(self, n=30, withId=True):
        # returns two lists [days], [datas]
        unzip = list(zip(*[(x["day"], x["data"]) for x in self.get_last_n(n, withId)]))
        if len(unzip): return unzip[0], unzip[1]
        return [], []

    def get_last(self):
        last = self.get_last_n(1)
        if len(last): return [0]

    def drop(self): self.collection.remove({})
    def drop_day(self, day): self.collection.remove({"day": day})

    def get_api_n(self, n):
        # returns a standardized dict that can be returned directly by the api
        res = self.unzip_last_n(n, False)
        res = [[d.strftime("%Y-%m-%d") for d in res[0]], res[1]]
        # res = map(lambda r: {"day": r["day"].strftime("%Y-%m-%d"), "data": r["data"]}, self.unzip_last_n(n, False))
        return {"history": res}
