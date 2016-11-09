__version__ = '0.1.1'

try:
    import mido
except ImportError:
    backend = None
else:
    backend = mido.Backend('mido.backends.rtmidi')
