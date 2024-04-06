from ..__space__ import *

class ProjectorCommand(ACommand):
    def __init__(self, 
            device: ProjectorDevice,
            power: Optional[str] = None,
            source: Optional[str] = None,
            colorMode: Optional[str] = None,
            
    ) -> None:
        self.device = device
        self.power = power
        self.source = source
        self.colorMode = colorMode

    def __str__(self) -> str:
        return f"ProjectorCommand({self.device}, {self.power}, {self.source}, {self.colorMode})"