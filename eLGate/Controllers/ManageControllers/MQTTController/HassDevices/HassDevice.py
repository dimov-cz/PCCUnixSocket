from ..__space__ import *

class HassDevice:
    
    def __init__(self, identifiers: list, name, sw_version, model, manufacturer):
        self.identifiers = identifiers
        self.name = name
        self.sw_version = sw_version
        self.model = model
        self.manufacturer = manufacturer
        
    def getConfig(self):
        return {
            "identifiers": self.identifiers,
            "name": self.name,
            "sw_version": self.sw_version,
            "model": self.model,
            "manufacturer": self.manufacturer
        }