from hashlib import md5
from ..__space__ import *

class ADevice(ALoggable, ABC):
    
    logger: logging.Logger
    
    id: str
    _shortId: Optional[str]
    name: str
    model: str
    manufacturer: str
    version: str
    
    def __init__(self, id: str, name: str, model: str = "", manufacturer: str = "", version:str = "") -> None:
        ALoggable.__init__(self)
        self.id = id
        self.name = name
        self.model = model
        self.manufacturer = manufacturer
        self.version = version
        
        self._shortId = None
        
    #for usage by system wich don't support long device ids,
    #we need ensure is 16 chars max
    def getShortId(self):
        if self._shortId is None:
            self._shortId = self.__calcDeviceId(self.id)
        return self._shortId
    
    def __str__(self) -> str:
        return "ADevice(" + self.id + ", " + self.name + ", " + self.model + ", " + self.manufacturer + ")"
    
    #creates shorter hash
    #this helps integrate with other systems
    @staticmethod
    def __calcDeviceId(long_id: str) -> str:
        if len(long_id)<=16:
            return long_id
        
        # Convert hex to bytes
        hash_bytes = None
        try:
            if len(long_id) == 32:
                hash_bytes = bytes.fromhex(long_id)
        except ValueError:
            pass

        if hash_bytes is None:
            hash_bytes = md5(long_id.encode('utf-8')).digest() #return 16 bytes

        # Sum first 8 bytes XOR last 8 bytes
        sum_bytes = hash_bytes[:8] + hash_bytes[-8:]
        sum_value = bytes(x ^ y for x, y in zip(sum_bytes[:8], sum_bytes[8:]))

        # Convert 8-byte value to hex 
        short_hash = hex(int.from_bytes(sum_value, byteorder='big'))[2:]
        return short_hash