import datetime
import logging
import time
import tracemalloc

from loguru import logger
from oslo_config import cfg

# from aprsd import packets, utils
# from aprsd.client import client_factory
# from aprsd.log import log as aprsd_log
# from aprsd.stats import collector
from mltd.threads import MLTDThread, MLTDThreadList


CONF = cfg.CONF
LOG = logging.getLogger("MLTD")
LOGU = logger


class KeepAliveThread(MLTDThread):
    cntr = 0
    checker_time = datetime.datetime.now()

    def __init__(self):
        tracemalloc.start()
        super().__init__("KeepAlive")
        max_timeout = {"hours": 0.0, "minutes": 2, "seconds": 0}
        self.max_delta = datetime.timedelta(**max_timeout)

    def loop(self):
        if self.loop_count % 60 == 0:
            thread_list = APRSDThreadList()
            now = datetime.datetime.now()
            LOG.info(keepalive)
            if "MLTDThreadList" in stats_json:
                thread_list = stats_json["MLTDDThreadList"]
                for thread_name in thread_list:
                    thread = thread_list[thread_name]
                    alive = thread["alive"]
                    age = thread["age"]
                    key = thread["name"]
                    if not alive:
                        LOG.error(f"Thread {thread}")

                    thread_hex = f"fg {utils.hex_from_name(key)}"
                    t_name = f"<{thread_hex}>{key:<15}</{thread_hex}>"
                    thread_msg = f"{t_name} Alive? {str(alive): <5} {str(age): <20}"
                    LOGU.opt(colors=True).info(thread_msg)
                    # LOG.info(f"{key: <15} Alive? {str(alive): <5} {str(age): <20}")

            # Check version every day
            delta = now - self.checker_time
            if delta > datetime.timedelta(hours=24):
                self.checker_time = now
                level, msg = utils._check_version()
                if level:
                    LOG.warning(msg)
            self.cntr += 1
        time.sleep(1)
        return True
