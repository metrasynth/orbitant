import logging
from collections import deque
from time import time

import mido


CLOCK = mido.Message('clock')


class BpmFinder(object):

    def __init__(self, min_ticks, max_ticks, tpb):
        self.min_ticks = min_ticks
        self.tpb = tpb
        self.queue = deque(maxlen=max_ticks)
        self.last_bpm = None

    @property
    def current_bpm(self):
        if len(self.queue) >= self.min_ticks:
            return (
                60. /
                ((self.queue[-1] - self.queue[0]) /
                 len(self.queue) * self.tpb)
            )

    def receive_message(self, message):
        if message.type == 'clock':
            self.queue.append(time())
            bpm = int(self.current_bpm or 0)
            if bpm and bpm != self.last_bpm:
                logging.debug('bpm=%r', bpm)
                self.last_bpm = bpm
