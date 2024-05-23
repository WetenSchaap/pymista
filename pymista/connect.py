from . import *

def connect_stage(stagetype, port = None):
    if 'zaber' in stagetype:
        return ZaberStage(port)
    elif 'dummy' in stagetype:
        return DummyStage(port)
    else:
        raise ValueError(f"No valid stage found with name {stagetype}")
