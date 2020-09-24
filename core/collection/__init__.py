# -*- coding: utf-8 -*-
# import stuff from above

import sys
sys.path = ['..', '../..'] + sys.path

from utils.misc import *
from utils import misc  # for globals like CONFIG

from utils.api_db import *
from utils import api_db  # to access KEYS, BEST, ...

from utils.nlp import *
from utils.dynamic_parallelism import DynamicParallelism

# load configuration from JSON
load_config()

# print config
print("using %d seed accounts (%d from news sources) and %d hashtags" % (len(misc.CONFIG["seed"]["usernames"]), len(misc.CONFIG["seed"]["usernames_news"]), len(misc.CONFIG["seed"]["hashtags"])))

# initialize the database connection
init_db()
print_db_stats()

# get api keys
refresh_keys_from_file()

import datetime
print("\nDone initializing at %s." % datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))
print("-" * 40)
