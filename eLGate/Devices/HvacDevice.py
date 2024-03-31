from ..__space__ import *

class HvacDevice(ADevice):
    
    modes: List[HvacOperationModeEnum]
    presetsIds: list
    
    def __init__(
            self, 
            id: str, 
            name: str, 
            model: str = "", 
            manufacturer: str = "",
            modes: List[HvacOperationModeEnum] = [ HvacOperationModeEnum.Off, HvacOperationModeEnum.Auto ],
            presetsIds = [ ]
    ) -> None:
        super().__init__(id, name, model, manufacturer)
        self.modes = modes
        self.presetsIds = presetsIds
        