from time import time


class DoneMessage:
    """
    encapsulate a given piece of code with a start and done message, additionally with number of seconds of duration
    """

    def __init__(self, message, done_message="Done%s.", time=True):
        self.message = message + "..."
        self.done_message = done_message

    def __enter__(self):
        if time: self.start = time()
        print(self.message, end="", flush=True)

    def __exit__(self, _type, _value, _traceback):
        extra = ""
        if time: extra = " in %0.3fs" % (time() - self.start)
        print(self.done_message % extra, flush=True)
