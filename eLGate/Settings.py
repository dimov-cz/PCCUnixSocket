from typing import Optional
import yaml
import os
import logging

class Settings:
    data = None
    def __init__(self, yamlFile: Optional[str] = None, data = None):
        if yamlFile is None and data is None:
            raise Exception("Either yamlFile or data must be set!")
        if yamlFile is not None and data is not None:
            raise Exception("Either yamlFile or data must be set, not both!")   
        if yamlFile is not None:
            self.data = self.loadSettings(yamlFile)
        else:
            self.data = data
        
    def loadSettings(self, settingsFile):
        pass
        if os.path.exists(settingsFile):
            file_mode = os.stat(settingsFile).st_mode
            # Check if the file is world-readable
            if file_mode & 0o004 == 0o004:
                logging.critical(f"{settingsFile} is world-readable! I will not continue. Exiting... And I'm not sorry! :P")
                exit(1)
        else:
            logging.warning(f"{settingsFile} does not exist!")

        try:
            with open(settingsFile, 'r') as f:
                return yaml.load(f, Loader=yaml.SafeLoader)
        except Exception as e:
            logging.critical(f"Failed to load {settingsFile}: {e}")
            exit(1)
            
    def _get(self, currentData, keyParts, default):
        
        if len(keyParts) == 1:
            if keyParts[0] in currentData:
                return currentData[keyParts[0]]
            else:
                return default
        else:
            if keyParts[0] in currentData:
                return self._get(currentData[keyParts[0]], keyParts[1:], default)
            else:
                return default
            
    def get(self, key, default=None):
        keyParts = key.split('.')
        return self._get(self.data, keyParts, default)
    
    def getString(self, key, default = "") -> str:
        value = self.get(key, None)
        if value is None:
            return default
        if not isinstance(value, str):
            raise Exception(f"Value for {key} is not a string!")
        return value
    
    def getInt(self, key, default = 0) -> int:
        value = self.get(key, None)
        if value is None:
            return default
        if (not isinstance(value, int)):
            raise Exception(f"Value for {key} is not an integer! It's a {type(value)}")
        return value
    
    def getBool(self, key, default = False) -> bool:
        value = self.get(key, None)
        if value is None:
            return default
        if (not isinstance(value, bool)):
            raise Exception(f"Value for {key} is not a boolean! It's a {type(value)}")
        return value

    def getList(self, key, default = []) -> list:
        value = self.get(key, default)
        if (not isinstance(value, list)):
            raise Exception(f"Value for {key} is not a dictionary! It's a {type(value)}")
        return value
    
    def getDict(self, key, default = {}) -> dict:
        value = self.get(key, default)
        if (not isinstance(value, dict)):
            raise Exception(f"Value for {key} is not a dictionary! It's a {type(value)}")
        return value
        result = {}
        for item in self.getList(key, []):
            result.update(item)
        return result
