
#from .__space__ import *
from abc import ABC, abstractmethod
import logging

from .Gateway import Gateway
from .Settings import Settings
from .Controllers.AController import AController
from .Controllers.DeviceControllers.ADeviceController import ADeviceController
from .Controllers.DeviceControllers.DeviceControllerList import DeviceControllerList
from .Controllers.ManageControllers.AManageController import AManageController
from .Controllers.ManageControllers.ManageControllerList import ManageControllerList

import time
import json
import threading

#hass_mqtt_device.logger.addHandler(loggingHandler)

settingsFile = 'settings.yaml'
defaultSocketFile = '/tmp/pcc.sock'
defaultTokensPathPrefix = '~/pcc-'
loopSleepTime = 0.1 #seconds

class JSONInnerEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj.__class__, '__json__'):
            return obj.__class__.__json__(obj)
        return super().default(obj)        


settings = Settings(settingsFile)

from .Controllers.ManageControllers.MQTTController.MQTTClientManageController import MQTTClientController
mqttController = MQTTClientController(
    settings.getString('mqtt.id', "PCCGateway"),
    settings.getString('mqtt.login'),
    settings.getString('mqtt.password')
)
mqttController.setLogLevel(logging.DEBUG)

gateway = Gateway()
gateway.addManageController(mqttController)

# accept incoming connections
while True:
        
    loggingHandler.flush()
    time.sleep(loopSleepTime)

mqttController.stop()
conn.close()

