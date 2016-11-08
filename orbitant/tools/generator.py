import logging

import begin

from orbitant import backend, generator


@begin.start
@begin.logging
def main(bpm: 'Beats per Minute' = 120,
         tpb: 'Ticks per Beat' = 24,
         name: 'MIDI port name' = 'Orbitant Generator',
         ):
    bpm = int(bpm)
    tpb = int(tpb)
    port = backend.open_output(name=name, virtual=True)
    gen = generator.Generator(port=port, bpm=bpm, tpb=tpb)
    logging.info('Starting clock; press ^C to exit')
    gen.start()
