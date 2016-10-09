import mido


CLOCK = mido.Message('clock')


TICKS_32ND = 96 // 32
TICKS_SEXTUPLET = 96 // 24
TICKS_16TH = 96 // 16
TICKS_TRIPLET = 96 // 12
TICKS_8TH = 96 // 8
TICKS_QUARTER = 96 // 4
TICKS_HALF = 96 // 2
TICKS_WHOLE = 96 // 1


def beat_properties(ticks):
    @property
    def beat(self):
        return self.tick // ticks
    @property
    def beat_tick(self):
        return self.tick % ticks
    return beat, beat_tick


class TransportSlave(object):
    """Listens and reacts to MIDI beat clock and transport messages.

    Subclass this and override the handlers to implement desired functionality.

    Supports Tick, Song Position Pointer (0, 0), Start, Stop, and Continue.
    """

    def __init__(self, port):
        self.port = port
        self._started = False
        self._tick = 0

    @property
    def started(self):
        return self._started

    @property
    def tick(self):
        return self._tick

    midi_beat, midi_beat_tick = beat_properties(6)

    beat_32nd, beat_32nd_tick = beat_properties(TICKS_32ND)
    beat_sextuplet, beat_sextuplet_tick = beat_properties(TICKS_SEXTUPLET)
    beat_16th, beat_16th_tick = beat_properties(TICKS_16TH)
    beat_triplet, beat_triplet_tick = beat_properties(TICKS_TRIPLET)
    beat_8th, beat_8th_tick = beat_properties(TICKS_8TH)
    beat_quarter, beat_quarter_tick = beat_properties(TICKS_QUARTER)
    beat_half, beat_half_tick = beat_properties(TICKS_HALF)
    beat_whole, beat_whole_tick = beat_properties(TICKS_WHOLE)

    @property
    def midi_beat(self):
        return self.tick // 6

    @property
    def midi_beat_tick(self):
        return self.tick % 6

    def run(self):
        for message in self.port:
            if message.type == 'clock':
                self._increment_tick()
            elif message.type == 'start':
                self._started = True
                self.on_start()
            elif message.type == 'stop':
                self._started = False
                self.on_stop()
            elif message.type == 'continue':
                self._started = True
                self.on_continue()
            elif message.type == 'songpos' and message.pos == 0:
                self._tick = 0
                self.on_rewind()

    def _increment_tick(self):
        self.on_tick()
        t = self.tick
        if t % TICKS_32ND == 0:
            self.on_32nd()
        if t % TICKS_SEXTUPLET == 0:
            self.on_sextuplet()
        if t % TICKS_16TH == 0:
            self.on_16th()
        if t % TICKS_TRIPLET == 0:
            self.on_triplet()
        if t % TICKS_8TH == 0:
            self.on_8th()
        if t % TICKS_QUARTER == 0:
            self.on_quarter()
        if t % TICKS_HALF == 0:
            self.on_half()
        if t % TICKS_WHOLE == 0:
            self.on_whole()
        self._tick += 1

    # Override these in subclasses:
    def on_start(self): pass
    def on_stop(self): pass
    def on_continue(self): pass
    def on_rewind(self): pass
    def on_tick(self): pass
    def on_midi_beat(self): pass
    def on_32nd(self): pass
    def on_sextuplet(self): pass
    def on_16th(self): pass
    def on_triplet(self): pass
    def on_8th(self): pass
    def on_quarter(self): pass
    def on_half(self): pass
    def on_whole(self): pass
