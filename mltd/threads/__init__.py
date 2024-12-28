import queue

# Make these available to anyone importing
# aprsd.threads
from .mltd import MLTDThread, MLTDThreadList  # noqa: F401
from .rx import (  # noqa: F401
    MLTDDupeRXThread, MLTDProcessPacketThread, MLTDRXThread,
)


packet_queue = queue.Queue(maxsize=20)
