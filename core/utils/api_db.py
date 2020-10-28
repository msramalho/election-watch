# -*- coding: utf-8 -*-
import twitter, datetime, time, json, os, atexit
from .misc import *
from . import misc  # for globals like CONFIG
from .done_message import DoneMessage
# API SETUP METHODS

# globals
api = twitter.Api(consumer_key="", consumer_secret="", access_token_key="", access_token_secret="", tweet_mode="extended", sleep_on_rate_limit=False)
KEYS, BEST = [], {}


def add_time_to_key(key):
    key["last_used"] = datetime.datetime.utcfromtimestamp(0)
    return key


def read_api_keys():
    keys = json_to_dict(configs_abs_path(misc.CONFIG["api_keys"]))
    # keys = json_to_dict(os.path.dirname(os.path.realpath(__file__)) + "/" + misc.CONFIG["api_keys"])
    return [add_time_to_key(k) for k in keys]


def refresh_keys_from_file():
    global KEYS, BEST
    KEYS = read_api_keys()[:-1]
    load_next_api()


def is_usable_15min_rule(key):
    # return bool if is usable, seconds to wait
    seconds_diff = (datetime.datetime.utcnow() - key["last_used"]).total_seconds()
    return (seconds_diff / 60) >= 15, (15 * 60 - seconds_diff)


def load_next_keys(verbose=True):
    global BEST
    BEST["last_used"] = datetime.datetime.utcnow()
    new_best = min(KEYS, key=lambda x: x["last_used"])
    usable, wait_for = is_usable_15min_rule(new_best)
    if not usable:
        stop_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=wait_for)
        if verbose:
            print("Sleeping for %d seconds AKA %.2f minutes... ending at %s" % (wait_for, wait_for / 60, stop_at), end="")
        time.sleep(wait_for)
        if verbose: print("Done")
    BEST = new_best


def load_next_api(verbose=True):
    global api
    load_next_keys(verbose)
    print("Using API keys for app %s" % BEST["name"], flush=True)
    api.SetCredentials(BEST["consumer_key"], BEST["consumer_secret"], BEST["access_token_key"], BEST["access_token_secret"])


# API Helpers
def get_paged_results(func, user_id, count, verbose=True, max_pages=999_999):  # used for paged functions
    next_c = -1
    page = 0
    while next_c != 0:
        try: next_c, _, res = func(user_id=user_id, cursor=next_c, count=count)
        except twitter.TwitterError as e:  # rotate keys and try again
            res = None
            if verbose: print("X", end="", flush=True)
            if not handle_error_next_api(e, user_id, "get_paged_results:%s" % func.__name__): break
        if res:
            if verbose: print(".", end="", flush=True)
            yield res
            page += 1
            if page >= max_pages: break


# API INVOCATION METHODS
def get_users_from_usernames(usernames):
    res = []  # set redundancy for username updates
    for s in set(usernames):
        user = get_account_details(screen_name=s)
        if user: res.append(user)
        else: print("account details for %s not found" % s, flush=True)
    return res


def get_account_details(user_id=None, screen_name=None, re_raise=False):
    try:
        return api.GetUser(user_id=user_id, screen_name=screen_name)
    except twitter.TwitterError as e:
        handle_error_next_api(e, user_id or screen_name, "process_user:GetUser")
        if re_raise: raise e


def update_account_details_on_suspended(user):
    account = get_account_details(user_id=user["_id"])
    if account:  # user has been unsuspended
        user = user_to_db_format(account)
        user["suspended"] = False
        user["time_unsuspended"] = datetime.datetime.utcnow()
        upsert_user(user)
        return user
    return user


def get_tweets(user, func, since_id_key, oldest_tweet, args={}):
    # this method finds tweets between [OLDEST_TWEET, now] or [since_id, now] iff since_id
    # up to a maximum of 3200 as per the API spec, using func
    # since_id should be different according to the func (timeline, favourites, ...)
    # working with timelines:
    # https://developer.twitter.com/en/docs/tweets/timelines/guides/working-with-timelines

    since_id = user[since_id_key] if since_id_key in user else None
    tweets = []
    new_tweets = [None]
    while len(new_tweets):
        try:
            max_id = tweets[-1]["_id"] - 1 if len(tweets) else None
            new_tweets = [tweet_to_db_format(t) for t in func(user_id=user["_id"], count=200, max_id=max_id, since_id=since_id, **args)]
            tweets.extend(new_tweets)
            if len(new_tweets) and new_tweets[-1]["created_at"] < oldest_tweet: break
        except twitter.TwitterError as e:
            if not handle_error_next_api(e, user["_id"], "get_tweets:%s" % func.__name__, checkSuspension=True): break
    # update db with new value for since_id
    user[since_id_key] = since_id if not len(tweets) else tweets[0]["_id"]  # return new since_id
    upsert_user(user)
    # filter out older than requested tweets
    return list(filter(lambda t: t["created_at"] >= oldest_tweet, tweets))


