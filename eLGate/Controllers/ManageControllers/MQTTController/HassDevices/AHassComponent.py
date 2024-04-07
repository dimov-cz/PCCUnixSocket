from ..__space__ import *

class AHassComponent(ALoggable, ABC):
    device: ADevice
    parentHassDevice: HassDevice
    componentUniqueId: str
    componentName: str
    
    """
    	"binary_sensor",
		"button",
		"climate",
		"cover",
		"device_automation",
		"light",
		"lock",
		"number",
		"select",
		"sensor",
		"switch"
    """
    @abstractproperty
    @property
    def componentTypeName(self) -> str:
        raise NotImplementedError()
    
    def __init__(
        self, 
        device: ADevice,
        parentHassDevice: HassDevice,        
        componentUniqueId: Optional[str] = None,
        componentName: Optional[str] = None,
    ) -> None:
        ALoggable.__init__(self)
        self.device = device
        self.parentHassDevice = parentHassDevice
        self.componentUniqueId = componentUniqueId if componentUniqueId is not None else self.device.getShortId()
        self.componentName = componentName if componentName  is not None else self.device.name
        
    def getUniqueId(self) -> str:
        return self.parentHassDevice.identifiers[0] + "_" + self.componentUniqueId

    @abstractmethod
    def getConfig(self) -> dict:
        pass

    def _buildStateSubtopic(self, topicName: str) -> str:
        return self.getStateTopic() + "/" + topicName
    
    def _buildStateSubtopicAndData(self, topicName: str, data) -> list:
        return [ self._buildStateSubtopic(topicName), data ]
    
    
    def getDiscoveryTopic(self) -> str:
        return self.parentHassDevice.getComponentDiscoveryTopic(self.componentTypeName, self.componentUniqueId)
    def getDataTopic(self) -> str:
        return self.parentHassDevice.getComponentDataTopic(self.componentTypeName, self.componentUniqueId)

    
    def getStateTopicName(self) -> str:
        return "state"
    def getStateTopic(self) -> str:
        return self.getDataTopic() + "/" + self.getStateTopicName()
    
    def getCommandTopicName(self) -> str:
        return "set"
    def getCommandTopic(self) -> str:
        return self.getDataTopic() + "/" + self.getCommandTopicName()
    
    def getUpdateAvailabilityTD(self, state: bool) -> list:
        return self._buildStateSubtopicAndData("avail", "online" if state else "offline")
    
    @abstractmethod
    def processCommandMessage(self, topicName: str, data) -> ACommand:
        self._logger.debug(f"processCommandMessage: {topicName} {data}")