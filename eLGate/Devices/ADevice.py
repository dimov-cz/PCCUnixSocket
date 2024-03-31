from ..__space__ import *

class ADevice(ALoggable, ABC):
    
    logger: logging.Logger
    
    id: str
    _shortId: Optional[str] = None
    name: str
    model: str
    manufacturer: str
    
    def __init__(self, id: str, name: str, model: str = "", manufacturer: str = "") -> None:
        ALoggable.__init__(self)
        self.id = id
        self.name = name
        self.model = model
        self.manufacturer = manufacturer
        
    #for usage by system wich don't support long device ids
    def getShortId(self):
        if self._shortId is None:
            self._shortId = self.__calcDeviceId(self.id)
        return self._shortId
    
    def __str__(self) -> str:
        return "ADevice(" + self.id + ", " + self.name + ", " + self.model + ", " + self.manufacturer + ")"
    
    #creates shorter hash from pcc guid to use as deviceId
    #this helps integrate with other systems
    @staticmethod
    def __calcDeviceId(long_hash):
        # Convert hex to bytes
        hash_bytes = bytes.fromhex(long_hash)

        # Sum first 8 bytes XOR last 8 bytes
        sum_bytes = hash_bytes[:8] + hash_bytes[-8:]
        sum_value = bytes(x ^ y for x, y in zip(sum_bytes[:8], sum_bytes[8:]))

        # Convert 8-byte value to hex 
        short_hash = hex(int.from_bytes(sum_value, byteorder='big'))[2:]
        return short_hash