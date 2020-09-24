# -*- coding: utf-8 -*-
import datetime, json, os, operator, atexit
from pushbullet import Pushbullet

import functools
# force print flush
print = functools.partial(print, flush=True)

CONIFG = {}
CONFIGS_FOLDER = "../configs"


def abs_path(filename):
    return ("%s" + os.sep + "%s") % (os.path.dirname(os.path.realpath(__file__)), filename)


def configs_abs_path(filename):
    return ("%s" + os.sep + "%s" + os.sep + "%s") % (os.path.dirname(os.path.realpath(__file__)), CONFIGS_FOLDER, filename)


def created_datetime(created_at):
    # example: "Fri Sep 27 10:19:25 +0000 2019"
    return datetime.datetime.strptime(created_at, '%a %b %d %H:%M:%S %z %Y')


def next_or_none(cursor):
    """Tries to get the next(cursor) element but catches errors and returns none upon failure"""
    try: return next(cursor)
    except: return None


def dict_key_or_default(d, key, default=None):
    """Avoid if key in d d[key] else None """
    if key in d: return d[key]
    return default


def dict_key_for_max_val(d):
    """returns the key in the dict that has the max value"""
    return max(d.items(), key=operator.itemgetter(1))[0]


def json_to_dict(filename):
    with open(filename, "r", encoding="utf-8") as f: d = json.load(f)
    return d


def dict_to_json(_dict, filename):
    with open(filename, "w", encoding="utf-8") as f: json.dump(_dict, f)


def import_configs():
    config = json_to_dict(configs_abs_path('config.json'))
    config["invalid_user_states"] = {"private": "private", "notfound": "notfound", "suspended": "suspended", "unwatched": "unwatched"}
    col = config["collection"]
    col["oldest_tweet"] = created_datetime(col["oldest_tweet"])
    # col["newest_tweet"] = created_datetime(col["newest_tweet"])
    config["error_codes"] = {int(k): v for k, v in json_to_dict(abs_path('error_codes.json')).items()}
    return config


def get_original_configs():
    return json_to_dict(configs_abs_path('config.json'))


def overwrite_configs(new_configs):
    with open(configs_abs_path('config.json'), "w", encoding="utf-8") as out:
        json.dump(new_configs, out, ensure_ascii=False)
        # json.dump(new_configs, out, default=str, indent=4, sort_keys=False, ensure_ascii=False)


def load_config():
    global CONFIG
    CONFIG = import_configs()


def pushbullet_notify(message):
    if "pushbullet_token" not in CONFIG["notifications"]:
        print("Tried to send pushbullet message [%s] but no `notifications.pushbullet_token` was found" % message)
        return
    pb = Pushbullet(CONFIG["notifications"]["pushbullet_token"])
    now = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
    pb.push_note("Election Watch", "%s\n\n%s" % (now, message))
    print(message, flush=True)  # also prints to stdout


def get_day_pairs_between(_from, _to):
    # returns a list of [(_from, d1), (d1, d2), ... (di, _to)]
    assert _from < _to, ("_from (%s) must come before _to (%s)" % (_from, _to))
    days_between = (_to - _from).days
    return [
        (_from + datetime.timedelta(days=i), _from + datetime.timedelta(days=i + 1)) for i in range(days_between)
    ]


def readable_seconds(seconds, _format="%2dd %2dh %2dm %2ds"):
    seconds = int(seconds)
    days = seconds // 86400
    hours = (seconds - 86400 * days) // 3600
    mins = (seconds - 86400 * days - 3600 * hours) // 60
    secs = (seconds - 86400 * days - 3600 * hours - 60 * mins)
    return _format % (days, hours, mins, secs)


def get_filter_by_day(day):
    # expects datetime
    day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
    day_end = day.replace(hour=23, minute=59, second=59, microsecond=0)
    return {"$gte": day_start, "$lt": day_end}


# register a detection of interruption for scripts
@atexit.register
def gracefully_stop():
    print('[!This process stopped at (%s)!]' % datetime.datetime.now())
    exit()
