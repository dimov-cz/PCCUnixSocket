from ..__space__ import *

class HassDevice:
    uniqueId: str
    shortId: str
    identifiers: List[str]
    name: str
    sw_version: str
    model: str
    manufacturer: str

    dataTopicPrefix: str
    discoveryTopicPrefix: str

    
    def __init__(self, 
                 uniqueId: str, 
                 shortId: str, 
                 name: str, 
                 sw_version: str, 
                 model: str, 
                 manufacturer: str,

                dataTopicPrefix: str,
                discoveryTopicPrefix: str,
    ):
        self.uniqueId = uniqueId
        self.shortId = shortId
        self.identifiers = [ uniqueId, shortId ]
        self.name = name
        self.sw_version = sw_version
        self.model = model
        self.manufacturer = manufacturer

        self.dataTopicPrefix = dataTopicPrefix
        self.discoveryTopicPrefix = discoveryTopicPrefix
        
    def getConfig(self):
        return {
            "identifiers": self.identifiers,
            "name": self.name,
            "sw_version": self.sw_version,
            "model": self.model,
            "manufacturer": self.manufacturer
        }
    
    def getComponentDiscoveryTopic(self, componentType:str, componentId: str):
        return f"{self.discoveryTopicPrefix}/{componentType}/{self.shortId}/{componentId}/config"

    def getComponentDataTopic(self, componentType:str, componentId: str):
        return f"{self.dataTopicPrefix}/{self.shortId}/{componentType}/{self.manufacturer}/{componentId}"
