from ..__space__ import *

class SelectHassComponent(AHassComponent):
    selectOptions: List[str]

    def __init__(
        self, 
        device: ADevice,
        parentHassDevice: HassDevice,
        
        dataMainTopic: str = "homeassistant",
        discoveryMainTopic: str = "homeassistant",
        
        componentUniqueId: Optional[str] = None,
        componentName: Optional[str] = None,
        selectOptions: List[str] = []
    ) -> None:
        super().__init__(
            device=device,
            parentHassDevice=parentHassDevice,
            dataMainTopic=dataMainTopic,
            discoveryMainTopic=discoveryMainTopic,
            componentUniqueId=componentUniqueId,
            componentName=componentName,
        )
        self.selectOptions = selectOptions

    @property
    def componentTypeName(self) -> str:
        return "select"

    def getConfig(self) -> dict:
        baseTopic = self.getDeviceTopic()
        stateTopic = '~/' + self.getStateTopicName()
        commandTopic = '~/' + self.getCommandTopicName()

        config = {
            "~": baseTopic,
            "name": self.componentName,
            "state_topic": stateTopic,
            "command_topic": commandTopic,
            
            "device": self.parentHassDevice.getConfig(),         
            "force_update": True,

            "options": self.selectOptions,

            "unique_id": self.getUniqueId(),
            "device_class": "switch", # illuminance / *humidity*
            
            'availability_topic': stateTopic + '/avail',
            'payload_available': 'online',
            'payload_not_available': 'offline',
        }
        return config
        
    def processCommandMessage(self, topicName: str, data) -> ACommand:
        self._logger.debug(f"processCommandMessage select: {topicName} {data}")
    
    def getSetStateTD(self, value: str):
        return [ self.getStateTopic(), value ]
