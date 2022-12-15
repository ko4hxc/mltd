import abc
import logging
from queue import Queue
import threading

import wrapt


LOG = logging.getLogger("APRSD")


class APRSDThreadList:
    """Singleton class that keeps track of application wide threads."""

    _instance = None

    threads_list = []
    lock = threading.Lock()
    global_queue = Queue()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.threads_list = []
        return cls._instance

    @wrapt.synchronized(lock)
    def add(self, thread_obj):
        thread_obj.set_global_queue(self.global_queue)
        self.threads_list.append(thread_obj)

    @wrapt.synchronized(lock)
    def remove(self, thread_obj):
        self.threads_list.remove(thread_obj)

    @wrapt.synchronized(lock)
    def stop_all(self):
        self.global_queue.put_nowait({"quit": True})
        """Iterate over all threads and call stop on them."""
        for th in self.threads_list:
            LOG.info(f"Stopping Thread {th.name}")
            th.stop()

    @wrapt.synchronized(lock)
    def __len__(self):
        return len(self.threads_list)


class APRSDThread(threading.Thread, metaclass=abc.ABCMeta):

    global_queue = None

    def __init__(self, name):
        super().__init__(name=name)
        self.thread_stop = False
        APRSDThreadList().add(self)

    def set_global_queue(self, global_queue):
        self.global_queue = global_queue

    def _should_quit(self):
        """ see if we have a quit message from the global queue."""
        if self.thread_stop:
            return True
        if self.global_queue.empty():
            return False
        msg = self.global_queue.get(timeout=1)
        if not msg:
            return False
        if "quit" in msg and msg["quit"] is True:
            # put the message back on the queue for others
            self.global_queue.put_nowait(msg)
            self.thread_stop = True
            return True

    def stop(self):
        self.thread_stop = True

    @abc.abstractmethod
    def loop(self):
        pass

    def _cleanup(self):
        """Add code to subclass to do any cleanup"""

    def run(self):
        LOG.debug("Starting")
        while not self._should_quit():
            can_loop = self.loop()
            if not can_loop:
                self.stop()
        self._cleanup()
        APRSDThreadList().remove(self)
        LOG.debug("Exiting")