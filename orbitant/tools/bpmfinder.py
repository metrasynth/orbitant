import logging

import begin

from orbitant import backend, bpmfinder


@begin.start
@begin.logging
def main(min_ticks: 'Ticks to accumulate before calculating' = 24,
         max_ticks: 'Maximum ticks to use when calculating' = 512,
         tpb: 'Ticks per beat' = 24,
         name: 'MIDI port name' = 'Orbitant Generator'):
    logging.info('Starting monitor; press ^C to exit')
    bpm_finder = bpmfinder.BpmFinder(
        min_ticks=int(min_ticks),
        max_ticks=int(max_ticks),
        tpb=int(tpb),
    )
    with backend.open_input(name=name) as port:
        for message in port:
            bpm_finder.receive_message(message)
