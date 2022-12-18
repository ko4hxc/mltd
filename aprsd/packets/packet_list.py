import logging
import threading

import wrapt

from aprsd import utils
from aprsd.packets import seen_list


LOG = logging.getLogger("APRSD")


class PacketList:
    """Class to track all of the packets rx'd and tx'd by aprsd."""

    _instance = None
    lock = threading.Lock()
    config = None

    packet_list: utils.RingBuffer = utils.RingBuffer(1000)

    total_recv: int = 0
    total_tx: int = 0

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            if "config" in kwargs:
                cls._instance.config = kwargs["config"]
        return cls._instance

    def __init__(self, config=None):
        if config:
            self.config = config

    def _is_initialized(self):
        return self.config is not None

    @wrapt.synchronized(lock)
    def __iter__(self):
        return iter(self.packet_list)

    @wrapt.synchronized(lock)
    def rx(self, packet):
        """Add a packet that was received."""
        self.total_recv += 1
        self.packet_list.append(packet)
        seen_list.SeenList().update_seen(packet)

    @wrapt.synchronized(lock)
    def tx(self, packet):
        """Add a packet that was received."""
        self.total_tx += 1
        self.packet_list.append(packet)
        seen_list.SeenList().update_seen(packet)

    @wrapt.synchronized(lock)
    def get(self):
        return self.packet_list.get()

    @wrapt.synchronized(lock)
    def total_received(self):
        return self.total_recv

    @wrapt.synchronized(lock)
    def total_sent(self):
        return self.total_tx
