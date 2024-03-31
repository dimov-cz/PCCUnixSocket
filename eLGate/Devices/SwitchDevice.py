from ..__space__ import *

class SwitchDevice(ADevice):
    def __init__(self, id: str, name: str, model: str = "", manufacturer: str = "") -> None:
        super().__init__(id, name, model, manufacturer)