from math import ceil
from datetime import datetime
from multiprocessing.pool import ThreadPool
from time import time
import shutil, inspect, os, glob, threading

from .misc import abs_path, readable_seconds


class DynamicParallelism:
    def __init__(self, query_count, task_fn, name, batch_size=100_000, max_threads=16, cleanup=False, verbose=True):
        self.query_count = query_count
        self.task_fn = task_fn  # must do all imports and cannot use global variables except those in the header (see below)
        self.batch_size = batch_size
        self.cleanup = cleanup
        self.verbose = verbose
        self.max_threads = max_threads
        self.folder = abs_path("../out/parallel/") + name

    def _calculate_batches(self):
        bs = self.batch_size  # shorten
        self.batches = ceil(self.query_count / bs)
        # create array of (skip, limit) to cover all query_count
        self.query_limits = [(i, i * bs, bs) for i in range(self.batches)]  # skip, limit
        if self.verbose: print("BATCHES: %s" % self.query_limits, flush=True)

    def _reset_out_folder(self):
        self.clean()
        if not os.path.isdir(self.folder): os.makedirs(self.folder)
        return self

    def _invoke_code(self, args):
        start = time()
        index, skip, limit = args
        # header disables print
        disable_print = "sys.stdout = open(os.devnull, 'w')\n"
        header = "import sys, os\n" + disable_print + "import sys\nsys.path = ['.', '..', '../..'] + sys.path\nfrom collection import *\n" + "sys.stdout = sys.__stdout__\n"
        filename = self.folder + "/task_%d.py" % (index)
        with open(filename, "w") as ftask:
            ftask.write(header)
            ftask.write(inspect.getsource(self.task_fn))
            ftask.write("%s(%d, %d)\n" % (self.task_fn.__name__, skip, limit))
            ftask.write(disable_print)
        exit_code = os.system("python %s > %s.txt" % (filename, filename))
        os.remove(filename)  # delete the code file
        if self.verbose: print("[%s] Task %3d [skip=%8d, limit=%8d, duration=%s, exit_code: %2s]" % (datetime.now(), *args, readable_seconds(time() - start), exit_code), flush=True)
        return exit_code, filename

    def _execute_parallel(self):
        p = ThreadPool(self.max_threads)
        p.map(self._invoke_code, self.query_limits)

    def clean(self):
        if os.path.isdir(self.folder): shutil.rmtree(self.folder)
        return self

    def reduce(self, out_file=None):
        out_file = out_file or self.folder + "_reduced.txt"
        task_files = glob.glob(self.folder + "/*.txt")
        with open(out_file, "w", encoding="utf-8") as _out:
            for f in task_files:
                if self.verbose: print("Processing file %s." % f)
                with open(f, "r", encoding="utf-8") as _in:
                    for l in _in: _out.write(l)
        return out_file

    def run(self):
        if self.verbose:
            start = time()
            print("Starting execution at %s batch_size=%d, max_threads=%d, cleanup=%s" % (datetime.now(), self.batch_size, self.max_threads, self.cleanup), flush=True)
        self._calculate_batches()
        self._reset_out_folder()
        self._execute_parallel()
        if self.cleanup:
            if self.verbose: print("Removing folder %s" % self.folder, flush=True)
            self.clean()
        if self.verbose: print("Finished at %s (%s)" % (datetime.now(), readable_seconds(time() - start)), flush=True)
        return self

    def run_async(self):
        t = threading.Thread(target=self.run, daemon=True)
        t.start()
        return t
