import yaml
import os

class Settings:
    data = None
    def __init__(self, yamlFile):
        self.data = self.loadSettings(yamlFile)
        
    def loadSettings(self, settingsFile):
        pass
        if os.path.exists(settingsFile):
            file_mode = os.stat(settingsFile).st_mode
            # Check if the file is world-readable
            if file_mode & 0o004 == 0o004:
                print(f"{settingsFile} is world-writable! I will not continue. Exiting... And I'm not sorry! :P")
                exit(1)
        else:
            print(f"{settingsFile} does not exist!")

        try:
            with open(settingsFile, 'r') as f:
                return yaml.load(f, Loader=yaml.SafeLoader)
        except Exception as e:
            print("Failed to load settings.yaml: " + str(e))
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
