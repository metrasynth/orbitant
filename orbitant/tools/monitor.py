import logging

import begin

from orbitant import backend, clock


@begin.start
@begin.logging
def main(min_ticks: 'Ticks to accumulate before calculating' = 24,
         max_ticks: 'Maximum ticks to use when calculating' = 512,
         tpb: 'Ticks per beat' = 24,
         name: 'MIDI port name' = 'Orbitant Generator'):
    logging.info('Starting monitor; press ^C to exit')
    monitor = clock.Monitor(min_ticks=min_ticks, max_ticks=max_ticks, tpb=tpb)
    with backend.open_input(name=name) as port:
        for message in port:
            monitor.receive_message(message)
