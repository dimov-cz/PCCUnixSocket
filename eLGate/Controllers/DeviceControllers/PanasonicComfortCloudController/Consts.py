from ....__space__ import *
from typing import Optional, List, Dict
from .PccCommander.ACDeviceStateValue import ACDeviceStateValue as PccDeviceStateValue
from .PccCommander.ACDeviceState import ACDeviceState as PccDeviceState
from .PccCommander import Constants as PccConsts

class PccConstToElGateMapper:
    @staticmethod
    def operationMode(power: Optional[PccDeviceStateValue], mode: Optional[PccDeviceStateValue]) -> Optional[HvacOperationModeEnum]:
        if mode is None:        return None
        if power is None:       return None
        if power.value == PccConsts.Power.Off.value:            return HvacOperationModeEnum.Off
        if mode.value == PccConsts.OperationMode.Auto.value:    return HvacOperationModeEnum.Auto
        if mode.value == PccConsts.OperationMode.Dry.value:     return HvacOperationModeEnum.Dry
        if mode.value == PccConsts.OperationMode.Cool.value:    return HvacOperationModeEnum.Cool
        if mode.value == PccConsts.OperationMode.Heat.value:    return HvacOperationModeEnum.Heat
        if mode.value == PccConsts.OperationMode.Fan.value:     return HvacOperationModeEnum.Fan
        