def search_hashtag(hashtag, since, until, lang, count=100, verbose=True):
    max_search_attempts = 10
    for i in range(max_search_attempts):  # make 10 attempts
        try:
            return [tweet_to_db_format(t) for t in api.GetSearch("(#%s)" % hashtag, since=since, until=until, lang=lang, count=count)]
        except:
            if verbose:
                print("[retrying %d/%d]..." % (i + 1, max_search_attempts), end="", flush=True)
    # if verbose: print("[failed every attempt]")
    return []

# API+DB METHODS


# https://developer.twitter.com/en/docs/basics/response-codes
def handle_error_next_api(error, user_id, task="", verbose=True, checkSuspension=False):
    error_message = "Error for %s with error %s with API Keys from '%s' (%s)" % (user_id, error, BEST["name"], task)

    if verbose: print(error_message, flush=True)

    if not hasattr(error, 'message'):
        if verbose: print("Non-expected error: %s" % error, flush=True)
    elif error.message == "Not authorized.":
        # some endpoints return this instead of suspended, so force a call on account details to check if it is suspensions, or private
        if checkSuspension: get_account_details(user_id)
        else: update_not_allowed_user(user_id)
        return False  # False means skip
    elif type(error.message) == list and "code" in error.message[0]:
        code = int(error.message[0]["code"])  # 88 = rate limit, 32 = authentication failed, 326 is blocked
        if code == 34 or code == 50:  # "Sorry, that page does not exist.", 50:"User not found"
            update_not_allowed_user(user_id, "notfound")
            return False
        elif code == 63:  # 'User has been suspended.'
            update_not_allowed_user(user_id, "suspended")
            return False
        elif code == 130: pass  # [{'message': 'Over capacity', 'code': 130}]
        # elif code == 88 or code == 32 or code == 326:
        elif code != 88:  # not rate limit
            # todo: notify on error
            code_info = misc.CONFIG["error_codes"][code]
            pushbullet_notify(error_message + "\n\nError code %d (%s):\n%s" % (code, code_info["text"], code_info["description"]) + "\n\nmore info on: https://developer.twitter.com/en/docs/basics/response-codes\n\n [consumer_secret:%s]" % api._consumer_key)
        if code == 326:
            pushbullet_notify("API account blocked, go to https://twitter.com to unlock")
        # by default load next api key
        load_next_api(verbose)
    return True


# DB METHODS
import pymongo
from pymongo import UpdateOne


# globals
mongo, db, col_tweets, col_users = None, None, None, None


# register a detection of interruption for scripts
@atexit.register
def gracefully_stop_db():
    global mongo
    if mongo:
        mongo.close()
        print("[closed mongo connection]")


def init_db():
    global mongo, db, col_tweets, col_users
    # read the mongodb address from config and override if env exists
    mongo_address = os.environ.get('MONGO_ADDRESS') or misc.CONFIG["mongodb"]["address"]
    mongo = pymongo.MongoClient(mongo_address)
    db = mongo[misc.CONFIG["mongodb"]["database"]]  # get mongodb database
    col_tweets = db.tweets  # get mongo collection for tweets
    col_users = db.users   # get mongo collection for users


def print_db_stats():
    from pprint import pprint
    stats = db.command("dbstats")
    print("Database stats: ")
    pprint(stats)
    print("DB size (B): %s" % stats["dataSize"])
    print("DB size (MB): %.2f" % (stats["dataSize"] / (1024 * 1024)))
    print("DB size (GB): %.2f" % (stats["dataSize"] / (1024 * 1024 * 1024)))


def get_db_mb():
    return db.command("dbstats")["dataSize"] / (1024 * 1024)


# Helpers
def object_id_format(o):
    o["_id"] = int(o["id_str"])
    try:
        del o["id"]
        del o["id_str"]
    except: pass  # if the properties do not exist
    return o


def object_common_format(o):
    o = object_id_format(o)
    o["created_at"] = created_datetime(o["created_at"])
    o["collected_at"] = datetime.datetime.utcnow()
    return o


def user_to_db_format(u):
    u = u.AsDict()
    u = object_common_format(u)
    if "status" in u: del u["status"]
    if "screen_name" not in u: u["screen_name"] = False
    return u


