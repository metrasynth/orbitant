import logging
from collections import deque
from time import time

from orbitant.transport import TransportSlave


class BpmFinder(TransportSlave):

    def __init__(self, port, min_samples, max_samples):
        super(BpmFinder, self).__init__(port)
        self.min_samples = min_samples
        self.queue = deque(maxlen=max_samples)
        self.last_bpm = None

    @property
    def current_bpm(self):
        if len(self.queue) >= self.min_samples:
            return (
                60.
                /
                (
                    (self.queue[-1] - self.queue[0]) /
                    len(self.queue) *
                    4
                )
            )

    def on_16th(self):
        self.queue.append(time())
        bpm = int(self.current_bpm or 0)
        if bpm and bpm != self.last_bpm:
            logging.info('bpm=%r', bpm)
            self.last_bpm = bpm
