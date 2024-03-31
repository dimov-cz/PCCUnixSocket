from ...__space__ import *

class HvacHassModeEnum(Enum):
    Off = "off"
    Auto = "auto"
    Cool = "cool"
    Heat = "heat"
    Dry = "dry"
    Fan = "fan_only"
    
    def getELGateMode(self) -> HvacOperationModeEnum:
        if self == HvacHassModeEnum.Off:  return HvacOperationModeEnum.Off
        if self == HvacHassModeEnum.Auto: return HvacOperationModeEnum.Auto
        if self == HvacHassModeEnum.Cool: return HvacOperationModeEnum.Cool
        if self == HvacHassModeEnum.Heat: return HvacOperationModeEnum.Heat
        if self == HvacHassModeEnum.Dry:  return HvacOperationModeEnum.Dry
        if self == HvacHassModeEnum.Fan:  return HvacOperationModeEnum.Fan
        raise Exception(f"Unknown mode to eLGate: {self}")
    
    @staticmethod
    def createFromELGateMode(mode: HvacOperationModeEnum) -> "HvacHassModeEnum":
        if mode == HvacOperationModeEnum.Off:  return HvacHassModeEnum.Off
        if mode == HvacOperationModeEnum.Auto: return HvacHassModeEnum.Auto
        if mode == HvacOperationModeEnum.Cool: return HvacHassModeEnum.Cool
        if mode == HvacOperationModeEnum.Heat: return HvacHassModeEnum.Heat
        if mode == HvacOperationModeEnum.Dry:  return HvacHassModeEnum.Dry
        if mode == HvacOperationModeEnum.Fan:  return HvacHassModeEnum.Fan
        raise Exception(f"Unknown mode to HASS: {mode}")
