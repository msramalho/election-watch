import os, sys, re, time, glob, threading, functools, datetime, schedule, shutil
from pytictoc import TicToc
from pathlib import Path
from utils.done_message import DoneMessage
from utils.misc import abs_path, dict_to_json
from loguru import logger
import nltk
nltk.download('stopwords')

# GLOBALS
OUTPUT_DIR = "out/"
ABORT_FILE = "abort"  # if this file is detected, the infinite loop is aborted
REPORT_FILE = "report"  # if this file is detected, the output of RUNNING is sent to OUTPUT_DIR/running.json
SLEEP_BEFORE_RETRY = 10  # time to sleep before retrying execute_file
MAX_RETRY_ATTEMPTS = 100  # max execute_file attempts
RUNNING = {}  # record active scripts


def valid_script_file(name):
    if name[-3:] != ".py": return False
    if name[-11:] == "__init__.py": return False
    return True


def get_all_script_files(path):
    # return all python script files in given path
    return [f for f in glob.glob("%s/*.py" % path) if valid_script_file(f)]


def create_dir_if_not_exists(dirname):
    if not os.path.exists(dirname): os.makedirs(dirname)


def datetime_filename(filename):
    # remove the numbers from the filename, create a folder in the OUTPUT_DIR that matches it and then return a timestamped txt filename in that folder
    p = Path(filename)
    filename = os.path.splitext(filename)[0]
    folder = OUTPUT_DIR + str(p.parent) + "/" + re.sub(r"^(\d\d_\d\d|\d\d)_", "", p.stem)
    create_dir_if_not_exists(folder)
    return folder + "/%s.txt" % datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def exit_if_abort():
    # stop if ABORT_FILE exists
    if os.path.exists(ABORT_FILE):
        logger.info("Detected abort file, stoping.")
        os.remove(ABORT_FILE)
        exit(1)
    return True


def with_logging(func):
    # This decorator can be applied to log jobs execution
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        message = '%s(%s | %s)' % (func.__name__, args, kwargs)
        with TicToc():  # TODO: log all execution times into a single file for profiling: out/performance.csv
            logger.info('  ⬆ %s | LAUNCHED: %s.' % (datetime.datetime.now(), message))
            result = func(*args, **kwargs)
            logger.info('  ⬇ %s | COMPLETED: %s in' % (datetime.datetime.now(), message))
        return result
    return wrapper


@with_logging
def execute_filename(filename):
    # print("FILENAME: %s" % filename, datetime_filename(filename))
    # return
    # execute a script and log its results to the output dir
    cmd = "python %s > %s" % (filename, datetime_filename(filename))
    failed_attempts = 0
    while failed_attempts < MAX_RETRY_ATTEMPTS and exit_if_abort():
        exit_code = os.system(cmd)
        if exit_code != 0:
            logger.info("  ⚠️ Failed cmd [%s], retrying in %ds (%d/%d attempts)" % (cmd, SLEEP_BEFORE_RETRY, failed_attempts + 1, MAX_RETRY_ATTEMPTS))
            failed_attempts += 1
            time.sleep(SLEEP_BEFORE_RETRY)
        else:
            logger.info("  ✔️ Completed cmd [%s]" % cmd)
            break
    return failed_attempts


# run jobs as threads
# @with_logging
def run_threaded(job_func, *args, **kwargs):
    global RUNNING  # {filename: [thread, start_time]}
    f = kwargs["filename"]
    if f in RUNNING and RUNNING[f][0]:
        if RUNNING[f][0].is_alive():
            logger.info("Function %s still running, this scheduled task will be skipped." % f)
            return
    job_thread = threading.Thread(target=job_func, daemon=True, args=args, kwargs=kwargs)
    job_thread.start()
    RUNNING[f] = [job_thread, datetime.datetime.now()]
    return job_thread


