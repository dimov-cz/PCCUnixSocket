from typing import Dict, Self

import json

from eLGate.__space__ import Settings
from .__space__ import *

class MQTTClientManageController(AManageController):
    mqttConnector: MQTTClientConnector
    _gateDevice: Optional[HassDevice]
    activeComponents: Dict[str, Dict[str, AHassComponent]]
    
    
    def __init__(self, clientId: str, hostname: str = "localhost", port: int = 1883, username: str = "", password: str = "", development: bool = False):
        super().__init__()
        self._gateDevice = None
        self.development = development
        self.activeComponents = {}
        
        self.mainDataTopic = "homeassistant"
        self.mainDiscoveryTopic = "homeassistant"

        self.mqttConnector = MQTTClientConnector()
        self.mqttConnector.setUp(
                            clientId= clientId, 
                            hostname= hostname,
                            port=     port,
                            username= username,
                            password= password,
                            messageCallback= self._on_message,
                            subscribeTopics= [ self.mainDataTopic + "/#"]
        )
        self.mqttConnector.start()

    def factoryBuild(settings: Settings) -> Self:
        return MQTTClientManageController(
            hostname=settings.getString('host', 'localhost'),
            port    =settings.getInt(   'port', 1883),
            clientId=settings.getString('id',   "eLGate"),
            username=settings.getString('login', ''),
            password=settings.getString('password', ''),
            development=settings.getBool('development', False)
        )
                
    def stop(self):
        self.mqttConnector.stop()
        self.mqttConnector.join()
        
    def _on_message(self, client, userdata, msg):
        for componentsList in self.activeComponents.values():
            for cKey, component in componentsList.items():
                #if commandTopic is the current topic (from first char)
                cmdTopic = component.getCommandTopic()
                if cmdTopic == msg.topic[:len(cmdTopic)]:
                    subtopic = msg.topic[len(cmdTopic)+1:]
                    self._logger.debug(f"Processing message for {component} -- {subtopic} -- {msg.payload}")
                    try:
                        if isinstance(component.device, ProjectorDevice):
                            command = ProjectorCommand(component.device)
                            if cKey == "main": command.power = component.processCommandMessage(subtopic, msg.payload).state
                            elif cKey == "src": command.source = msg.payload.decode("utf-8")
                            elif cKey == "colormode": command.colorMode = msg.payload.decode('utf-8')
                        else:
                            command = component.processCommandMessage(subtopic, msg.payload)
                        self.sendCommand(command)
                    except Exception as e:
                        self._logger.error(f"Error processing command message: {e}")
                    return
        self._logger.warning(f"Message for unknown topic: {msg}")
        
    def loop(self):
        if not self.mqttConnector.isConnected():
            return
        
        #self._logger.debug("MQTT connected - loop")
    
    
    def meAsDevice(self) -> HassDevice:
        if self._gateDevice is None:
            self._gateDevice = HassDevice(
                "eLGate", "eLGate" , 
                "eLGate", "v0.2", "0", "eL", 
                self.mainDataTopic, self.mainDiscoveryTopic
            )
        return self._gateDevice
    
    def _sendConfig(self, component: AHassComponent):
        self._logger.info(f"Sending config for {component}")
        config = component.getConfig()
        self.mqttConnector.getClient().publish(
                                    component.getDiscoveryTopic(), 
                                    json.dumps(config), 
                                    retain= not self.development  #retain only in production
        )
        
    def _sendData(self, topicAndData: list, retain: bool = False):
        mqttClient = self.mqttConnector.getClient()
        if self.development:
            retain = False
        mqttClient.publish(topicAndData[0], topicAndData[1], retain= retain)
        
    def processNewDevice(self, message: NewDeviceMessage):
        self._logger.info(f"Processing new device: {message}")
        deviceId = message.device.id
        if deviceId not in self.activeComponents.values():
            if isinstance(message.device, ADevice):
                d = message.device;
                hassDevice = HassDevice(
                    d.id, d.getShortId(),
                    d.name, d.version, d.model, d.manufacturer,
                    self.mainDataTopic, self.mainDiscoveryTopic
                )
            else:
                hassDevice = self.meAsDevice()

            if isinstance(message.device, HvacDevice):
                self._logger.info(f"Processing new HVAC: {message.device}")
                newComponent = HvacHassComponent(
                                    device=message.device, 
                                    parentHassDevice=hassDevice
                )
                self.activeComponents[deviceId] = {}
                self.activeComponents[deviceId]["main"] = newComponent
                self._sendConfig(newComponent)
                self.mqttConnector.getClient().subscribe(newComponent.getCommandTopic()+'/#')

            elif isinstance(message.device, ProjectorDevice):
                self._logger.info(f"Processing new projector: {message.device}")
                self.activeComponents[deviceId] = {}
                newComponent = SwitchHassComponent( message.device, hassDevice, "PWR", "Power")
                self.activeComponents[deviceId]["main"] = newComponent
                self._sendConfig(newComponent)
                self.mqttConnector.getClient().subscribe(newComponent.getCommandTopic()+'/#')

                newComponent = SelectHassComponent(
                                    device=message.device,
                                    parentHassDevice=hassDevice,
                                    componentUniqueId= "SRC",
                                    componentName= "Source",
                                    selectOptions=message.device.sourcesList
                )
                self.activeComponents[deviceId]["src"] = newComponent
                self._sendConfig(newComponent)
                self.mqttConnector.getClient().subscribe(newComponent.getCommandTopic()+'/#')

                newComponent = SelectHassComponent(
                                    device=message.device,
                                    parentHassDevice=hassDevice,
                                    componentUniqueId= "MODE",
                                    componentName= "Mode",
                                    selectOptions=message.device.colorModesList
                )
                self.activeComponents[deviceId]["colormode"] = newComponent
                self._sendConfig(newComponent)
                self.mqttConnector.getClient().subscribe(newComponent.getCommandTopic()+'/#')
            else:
                self._logger.info(f"Unsupported device type: {message.device}")
                
    def processClimateState(self, message: ClimateStateMessage):
        self._logger.info(f"Processing climate state: {message}")
        if message.deviceId not in self.activeComponents:
            self._logger.error(f"Device not found: {message.deviceId}")
            return
        hassComponent = self.activeComponents[message.deviceId]["main"]
        if not isinstance(hassComponent, HvacHassComponent):
            self._logger.error(f"Device is not a climate device: {message.deviceId}")
            return
        
        if message.available is not None: self._sendData(hassComponent.getUpdateAvailabilityTD(message.available))
        if message.mode is not None:    self._sendData(hassComponent.getUpdateModeTD(message.mode))
        if message.presetId is not None: self._sendData(hassComponent.getUpdatePresetTD(message.presetId))
        if message.targetTemperature is not None: self._sendData(hassComponent.getUpdateTargetTemperatureTD(message.targetTemperature))
        if message.currentTemperatureIn is not None: self._sendData(hassComponent.getUpdateInsideTemperatureTD(message.currentTemperatureIn))
        if message.currentTemperatureOut is not None: self._sendData(hassComponent.getUpdateOutsideTemperatureTD(message.currentTemperatureOut))

    def processProjectorState(self, message: ProjectorStateMessage):
        self._logger.info(f"Processing projector state: {message}")
        if message.deviceId not in self.activeComponents:
            self._logger.error(f"Device not found: {message.deviceId}")
            return
        powerComp = self.activeComponents[message.deviceId]["main"]
        sourceComp = self.activeComponents[message.deviceId]["src"]
        colorModeComp = self.activeComponents[message.deviceId]["colormode"]
        
        if message.power is not None:
            if message.available is not None: 
                self._sendData(powerComp.getUpdateAvailabilityTD(message.available))
            self._sendData(powerComp.getSetStateTD(message.power))

        if message.availableSettings is not None: 
            self._sendData(sourceComp.getUpdateAvailabilityTD(message.availableSettings))
            self._sendData(colorModeComp.getUpdateAvailabilityTD(message.availableSettings))

        if message.source is not None:
            self._sendData(sourceComp.getSetStateTD(message.source))
        
        if message.colorMode is not None:
            self._sendData(colorModeComp.getSetStateTD(message.colorMode))

        