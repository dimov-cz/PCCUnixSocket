from ..__space__ import *

class SensorHassComponent(AHassComponent):
    def __init__(self, device: SensorDevice) -> None:
        self.device = device