from ..__space__ import *

class AHassComponent(ALoggable, ABC):
    device: ADevice
    parentHassDevice: HassDevice

    dataMainTopic: str
    discoveryMainTopic: str

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
        
        dataMainTopic: str = "homeassistant",
        discoveryMainTopic: str = "homeassistant",
        
        componentUniqueId: Optional[str] = None,
        componentName: Optional[str] = None,
    ) -> None:
        ALoggable.__init__(self)
        self.device = device
        self.parentHassDevice = parentHassDevice

        self.dataMainTopic = dataMainTopic
        self.discoveryMainTopic = discoveryMainTopic

        self.componentUniqueId = componentUniqueId if componentUniqueId is not None else self.device.getShortId()
        self.componentName = componentName if componentName  is not None else self.device.name
        
    def getUniqueId(self) -> str:
        return self.parentHassDevice.identifiers[0] + "_" + self.componentUniqueId

    @abstractmethod
    def getConfig(self) -> dict:
        pass
    
    def getDiscoveryTopic(self) -> str:
        return f"{self.discoveryMainTopic}/{self.componentTypeName}/{self.parentHassDevice.name}/{self.componentUniqueId}/config"
    
    def getDeviceTopic(self) -> str:
        return f"{self.dataMainTopic}/{self.parentHassDevice.name}/{self.componentTypeName}/{self.device.manufacturer}/{self.componentUniqueId}"
    def getStateTopicName(self) -> str:
        return "state"
    def getStateTopic(self) -> str:
        return self.getDeviceTopic() + "/" + self.getStateTopicName()
    def getCommandTopicName(self) -> str:
        return "set"
    def getCommandTopic(self) -> str:
        return self.getDeviceTopic() + "/" + self.getCommandTopicName()
    
    @abstractmethod
    def processCommandMessage(self, topicName: str, data) -> ACommand:
        self._logger.debug(f"processCommandMessage: {topicName} {data}")