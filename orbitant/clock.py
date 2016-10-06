import logging
from collections import deque
from time import sleep, time

import mido


CLOCK = mido.Message('clock')


class Generator(object):

    def __init__(self, port, bpm, tpb):
        self.port = port
        self.bpm = bpm
        self.tpb = tpb
        self.ticks = 0

    def start(self):
        initial_time = time()
        tick_time = 60. / self.bpm / self.tpb
        wait_time = tick_time / 1.5
        sleep_time = wait_time / 2.
        while True:
            next_time = initial_time + (tick_time * self.ticks)
            while time() + wait_time < next_time:
                sleep(sleep_time)
            while time() < next_time:
                pass
            self.tick()
            self.ticks += 1

    @property
    def beat(self):
        return self.ticks // self.tpb

    @property
    def beat_tick(self):
        return self.ticks % self.tpb

    def tick(self):
        self.port.send(CLOCK)
        logging.debug('beat=%i tick=%i', self.beat, self.beat_tick)


class Monitor(object):

    def __init__(self, min_ticks, max_ticks, tpb):
        self.min_ticks = min_ticks
        self.tpb = tpb
        self.queue = deque(maxlen=max_ticks)
        self.last_bpm = None

    @property
    def current_bpm(self):
        if len(self.queue) >= self.min_ticks:
            return 60. / ((self.queue[-1] - self.queue[0]) / len(self.queue) * self.tpb)

    def receive_message(self, message):
        self.queue.append(time())
        bpm = int(self.current_bpm or 0)
        if bpm and bpm != self.last_bpm:
            logging.debug('bpm=%r', bpm)
            self.last_bpm = bpm
