import logging
import sys
import os

print("__main__ entered")

#early logging setup:
loggingHandler = logging.StreamHandler(sys.stdout)
logging.basicConfig(
    format='%(asctime)s - %(levelname)s@%(name)s - %(message)s', 
    handlers=[loggingHandler]
)
if int(os.environ.get('DEBUG', '0')) > 0: #works as global filter for all loggers
    loggingHandler.setLevel(logging.DEBUG)
else:
    loggingHandler.setLevel(logging.INFO)
    
if int(os.environ.get('DEBUG', '0')) == 3: #global logger level
    logging.getLogger().setLevel(logging.DEBUG)
    
    
from .__space__ import *
from .Gateway import Gateway

import time
import json
import threading
import signal

#hass_mqtt_device.logger.addHandler(loggingHandler)
class JSONInnerEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj.__class__, '__json__'):
            return obj.__class__.__json__(obj)
        return super().default(obj)        


class SignalCatcher:
    intReceived = False
    termReceived = False
    
    def __init__(self):
        signal.signal(signal.SIGINT, self._signal_int)
        signal.signal(signal.SIGTERM, self._signal_term)
        signal.signal(signal.SIGPIPE, signal.SIG_DFL) #ignore errors on broken pipe to avoid raising exceptions
    
    def stop(self):
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    
    def _signal_int(self, sig, frame):
        self.intReceived = True
        
    def _signal_term(self, sig, frame):
        self.termReceived = True
        
    def noSignalReceived(self):
        return not (self.intReceived or self.termReceived)


def main():
    print("main")

    settingsFile = 'settings.yaml'
    defaultSocketFile = '/tmp/pcc.sock'
    defaultTokensPathPrefix = '~/pcc-'
    loopSleepTime = 1 #seconds

    settings = Settings(settingsFile)

    from .Controllers.ManageControllers.MQTTController.MQTTClientManageController import MQTTClientManageController
    mqttController = MQTTClientManageController(
        hostname=settings.getString('mqtt.host', 'localhost'),
        port    =settings.getInt(   'mqtt.port', 1883),
        clientId=settings.getString('mqtt.id',   "eLGate"),
        username=settings.getString('mqtt.login'),
        password=settings.getString('mqtt.password')
    )
    
    from .Controllers.DeviceControllers.PanasonicComfortCloudController.PanasonicComfortCloudDeviceController import PanasonicComfortCloudDeviceController
    pccController = PanasonicComfortCloudDeviceController(Settings(data = settings.get('pcc')))

    sc = SignalCatcher()

    gateway = Gateway()
    gateway.addManageController(mqttController)
    gateway.addDeviceController(pccController)
    
    # accept incoming connections
    exiting = False
    while sc.noSignalReceived() and not exiting:
        try:
            #print("loop")
            gateway.loop()
            loggingHandler.flush()
            time.sleep(loopSleepTime)
        except Exception as e:
            logging.error(f"Error in main loop: {e}")
            exiting = True
            sc.stop()
            raise e
            
            

    logging.info("Exiting...")
    mqttController.stop()
    pccController.stop()
    logging.info("Exiting... done")
