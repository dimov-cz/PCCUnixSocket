import json
from ..__space__ import *

from .Consts.HvacHassConsts import HvacHassModeEnum

class HvacHassComponent(AHassComponent):
    device: HvacDevice
    
    @property
    def componentTypeName(self) -> str:
        return "climate"
            
    #A list of supported modes. Needs to be a subset of the default values.
    # Default: [“auto”, “off”, “cool”, “heat”, “dry”, “fan_only”]
    def defaultModes(self) -> list:
        return [ "off", "auto", "cool", "heat", "dry", "fan_only" ]
        
    def _checkModes(self, modes) -> list:
        out = []
        for mode in modes:
            if mode in self.defaultModes():
                out.append(mode)
            else:
                raise Exception("Mode not supported: " + mode)
        return out
        
    def getConfig(self) -> dict:
        baseTopic = self.getDataTopic()
        stateTopic = '~/' + self.getStateTopicName()
        commandTopic = '~/' + self.getCommandTopicName()
        presetsIds = self.device.presetsIds.copy()
        if "none" in presetsIds:
            presetsIds.remove("none") #not allowed in HASS
        config = {
            "~": baseTopic,
            "name": self.componentName,
            #"state_topic": "~/state",
            #"unit_of_measurement": self.unit_of_measurement, #NI in DCZ?
            
            "device": self.parentHassDevice.getConfig(),         
            "force_update": True,

            "unique_id": self.getUniqueId(),
            "device_class": "hvac", # illuminance / *humidity*
            "stat_t": "~/state",
            
            'availability_topic': stateTopic + '/avail',
            'payload_available': 'online',
            'payload_not_available': 'offline',

            #actuator temp:
            'temperature_state_topic': stateTopic + '/temp',
            #'temperature_state_template': '{{ value_json.temp }}',
            "temp_unit": 'C',
            'temperature_command_topic': commandTopic + '/temp',
            #'temperature_command_template': '{{ value_json.temp }}',
            
            'current_temperature_topic': stateTopic + '/curr_temp_in',
            
            "modes": [ HvacHassModeEnum.createFromELGateMode(mode).value for mode in self.device.modes ],
            'mode_state_topic': stateTopic + '/mode',
            'mode_state_template': '{{ value_json.modeId }}', #because of domoticz FixCommandTopicStateTemplate, topic must differ from json data attribute...
            'mode_command_topic': commandTopic + '/mode',
            #'mode_command_template': '{{ value }}',                 #Hass, plain value
            'mode_command_template': '{"modeId": "{{ value }}"}',   #Hass, json value
            
            "preset_modes": presetsIds,
            'preset_mode_state_topic': stateTopic + '/preset',
            'preset_mode_value_template': '{{ value_json.presetId }}',
            'preset_mode_command_topic': commandTopic + '/preset',
            'preset_mode_command_template': '{"presetId": "{{ value }}"}', 
            
            #'swing_modes': [ "Off", "Vertical", "Horizontal", "Both" ],
            #'swing_mode_state_topic': stateTopic + '/swing',
            #'swing_mode_command_topic': commandTopic + '/swing',
            
        }
        return config
    
    def getUpdateModeTD(self, mode: HvacOperationModeEnum) -> list:
        eLMode = HvacHassModeEnum.createFromELGateMode(mode)
        return self._buildStateSubtopicAndData("mode",   json.dumps( { "modeId": eLMode.value, "modeName": eLMode.name }) )
    
    def getUpdatePresetTD(self, preset: str) -> list:
        return self._buildStateSubtopicAndData("preset", json.dumps( { "presetId": preset } ))
    
    def getUpdateTargetTemperatureTD(self, temp: Optional[float]) -> list:
        return self._buildStateSubtopicAndData("temp", temp)
    
    def getUpdateInsideTemperatureTD(self, temp: Optional[float]) -> list:
        return self._buildStateSubtopicAndData("curr_temp_in", temp)
    
    def getUpdateOutsideTemperatureTD(self, temp: Optional[float]) -> list:
        return self._buildStateSubtopicAndData("curr_temp_out", temp)
    
    def processCommandMessage(self, topicName: str, data) -> ACommand:
        self._logger.debug(f"processCommandMessage: {data} in {topicName}")
        if topicName == "mode":
            try:
                data = json.loads(data)
                if not "modeId" in data:
                    raise Exception(f"No modeId in data: {data}")
                hassMode = HvacHassModeEnum(data.get("modeId"))
                return ClimateCommand(device= self.device, mode=hassMode.getELGateMode())
            except Exception as e:
                raise Exception(f"Unknown mode data: {data} {e}")
        elif topicName == "temp":
            return ClimateCommand(device= self.device, temperature= float(data))
        elif topicName == "preset":
            try:
                data = json.loads(data)
                if not "presetId" in data:
                    raise Exception(f"No presetId in data: {data}")
                return ClimateCommand(device= self.device, preset=data.get("presetId"))
            except Exception as e:
                raise Exception(f"Unknown mode data: {data} {e}")
        else:
            raise Exception(f"Unknown set topic: {topicName} {data}")