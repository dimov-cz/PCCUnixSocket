from ..__space__ import *

class SwitchHassComponent(AHassComponent):


    @property
    def componentTypeName(self) -> str:
        return "switch"

    def getConfig(self) -> dict:
        baseTopic = self.getDataTopic()
        stateTopic = '~/' + self.getStateTopicName()
        commandTopic = '~/' + self.getCommandTopicName()

        config = {
            "~": baseTopic,
            "name": self.componentName,
            "state_topic": stateTopic,
            "command_topic": commandTopic,
            
            "device": self.parentHassDevice.getConfig(),         
            "force_update": True,

            "payload_off": 'OFF',
            "payload_on": 'ON',

            "unique_id": self.getUniqueId(),
            "device_class": "switch", # illuminance / *humidity*
            
            'availability_topic': stateTopic + '/avail',
            'payload_available': 'online',
            'payload_not_available': 'offline',
        }
        return config
        
    def processCommandMessage(self, topicName: str, data) -> ACommand:
        self._logger.debug(f"processCommandMessage at switch: {topicName} {data}")
        return SwitchCommand(
            self.device, 
            data.decode('utf-8') == 'ON',
        )
    
    def getSetStateTD(self, s: bool):
        return [ self.getStateTopic(), "ON" if s else "OFF" ]
