from ..__space__ import *

class ClimateStateMessage(AMessage):
    presetId: Optional[str]
    
    def __init__(self, 
                 deviceId: str,
                 mode: Optional[HvacOperationModeEnum],
                 presetId: Optional[str],
                 currentTemperatureIn: Optional[float], 
                 currentTemperatureOut: Optional[float],
                 targetTemperature: Optional[float],
                 available: Optional[bool] = None,
                 ) -> None:
        self.deviceId = deviceId
        self.mode = mode
        self.presetId = presetId
        self.currentTemperatureIn = currentTemperatureIn
        self.currentTemperatureOut = currentTemperatureOut
        self.targetTemperature = targetTemperature
        self.available = available

    def __str__(self) -> str:
        return "ClimateStateMessage(" + str(self.deviceId) + ", " + str(self.mode) + ", " + str(self.currentTemperatureIn) + ", " + str(self.currentTemperatureOut) + ", " + str(self.targetTemperature) + ")"