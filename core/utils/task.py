from slugify import slugify
import uuid
from .misc import get_filter_by_day


class Task:
    # handles a collection task_name
    # each document is {_id: uuid, day: day of analysis, data: what to store for this day}
    def __init__(self, db, name):
        self.name = slugify(name, separator="_")
        self.collection = db["task_%s" % self.name]
        # self.collection.create_index("day") # create index on day

    def exists_day(self, day):
        return self.collection.find_one({"day": get_filter_by_day(day)}) is not None

    def insert(self, day, data):
        return self.collection.insert({"_id": str(uuid.uuid4()), "day": day, "data": data})

    def get_last_n(self, n=30):
        assert n > 0, "n must be greater than 0"
        # retrieve last n entries concatenated
        # self.collection.find({})
        return list(self.collection.find({}).sort([("day", -1)]).limit(n))

    def unzip_last_n(self, n=30):
        # returns two lists [days], [datas]
        unzip = list(zip(*[(x["day"], x["data"]) for x in self.get_last_n(n)]))
        return unzip[0], unzip[1]

    def get_last(self): return self.get_last_n(1)[0]

    def drop(self): self.collection.remove({})
