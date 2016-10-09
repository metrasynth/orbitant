import logging

import begin

from orbitant import backend, bpmfinder


@begin.start
@begin.logging
def main(min_samples: 'Timing samples to accumulate before calculating' = 16,
         max_samples: 'Maximum timing samples to use when calculating' = 128,
         name: 'MIDI port name' = 'Orbitant Generator'):
    logging.info('Starting monitor; press ^C to exit')
    with backend.open_input(name=name) as port:
        bpm_finder = bpmfinder.BpmFinder(
            port=port,
            min_samples=int(min_samples),
            max_samples=int(max_samples),
        )
        bpm_finder.run()
