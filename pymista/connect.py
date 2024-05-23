from pymista import *

def connect_stage(stagetype : str, port = None) -> UniversalStage:
    if 'zaber' in stagetype:
        return ZaberStage(port)
    elif 'dummy' in stagetype:
        return DummyStage(port)
    else:
        raise ValueError(f"No valid stage found with name {stagetype}")
