from ...__space__ import *

class ADeviceController(AController):
    
    __messages: List[AMessage] = []
    
    def sendMessage(self, message: AMessage) -> None:
        self.__messages.append(message)
        
    def popMessage(self) -> Optional[AMessage]:
        if len(self.__messages) == 0:
            return None
        return self.__messages.pop(0)
    
    # @optional
    def processClimateCommand(self, command: ClimateCommand):
        pass

    # @optional
    def processProjectorCommand(self, command: ProjectorCommand):
        pass