def tweet_common_format(t, sub_tweet=True):
    if sub_tweet: t = object_id_format(t)
    else: t = object_common_format(t)

    # remove empty fields
    for key in ["hashtags", "user_mentions", "urls"]:
        if key in t and len(t[key]) == 0: del t[key]

    # remove duplicate fields (and media if in config)
    keys_to_delete = ["in_reply_to_screen_name", "quoted_status_id"]
    if misc.CONFIG["collection"]["ignore_tweet_media"]: keys_to_delete.append("media")
    for key in keys_to_delete:
        if key in t: del t[key]

    # delete keys with ids repeated as str
    for key in list(t.keys())[::]:
        if "_id_str" in key: del t[key]

    # standard format with less repeated information
    t["user"] = t["user"]["id"]
    if "hashtags" in t: t["hashtags"] = [h["text"].lower() for h in t["hashtags"]]
    if "user_mentions" in t: t["user_mentions"] = [um["id"] for um in t["user_mentions"]]

    # recursively cleanup
    if "retweeted_status" in t: t["retweeted_status"] = tweet_common_format(t["retweeted_status"])
    if "quoted_status" in t: t["quoted_status"] = tweet_common_format(t["quoted_status"])
    # mark as original
    if not "retweeted_status" in t and not "in_reply_to_user_id" in t and not "quoted_status" in t:
        t["original"] = True
    return t


def tweet_to_db_format(t):  # convert a tweet Status object to a dict with "_id"
    t = t.AsDict()
    t = tweet_common_format(t, sub_tweet=False)
    return t


# DB interaction

def find_exclude_invalid(search_params={}, _except=["suspended"]):
    for v in misc.CONFIG["invalid_user_states"].values():
        search_params[v] = {"$exists": False}
    for v in _except: del search_params[v]
    return search_params


def insert_user_ids(user_ids, depth=0):
    if not len(user_ids): return
    col_users.bulk_write([UpdateOne({'_id': u}, {"$min": {"depth": depth}}, upsert=True) for u in user_ids], ordered=False)


def upsert_user_ids_appearances(user_ids):  # legacy
    if not len(user_ids): return
    col_users.bulk_write([UpdateOne({'_id': u}, {"$inc": {"appearances": 1}}, upsert=True) for u in user_ids], ordered=False)


def upsert_user_ids_inc_custom_depth(user_ids, custom_name, depth=0):
    # custom_name replaces appearances to allow for different counters like
    # the followers of politcal seed and news seed
    if not len(user_ids): return
    col_users.bulk_write([UpdateOne({'_id': u}, {"$inc": {custom_name: 1}, "$min": {"depth": depth}}, upsert=True) for u in user_ids], ordered=False)


def upsert_users(users):
    # insert/update users when they come from the api
    if not len(users): return
    col_users.bulk_write([UpdateOne({'_id': u['_id']}, {
        "$set": u,
        "$min": {"first_collected_at": u["collected_at"]}
    }, upsert=True) for u in users], ordered=False)


def upsert_user(user):
    # insert/update a user when they come from the api
    operations = {"$set": user, "$min": {}}
    if "collected_at" in user:
        operations["$min"]["first_collected_at"] = user["collected_at"]
        if "first_collected_at" in user: del user["first_collected_at"]
    if "depth" in user:
        operations["$min"]["depth"] = user["depth"]
        del user["depth"]
    if not len(operations["$min"]): del operations["$min"]  # if empty remove
    col_users.find_one_and_update({'_id': user['_id']}, operations, upsert=True)


def update_not_allowed_user(user_id, prop="private"):
    prop = misc.CONFIG["invalid_user_states"][prop]  # standardized
    col_users.find_one_and_update({'_id': user_id}, {'$set': {prop: True}, "$min": {"time_%s" % prop: datetime.datetime.utcnow()}})


def paged_followers(user_id):
    return get_paged_results(api.GetFollowerIDsPaged, user_id, 5000)


def paged_friends(user_id):
    return get_paged_results(api.GetFriendIDsPaged, user_id, 5000)


def insert_tweets(tweets):
    if not len(tweets): return
    # must have been processed with tweet_to_db_format beforehand
    # ordered=False means all docs will be inserted and duplicates ignored
    try: col_tweets.insert_many(tweets, ordered=False)
    except pymongo.errors.BulkWriteError: pass  # ignore duplicate insertion errors


def upsert_tweet_info(tweet):
    col_tweets.find_one_and_update({'_id': tweet["_id"]}, {'$set': tweet}, upsert=True)


def get_watched_users_ids():
    return [u["_id"] for u in col_users.find({"depth": {"$exists": True}, "unwatched": {"$exists": False}}, {})]


def get_suspended_users_ids():
    return [u["_id"] for u in col_users.find({"suspended": True, "depth": {"$exists": True}}, {})]
