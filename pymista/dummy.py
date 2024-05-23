"""
Class controlling dummy stage
"""
from .universal import *

class DummyStage(UniversalStage):
    def __init__(self):
        super(DummyStage, self).__init__()
        self.stagetype = "dummy"