def timedelta_str(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    if hours == 0 and minutes == 0: return "%ds" % seconds
    if hours == 0: return "%dm %ds" % (minutes, seconds)
    return "%dh %dm %ds" % (hours, minutes, seconds)


def output_running_tasks_json():
    if os.path.exists(REPORT_FILE):
        def clean_key(k): return os.sep.join(k.split(os.sep)[1:])  # removes "collection/" from path
        with DoneMessage("Detected report file, producing running tasks report"):
            report = {clean_key(k): [v[1].strftime("%b %d %Y %H:%M:%S"), timedelta_str(datetime.datetime.now() - v[1])] for k, v in RUNNING.items() if v[0].is_alive()}
            dict_to_json(report, OUTPUT_DIR + "/running.json")
            os.remove(REPORT_FILE)


def launch_setup(path):
    # things that must execute first
    setup = get_all_script_files("%s/setup" % path)
    logger.info("Launching all %d setup tasks..." % len(setup))
    # run initialization functions in parallel
    threads = []
    for script in setup:
        threads.append(run_threaded(execute_filename, filename=script))

    for t in threads:
        if t and t.is_alive(): t.join()
    logger.info("All setup threads ready.")


def launch_once(path):
    # things that must execute all the time
    once = get_all_script_files("%s/once" % path)
    logger.info("Launching all %d once tasks..." % len(once))
    for script in once:
        run_threaded(execute_filename, filename=script)
    logger.info("All once tasks launched.")


def apply_delta(hh, mm):
    # applies an hour:minute delta time to this moment and returns the new hour:min string
    now = datetime.datetime.now()
    if hh == 0 and mm == 0: mm += 2  # schedule for two minutes afterwards to give schedule enough time to start
    delta = datetime.timedelta(hours=hh, minutes=mm)
    return (now + delta).time().strftime("%H:%M")


def schedule_daily(path):
    # parse each scripts delta time and schedule their daily execution
    daily = get_all_script_files("%s/daily" % path)
    for script in daily:
        m = re.search(r"(\d\d)_(\d\d)[^\/]", script)
        if m:  # if this file starts with hh_mm
            h_delta, m_delta = map(int, [m.group(1), m.group(2)])
            daily_time = apply_delta(h_delta, m_delta)
            # execute daily starting now and with each script's daily delta
            with DoneMessage("⏱️ Scheduling %s every day at %s" % (script, daily_time)):
                schedule.every().day.at(daily_time).do(run_threaded, execute_filename, filename=script)


def schedule_hourly(path):
    # parse each scripts delta time and schedule their daily execution
    hourly = get_all_script_files("%s/hourly" % path)
    for script in hourly:
        m = re.search(r"(\d\d)[^\/]", script)
        if m:  # if this file starts with hh_mm
            m_delta = int(m.group(1))
            hourly_time = apply_delta(0, m_delta)[2:]
            # execute hourly starting now and with each script's hourly delta
            with DoneMessage("⏱️ Scheduling %s every hour at %s minutes" % (script, hourly_time)):
                schedule.every().hour.at(hourly_time).do(run_threaded, execute_filename, filename=script)


def launch_or_schedule(path):
    launch_setup(path)
    logger.info("-" * 20)
    launch_once(path)
    logger.info("-" * 20)
    schedule_daily(path)
    schedule_hourly(path)


def convert_jupyter_to_scripts(start_folder):
    # clean up all jupyter generated files and regenerate them
    with DoneMessage("Deleting previously generated scripts"):
        for f in Path(start_folder).glob('*/*.py'):
            with DoneMessage("   [Delete script] %s" % f):
                os.remove(f)
    os.system("jupyter nbconvert --to script ./*/*/*.ipynb")


def test(path, folders=["%s/daily", "%s/hourly"]):
    threads = []
    for f in folders:
        logger.info("TESTING %s" % f)
        scripts_to_test = get_all_script_files(f % path)
        for script in scripts_to_test:
            threads.append(run_threaded(execute_filename, filename=script))
    for t in threads: t.join()
    exit()


# ---------------------------------- LAUNCHER CODE
logger.add("logs.txt", format="{time} {message}", level="INFO")
# USAGE
assert len(sys.argv) == 2, ("Wrong usage, should be: python launcher.py <FOLDER_TO_LAUNCH> and not %s" % sys.argv)

start_folder = sys.argv[1]
assert os.path.exists(start_folder), ("Wrong argument, %s should be a valid folder" % start_folder)

# Convert Jupyter -> Scripts
convert_jupyter_to_scripts(start_folder)

# test(start_folder)
# test(start_folder, ["%s/hourly"])

# Schedule scripts
logger.info("Launching all scripts in %s." % start_folder)
launch_or_schedule(start_folder)

# start infinite loop of executing jobs
logger.info("-" * 40)
logger.info("Starting scheduled jobs.")
while exit_if_abort():
    schedule.run_pending()
    output_running_tasks_json()
    time.sleep(1)
