from ....__space__ import *

import time
import paho.mqtt.client as mqtt

class MQTTClientController(AManageController):
    def __init__(self, clientId: str, username: str = "", password: str = ""):
        super().__init__()
        self.clientId = clientId
        self.mqtt_client = mqtt.Client(clientId)
        self.mqtt_client.username_pw_set(username, password)
        self.mqtt_client.connect("localhost", 1883, 60)
        
        self.mqtt_client.on_connect = self._on_connect
        self.mqtt_client.on_message = self._on_message
        self.mqtt_client.loop_start()
        
    def ensureConnected(self):
        while not self.mqtt_client.is_connected():
            self.logger.info("Connecting to MQTT broker...")
            time.sleep(0.1)
            
    def stop(self):
        self.mqtt_client.loop_stop()
        
    def getClient(self):
        return self.mqtt_client
        
    def _on_connect(self, client, userdata, flags, rc):
        self.logger.info(f"Connected to MQTT broker with result code {rc}")
        self.mqtt_client.subscribe("homeassistant/#")
        
    def _on_message(self, client, userdata, msg):
        self.logger.debug(f"Received message on topic {msg.topic}: {msg.payload}")
        
    def processAnnouncement(self, device: ACDevice):
        info = device.getDeviceInfo()
        self.logger.info(f"Processing announce: {device} {info}")