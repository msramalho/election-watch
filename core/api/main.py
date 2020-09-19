import sys, os, glob, time, re
sys.path = ['.', '..', '../..'] + sys.path

from flask import Flask, request
from flask_pymongo import PyMongo
from flask_cors import CORS
from collections import defaultdict

from utils.misc import json_to_dict, configs_abs_path, abs_path


app = Flask(__name__)
CORS(app)

config = json_to_dict(configs_abs_path('config.json'))

app.config["MONGO_URI"] = config["mongodb"]["address"] + "admin"


mongo = PyMongo(app)
db = mongo.cx.get_database(config["mongodb"]["database"])
col_users = db.get_collection("users")
col_tweets = db.get_collection("tweets")


@app.route("/")
def hello():
    return {"alive": True}


@app.route("/stats")
def stats():
    try:
        return {
            "users": {
                "total": col_users.count({}),
                # "depth_0": col_users.count({"depth": 0}),
                # "depth_1": col_users.count({"depth": 1}),
                # "depth_2": col_users.count({"depth": 2}),
                # "screen_name": col_users.count({"screen_name": {"$exists": True}})
            },
            "tweets": {
                "total": col_tweets.count({}),
                # "processed": col_tweets.count({"processed": True})
            },
            "mb": db.command("dbstats")["dataSize"] / (1024 * 1024)
        }
    except Exception as e:
        print("/stats failed with %s" % e)
        return {"users": {"error": "db not connected"}, "tweets": {"error": "db not connected"}, "mb": 0}


@app.route("/db_logs")
def db_logs():
    max_items = request.args.get('max_items') or 50_000
    max_items = int(max_items)
    db_logs = abs_path(".." + os.sep + "out") + os.sep + "db_logs.csv"
    res = {"time": [], "users": [], "tweets": [], "mb": []}
    with open(db_logs, encoding="utf-8") as f:
        total_points = len(f.readlines())
        max_items = min(max_items, total_points)
    with open(db_logs, encoding="utf-8") as f:
        steps = total_points // max_items
        i = 0
        for l in f:
            if i == steps:
                t, u, tw, m = l.strip().split(",")
                res["time"].append(t)
                res["users"].append(u)
                res["tweets"].append(tw)
                res["mb"].append(m)
                i = 0
            i += 1
    return res


def get_out_folder():
    return abs_path(".." + os.sep + "out" + os.sep + "collection")


def get_all_output_files():
    # return all python script files in given path
    out_folder = get_out_folder()
    return [f.split(os.sep) for f in glob.glob("%s/*/*/*.txt" % out_folder)]


def get_running_scripts():
    # communicates with launcher process to obtain currently running scripts
    # TODO: if multiple instances of launcher.py exist then this needs to be adjusted
    running_json = abs_path(".." + os.sep + "out" + os.sep + "running.json")
    report_file = abs_path(".." + os.sep + "report")
    # delete previous running.json
    if os.path.exists(running_json): os.remove(running_json)
    # create report file
    open(report_file, 'w').close()
    # wait for launcher to produce running.json
    i = 0
    while not os.path.exists(running_json) and i < 10:  # wait a max of 5 seconds
        time.sleep(0.5)
        i += 1
    if not os.path.exists(running_json): return {}
    # return json_to_dict(running_json)
    # TODO: this is a temporary fix while real server is not reloaded
    return {re.sub(r"(\d+_\d+_)", "", k): v for k, v in json_to_dict(running_json).items()}


@app.route("/logs")
def logs():
    res = defaultdict(list)
    running_scripts = get_running_scripts()
    print("Currently running %s" % running_scripts)
    for p in get_all_output_files():
        res[p[-3] + "/" + p[-2]].append(p[-1])
    new_res = {}
    for k, v in res.items():
        new_res[k] = {"logs": sorted(v, reverse=True)}
        if k + ".py" in running_scripts:
            new_res[k]["elapsed"] = running_scripts[k + ".py"]
    return new_res


def read_task_log_file(task, filename):
    log_path = get_out_folder() + os.sep + task + os.sep + filename
    with open(log_path, "r", encoding="utf-8") as f:
        return f.read()


@app.route("/log")
def log():
    task = request.args.get('task')
    try: index = int(request.args.get('index'))
    except: return "Index is not a valid number", 404

    _logs = logs()
    if task not in _logs:
        return ("Task %s not found" % task), 404
    if index >= len(_logs[task]["logs"]):
        return ("Index %s not found for task %s" % (index, task)), 404
    return {"content": read_task_log_file(task, _logs[task]["logs"][index])}


if __name__ == '__main__':
    app.run(host='0.0.0.0')
