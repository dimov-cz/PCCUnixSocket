from ...__space__ import *
from enum import Enum

class HvacOperationModeEnum(Enum):
    Off = 0
    Auto = 1
    Cool = 2
    Heat = 3
    Dry = 4
    Fan = 5

class HvacEcoModeEnum(Enum):
    Auto = 1
    Quiet = 2
    Powerful = 3


class HvacAirSwingAutoModeEnum(Enum):
    Disabled = 0
    AirSwingUD = 1
    AirSwingLR = 2
    Both = 3

# vertical axis
class HvacAirSwingUDEnum(Enum):
    Auto = 1
    Swing = 2
    
    Up = 10
    UpMid = 15
    Mid = 20
    DownMid = 25
    Down = 30
    
#horizontal axis
class HvacAirSwingLREnum(Enum):
    Auto = 1
    
    Left = 10
    LeftMid = 15
    Mid = 20
    RightMid = 25
    Right = 30

class HvacFanSpeedEnum(Enum):
    Auto = 1
    Low = 10
    LowMid = 15
    Mid = 20
    HighMid = 25
    High = 30

#Fan modes
#“auto”, “low”, “medium”, “high
class HvacNanoeModeEnum(Enum):
    Unavailable = -1
    Off = 0
    On = 1
    ModeG = 2
    All = 3
