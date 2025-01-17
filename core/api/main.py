import sys, os, glob, time, re, json
sys.path = ['.', '..', '../..'] + sys.path

from flask import Flask, request, send_file
# from flask_pymongo import PyMongo
from flask_cors import CORS
from collections import defaultdict
from loguru import logger
from collections import OrderedDict  # for json.load to keep order
from gevent.pywsgi import WSGIServer

from utils.misc import json_to_dict, configs_abs_path, abs_path
from utils.task import Task
from utils.db_connect import DBConnect

# disable stdout/sterr
f = open(os.devnull, 'w')
sys.stdout = f
sys.stderr = f

app = Flask(__name__)
CORS(app)

config = json_to_dict(configs_abs_path('config.json'))

MONGO_URI = os.environ.get('MONGO_ADDRESS') or config["mongodb"]["address"]
DATABASE = config["mongodb"]["database"]
# app.config["MONGO_URI"] = config["mongodb"]["address"] + "admin"
# mongo = PyMongo(app)
# db = mongo.cx.get_database(config["mongodb"]["database"])
# col_users = db.get_collection("users")
# col_tweets = db.get_collection("tweets")


@app.route("/")
def hello():
    return {"alive": True}


def read_json(filename):
    with open(filename, encoding="utf-8") as f:
        return json.loads(f.read(), object_pairs_hook=OrderedDict)


@app.route("/stats")
def stats():
    try:
        return read_json(abs_path("..") + os.sep + config["database_stats_file_api"])
    except: return dict()


@app.route("/db_logs")
def db_logs():
    return read_json(abs_path("..") + os.sep + config["database_logs_file_api"])


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
    except: return "Index is not a valid number", 403

    _logs = logs()
    if task not in _logs:
        return ("Task %s not found" % task), 404
    if index >= len(_logs[task]["logs"]):
        return ("Index %s not found for task %s" % (index, task)), 404
    return {"content": read_task_log_file(task, _logs[task]["logs"][index])}


@app.route("/task_data")
def task_data():
    # this will query the DB dynamically in the task_name collection
    task_name = request.args.get('task_name')
    try: assert type(task_name) == str and len(task_name) > 0
    except: return "task_name is invalid", 403

    with DBConnect(MONGO_URI, DATABASE) as db:
        task = Task(db, task_name, False)
        try: assert task.exists()
        except: return "task_name not found", 404
        return task.get_api_n(365)  # return data for the last 365 days


def read_and_return_file(FILENAME):
    try:
        return send_file(FILENAME, mimetype='text/plain')
    except: return "internal error", 500


@app.route("/embeddings_tensors")
def embeddings_tensors():
    TENSOR = abs_path("../embeddings/tweet_relations_mentions_tf_out_tensor.tsv")
    return read_and_return_file(TENSOR)


@app.route("/embeddings_metadata")
def embeddings_metadata():
    METADATA = abs_path("../embeddings/tweet_relations_mentions_tf_out_metadata_handles.tsv")
    return read_and_return_file(METADATA)


@app.after_request
def add_header(response):
    response.cache_control.max_age = 0  # 54000=15min
    response.cache_control.public = True
    logger.info(request.full_path)
    return response


if __name__ == '__main__':
    logger.remove()
    logger.add("logs_flask.txt", format="{time:X}|{message}", level="INFO")
    # Debug/Development
    # app.run(debug=True, host='0.0.0.0')
    # Production
    http_server = WSGIServer(('', 5000), app, log=None, error_log=None)
    http_server.serve_forever()
