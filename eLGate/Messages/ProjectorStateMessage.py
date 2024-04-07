from ..__space__ import *

class ProjectorStateMessage(AMessage):
    
    def __init__(self, 
                 deviceId: str,
                 available: Optional[bool] = None,
                 availableSettings: Optional[bool] = None,

                 power: Optional[bool] = None,
                 ready: Optional[bool] = None,

                 source: Optional[str] = None,
                 sourceList: Optional[List[str]] = None,
                 colorMode: Optional[str] = None,

                 mute: Optional[bool] = None,
                 volume: Optional[int] = None,
    ) -> None:
        self.deviceId = deviceId
        self.available = available
        self.availableSettings = availableSettings

        self.power = power
        self.ready = ready

        self.source = source
        self.sourceList = sourceList
        self.colorMode = colorMode

        self.mute = mute
        self.volume = volume
        
        self.available = available

    def __str__(self) -> str:
        attrs = vars(self)
        attrs_str = ', '.join(f"{key}={value}" for key, value in attrs.items() if value is not None)
        return f"ProjectorStateMessage({attrs_str})"
