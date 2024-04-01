from ...__space__ import *

class AManageController(AController):
    
    __commands: List[ACommand] = []
    
    def sendCommand(self, command:ACommand) -> None:
        self.__commands.append(command)
        
    def popCommand(self) -> Optional[ACommand]:
        if len(self.__commands) == 0:
            return None
        return self.__commands.pop(0)
    
    @abstractmethod
    def processNewDevice(self, message: NewDeviceMessage):
        pass

    @abstractmethod
    def stop(self):
        return super().stop()
    
    # optional
    def processClimateState(self, message: ClimateStateMessage):
        pass

    