from ..__space__ import *

class NewDeviceMessage(AMessage):
    
    def __init__(self, device: ADevice) -> None:
        self.device = device
        
    def __str__(self) -> str:
        return "NewDeviceMessage(" + str(self.device) + ")"