class ELGateToPccConstMapper:
    @staticmethod
    def power(mode: Optional[HvacOperationModeEnum]) -> Optional[PccDeviceStateValue]:
        if mode is None:        return None
        if mode == HvacOperationModeEnum.Off: return PccDeviceStateValue(PccConsts.Power.Off.value)
        return PccDeviceStateValue(PccConsts.Power.On.value)
        
    @staticmethod
    def operationMode(mode: Optional[HvacOperationModeEnum]) -> Optional[PccDeviceStateValue]:
        if mode is None:        return None
        if mode == HvacOperationModeEnum.Off: return None
        if mode == HvacOperationModeEnum.Auto: return PccDeviceStateValue(PccConsts.OperationMode.Auto.value)
        if mode == HvacOperationModeEnum.Dry: return PccDeviceStateValue(PccConsts.OperationMode.Dry.value)
        if mode == HvacOperationModeEnum.Cool: return PccDeviceStateValue(PccConsts.OperationMode.Cool.value)
        if mode == HvacOperationModeEnum.Heat: return PccDeviceStateValue(PccConsts.OperationMode.Heat.value)
        if mode == HvacOperationModeEnum.Fan: return PccDeviceStateValue(PccConsts.OperationMode.Fan.value)
       
    @staticmethod 
    def ecoMode(ecoMode: Optional[HvacEcoModeEnum]) -> Optional[PccDeviceStateValue]:
        if ecoMode is None:        return None
        if ecoMode == HvacEcoModeEnum.Auto: return PccDeviceStateValue(PccConsts.EcoMode.Auto.value)
        if ecoMode == HvacEcoModeEnum.Quiet: return PccDeviceStateValue(PccConsts.EcoMode.Quiet.value)
        if ecoMode == HvacEcoModeEnum.Powerful: return PccDeviceStateValue(PccConsts.EcoMode.Powerful.value)
        
    @staticmethod
    def fanSpeed(fanSpeed: Optional[HvacFanSpeedEnum]) -> Optional[PccDeviceStateValue]:
        if fanSpeed is None:        return None
        if fanSpeed == HvacFanSpeedEnum.Auto: return PccDeviceStateValue(PccConsts.FanSpeed.Auto.value)
        if fanSpeed == HvacFanSpeedEnum.Low: return PccDeviceStateValue(PccConsts.FanSpeed.Low.value)
        if fanSpeed == HvacFanSpeedEnum.LowMid: return PccDeviceStateValue(PccConsts.FanSpeed.LowMid.value)
        if fanSpeed == HvacFanSpeedEnum.Mid: return PccDeviceStateValue(PccConsts.FanSpeed.Mid.value)
        if fanSpeed == HvacFanSpeedEnum.HighMid: return PccDeviceStateValue(PccConsts.FanSpeed.HighMid.value)
        if fanSpeed == HvacFanSpeedEnum.High: return PccDeviceStateValue(PccConsts.FanSpeed.High.value)
        
    @staticmethod
    def airSwingHorizontal(value: Optional[HvacAirSwingLREnum]) -> Optional[PccDeviceStateValue]:
        if value is None:        return None
        if value == HvacAirSwingLREnum.Auto: return PccDeviceStateValue(PccConsts.AirSwingLR.Auto.value)
        if value == HvacAirSwingLREnum.Left: return PccDeviceStateValue(PccConsts.AirSwingLR.Left.value)
        if value == HvacAirSwingLREnum.LeftMid: return PccDeviceStateValue(PccConsts.AirSwingLR.LeftMid.value)
        if value == HvacAirSwingLREnum.Mid: return PccDeviceStateValue(PccConsts.AirSwingLR.Mid.value)
        if value == HvacAirSwingLREnum.RightMid: return PccDeviceStateValue(PccConsts.AirSwingLR.RightMid.value)
        if value == HvacAirSwingLREnum.Right: return PccDeviceStateValue(PccConsts.AirSwingLR.Right.value)
        
    @staticmethod
    def airSwingVertical(value: Optional[HvacAirSwingUDEnum]) -> Optional[PccDeviceStateValue]:
        if value is None:        return None
        if value == HvacAirSwingUDEnum.Auto: return PccDeviceStateValue(PccConsts.AirSwingUD.Auto.value)
        if value == HvacAirSwingUDEnum.Swing: return PccDeviceStateValue(5) #missing in currect stable pcc, pr sent
        if value == HvacAirSwingUDEnum.Up: return PccDeviceStateValue(PccConsts.AirSwingUD.Up.value)
        if value == HvacAirSwingUDEnum.UpMid: return PccDeviceStateValue(PccConsts.AirSwingUD.UpMid.value)
        if value == HvacAirSwingUDEnum.Mid: return PccDeviceStateValue(PccConsts.AirSwingUD.Mid.value)
        if value == HvacAirSwingUDEnum.DownMid: return PccDeviceStateValue(PccConsts.AirSwingUD.DownMid.value)
        if value == HvacAirSwingUDEnum.Down: return PccDeviceStateValue(PccConsts.AirSwingUD.Down.value)
        
    @staticmethod
    def nanoe(value: Optional[HvacNanoeModeEnum]) -> Optional[PccDeviceStateValue]:
        if value is None:        return None
        if value == HvacNanoeModeEnum.Unavailable: return None
        if value == HvacNanoeModeEnum.On: return PccDeviceStateValue(PccConsts.NanoeMode.On.value)
        if value == HvacNanoeModeEnum.Off: return PccDeviceStateValue(PccConsts.NanoeMode.Off.value)
        if value == HvacNanoeModeEnum.ModeG: return PccDeviceStateValue(PccConsts.NanoeMode.ModeG.value)
        if value == HvacNanoeModeEnum.All: return PccDeviceStateValue(PccConsts.NanoeMode.All.value)
        
    @staticmethod
    def presets(eLGatePresets) -> Dict[str, PccDeviceState]:
        pccPresets = {}
        for presetName in eLGatePresets:
            preset = eLGatePresets[presetName]
            try:
                state: PccDeviceState = PccDeviceState()
                mode = preset['mode'] if preset['mode'] else 'Off'; # note: Off in yaml is False
                state.power = ELGateToPccConstMapper.power(HvacOperationModeEnum[mode])
                state.mode = ELGateToPccConstMapper.operationMode(HvacOperationModeEnum[mode])
                state.eco = ELGateToPccConstMapper.ecoMode(HvacEcoModeEnum[preset['eco']] if 'eco' in preset else None)
                state.fanSpeed = ELGateToPccConstMapper.fanSpeed(HvacFanSpeedEnum[preset['fanSpeed']] if 'fanSpeed' in preset else None)
                state.airSwingHorizontal = ELGateToPccConstMapper.airSwingHorizontal(HvacAirSwingLREnum[preset['airSwingHorizontal']] if 'airSwingHorizontal' in preset else None)
                state.airSwingVertical = ELGateToPccConstMapper.airSwingVertical(HvacAirSwingUDEnum[preset['airSwingVertical']] if 'airSwingVertical' in preset else None)
                state.nanoe = ELGateToPccConstMapper.nanoe(HvacNanoeModeEnum[preset['nanoe']] if 'nanoe' in preset else None)
                pccPresets[presetName] = state
            except Exception as e:
                logging.getLogger(__name__).error(f"Error in preset {presetName}: {e}")
        return pccPresets
        
        
        """

class AirSwingUD(Enum):
    Auto = -1
    Up = 0
    UpMid = 3
    Mid = 2
    DownMid = 4
    Down = 1
    Swing = 5

class AirSwingLR(Enum):
    Auto = -1
    Left = 1
    LeftMid = 5
    Mid = 2
    RightMid = 4
    Right = 0

class EcoMode(Enum):
    Auto = 0
    Powerful = 1
    Quiet = 2

class AirSwingAutoMode(Enum):
    Disabled = 1
    Both = 0
    AirSwingLR = 3
    AirSwingUD = 2

class FanSpeed(Enum):
    Auto = 0
    Low = 1
    LowMid = 2
    Mid = 3
    HighMid = 4
    High = 5

class dataMode(Enum):
    Day = 0
    Week = 1
    Month = 2
    Year = 4

class NanoeMode(Enum):
    Unavailable = 0
    Off = 1
    On = 2
    ModeG = 3
    All = 4

        """