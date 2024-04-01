from eLGate.__space__ import Settings
from ....__space__ import *
import time
from typing import Self

from .PccCommander.PccCommander import PccCommander as PccCommander
from .PccCommander.Response import Response as PccResponse
from .PccCommander.ResponseType import ResponseType as PccResponseType
from .PccCommander.ACDeviceState import ACDeviceState as PccDeviceState
from .PccCommander.ACDeviceStateValue import ACDeviceStateValue as PccDeviceStateValue

from .Consts import PccConstToElGateMapper, ELGateToPccConstMapper

class PanasonicComfortCloudDeviceController(ADeviceController):
    pcc: Optional[PccCommander] = None
    autoUpdateTime: float = 60
    lastUpdateStart: float = 0
    
    def __init__(self, settings: Settings) -> None:
        super().__init__()

        eLGatePresets = settings.getDict('presets')
        self.pcc = PccCommander(
            presets = ELGateToPccConstMapper.presets(eLGatePresets),
        )
        self.pcc.setLogLevel(self._logger.getEffectiveLevel())
        
        tokenPath = settings.getString('tokenPath', '~/pcc-')
        for account in Settings.getList(settings, 'accounts'):
            self.pcc.addAccount(
                login     = account['login'],
                password  = account['password'],
                tokenPath = tokenPath + account['login']
            )
    
    def factoryBuild(settings: Settings) -> Self:
        return PanasonicComfortCloudDeviceController(
            settings = settings
        )

    def setLogLevel(self, level):
        if (self.pcc):
            self.pcc.setLogLevel(level)
        super().setLogLevel(level)
    
    def stop(self):
        #self.pcc.stop()
        pass
    
    def loop(self):
        if self.pcc is None:
            return
        
        for response in iter(self.pcc.getResponse, None):
            if response.type == PccResponseType.Registration:
                device = response.device
                if device is None:
                    self._logger.error("Got registration response without device")
                    return
                deviceInfo = device.getDeviceInfo()
                self._logger.debug(f"Got registration response: {deviceInfo}")
                self.sendMessage(
                    NewDeviceMessage(
                        HvacDevice(
                            deviceInfo.deviceId, 
                            deviceInfo.name, 
                            deviceInfo.model, 
                            "Panasonic",
                            modes= [ 
                                    HvacOperationModeEnum.Off,
                                    HvacOperationModeEnum.Auto,
                                    HvacOperationModeEnum.Cool,
                                    HvacOperationModeEnum.Heat,
                                    HvacOperationModeEnum.Dry,
                                    HvacOperationModeEnum.Fan
                            ], 
                            presetsIds= self.pcc.getPresetsIds()
                        )
                    )
                )
                #request first status immediately
                self.pcc.requestStatus(deviceInfo.deviceId)
            elif response.type == PccResponseType.Status:
                device = response.device
                if device is None:
                    self._logger.error("Got status response without device")
                    return
                
                self._logger.debug(f"Got status response: {device} {response.data}")
                
                deviceInfo = device.getDeviceInfo()
                data = response.data #type: PccDeviceState
                if not isinstance(data, PccDeviceState):
                    self._logger.error("Got status response with wrong data type")
                    return
                self.sendMessage(
                    ClimateStateMessage(
                        deviceId= deviceInfo.deviceId,
                        available= data.available,
                        mode= PccConstToElGateMapper.operationMode(data.power, data.mode),
                        presetId= data.presetId,
                        currentTemperatureIn= data.temperatureInside, 
                        currentTemperatureOut= data.temperatureOutside,
                        targetTemperature= data.temperature,
                    )
                )
            else:
                self._logger.info(f"Got unk response: {response.type}")

        if self.lastUpdateStart + self.autoUpdateTime < time.time():
            self.lastUpdateStart = time.time()
            self.pcc.requestStatusAll()
    
    def processClimateCommand(self, command: ClimateCommand):
        if not self.pcc:
            self._logger.error("Got command, but pcc is not initialized")
            return
        if not self.pcc.hasDevice(command.device.id):
            self._logger.debug(f"Command is for other device: {command.device.id}")
            return
        
        self._logger.debug(f"Got command: {command}")
        newState = PccDeviceState()
        if command.preset is not None:
            newState = self.pcc.getPresetState(command.preset)
        if command.temperature is not None:
            newState.temperature = command.temperature
        if command.mode is not None:
            newState.power = ELGateToPccConstMapper.power(command.mode)
            newState.mode = ELGateToPccConstMapper.operationMode(command.mode)
        
        self.pcc.requestSetState(command.device.id, newState)