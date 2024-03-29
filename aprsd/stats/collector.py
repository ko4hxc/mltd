from typing import Protocol

from aprsd.utils import singleton


class StatsProducer(Protocol):
    """The StatsProducer protocol is used to define the interface for collecting stats."""
    def stats(self) -> dict:
        ...


@singleton
class Collector:
    """The Collector class is used to collect stats from multiple StatsProducer instances."""
    def __init__(self):
        self.producers: dict[str, StatsProducer] = {}

    def collect(self):
        stats = {}
        for name, producer in self.producers.items():
            # No need to put in empty stats
            tmp_stats = producer.stats()
            if tmp_stats:
                stats[name] = tmp_stats
        return stats

    def register_producer(self, producer: StatsProducer):
        name = producer.__class__.__name__
        self.producers[name] = producer
