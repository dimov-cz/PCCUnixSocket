from ..__space__ import *

class ProjectorDevice(ADevice):
    
    sourcesList: List[str]
    colorModesList: List[str]
    
    def __init__(
            self, 
            id: str, 
            name: str, 
            model: str = "", 
            manufacturer: str = "",

            sourcesList = [ ],
            colorModesList = [ ],
    ) -> None:
        super().__init__(id, name, model, manufacturer)
        self.sourcesList = sourcesList
        self.colorModesList = colorModesList
        