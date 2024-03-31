from ..__space__ import *

class BinarySensorHassComponent(AHassComponent):
    def __init__(self, device: BinarySensorDevice) -> None:
        self.device = device