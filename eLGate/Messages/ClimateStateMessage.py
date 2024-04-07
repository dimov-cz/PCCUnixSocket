from ..__space__ import *

class ClimateStateMessage(AMessage):
    presetId: Optional[str]
    
    def __init__(self, 
                 deviceId: str,
                 available: Optional[bool] = None,
                 availableSettings: Optional[bool] = None,

                 mode: Optional[HvacOperationModeEnum] = None,
                 presetId: Optional[str] = None,
                 currentTemperatureIn: Optional[float] = None, 
                 currentTemperatureOut: Optional[float] = None,
                 targetTemperature: Optional[float] = None,
                 ) -> None:
        self.deviceId = deviceId
        self.available = available
        self.availableSettings = availableSettings

        self.mode = mode
        self.presetId = presetId
        self.currentTemperatureIn = currentTemperatureIn
        self.currentTemperatureOut = currentTemperatureOut
        self.targetTemperature = targetTemperature

    def __str__(self) -> str:
        attrs = vars(self)
        attrs_str = ', '.join(f"{key}={value}" for key, value in attrs.items() if value is not None)
        return f"ClimateStateMessage({attrs_str})"