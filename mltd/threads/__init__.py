import queue

# Make these available to anyone importing
# mltd.threads
from .mltd import MLTDThread, MLTDThreadList  # noqa: F401


packet_queue = queue.Queue(maxsize=20)
