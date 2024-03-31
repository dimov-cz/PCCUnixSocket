from ..__space__ import *

class SwitchHassComponent(AHassComponent):
    def __init__(self, device: SwitchDevice) -> None:
        self.device = device