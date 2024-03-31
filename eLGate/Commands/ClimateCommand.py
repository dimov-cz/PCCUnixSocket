from ..__space__ import *

class ClimateCommand(ACommand):
    def __init__(self, 
            device: HvacDevice,
            mode: Optional[str] = None,
            temperature: Optional[float] = None,
            preset: Optional[str] = None,
    ) -> None:
        self.device = device
        self.mode = mode
        self.temperature = temperature
        self.preset = preset
        
    def __str__(self) -> str:
        return "ClimateCommand(" + str(self.device) + ", " + str(self.mode) + ", " + str(self.temperature) + ", " + str(self.preset) + ")"