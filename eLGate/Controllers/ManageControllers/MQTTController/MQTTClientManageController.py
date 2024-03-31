from typing import Dict
import json
from .__space__ import *

from .hass_mqtt_discovery.hass_mqtt_device import Climate as HassClimate
from .hass_mqtt_discovery.hass_mqtt_device import Device as HassDevice2

class MQTTClientManageController(AManageController):
    mqttConnector: MQTTClientConnector
    _gateDevice: Optional[HassDevice] = None
    activeComponents: Dict[str, AHassComponent] = {}
    
    
    def __init__(self, clientId: str, hostname: str = "localhost", port: int = 1883, username: str = "", password: str = ""):
        super().__init__()
        
        self.mqttConnector = MQTTClientConnector()
        self.mqttConnector.setUp(
                            clientId= clientId, 
                            hostname= hostname,
                            port=     port,
                            username= username,
                            password= password,
                            messageCallback= self._on_message,
                            subscribeTopics= [ "homeassistant/#"]
        )
        self.mqttConnector.start()
                
    def stop(self):
        self.mqttConnector.stop()
        self.mqttConnector.join()
        
    def _on_message(self, client, userdata, msg):
        for component in self.activeComponents.values():
            #if commandTopic is the current topic (from first char)
            cmdTopic = component.getCommandTopic()
            if cmdTopic == msg.topic[:len(cmdTopic)]:
                subtopic = msg.topic[len(cmdTopic)+1:]
                self._logger.debug(f"Processing message for {component} -- {subtopic} -- {msg.payload}")
                try:
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
            self._gateDevice = HassDevice(["eLGate"], "eLGate", "v0.1", "0", "eL")
        return self._gateDevice

    def _sendConfig(self, component: AHassComponent):
        self._logger.info(f"Sending config for {component}")
        config = component.getConfig()
        self.mqttConnector.getClient().publish(component.getDiscoveryTopic(), json.dumps(config), retain=False)
        
    def _sendData(self, topicAndData: list):
        mqttClient = self.mqttConnector.getClient()
        mqttClient.publish(topicAndData[0], topicAndData[1], retain=False)
        
    def processNewDevice(self, message: NewDeviceMessage):
        self._logger.info(f"Processing new device: {message}")
        deviceId = message.device.id
        if deviceId not in self.activeComponents.values():
            if isinstance(message.device, HvacDevice):
                self._logger.info(f"Processing new HVAC: {message.device}")                
                newComponent = HvacHassComponent(
                                    device=message.device, 
                                    parentHassDevice=self.meAsDevice()
                )
                self.activeComponents[deviceId] = newComponent
                self._sendConfig(newComponent)
                self.mqttConnector.getClient().subscribe(newComponent.getCommandTopic()+'/#')
            else:
                self._logger.info(f"Unsupported device type: {message.device}")
                
    def processClimateState(self, message: ClimateStateMessage):
        self._logger.info(f"Processing climate state: {message}")
        if message.deviceId not in self.activeComponents:
            self._logger.error(f"Device not found: {message.deviceId}")
            return
        device = self.activeComponents[message.deviceId]
        if not isinstance(device, HvacHassComponent):
            self._logger.error(f"Device is not a climate device: {message.deviceId}")
            return
        
        if message.available is not None: self._sendData(device.getUpdateAvailabilityTD(message.available))
        if message.mode is not None:    self._sendData(device.getUpdateModeTD(message.mode))
        if message.presetId is not None: self._sendData(device.getUpdatePresetTD(message.presetId))
        if message.targetTemperature is not None: self._sendData(device.getUpdateTargetTemperatureTD(message.targetTemperature))
        if message.currentTemperatureIn is not None: self._sendData(device.getUpdateInsideTemperatureTD(message.currentTemperatureIn))
        if message.currentTemperatureOut is not None: self._sendData(device.getUpdateOutsideTemperatureTD(message.currentTemperatureOut))