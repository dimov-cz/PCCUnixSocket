from .__space__ import *

import time
import paho.mqtt.client as mqtt
from threading import Thread
from typing import Any, Callable

class MQTTClientConnector(Thread, ALoggable):
    clientId: str
    hostname: str
    port: int
    username: str
    password: str
    mqtt_client: mqtt.Client
    subscribeTopics: list
    messageCallback: Optional[Callable[[mqtt.Client, Any, mqtt.MQTTMessage], None]] = None
    
    sleepPeriod = 0.5 #seconds
    sleepPeriodOnError = 3 #seconds
    connected = False
    exiting = False
    
    def __init__(self, **kwargs) -> None:
        ALoggable.__init__(self)
        Thread.__init__(self, kwargs=kwargs)
    
    def setUp(self, 
              clientId: str, 
              hostname: str = "localhost", 
              port: int = 1883, 
              username: str = "", 
              password: str = "",
              subscribeTopics: list = [],
              messageCallback: Optional[Callable[[mqtt.Client, Any, mqtt.MQTTMessage], None]] = None
    ):
        self.clientId = clientId
        self.hostname = hostname
        self.password = password
        self.username = username
        self.port = port
        self.subscribeTopics = subscribeTopics
        self.messageCallback = messageCallback
        
        self.mqtt_client = mqtt.Client(self.clientId)
        self.mqtt_client.on_connect = self._on_connect
        self.mqtt_client.on_message = self._on_message
        
    def run(self):
        while not self.exiting:
            sleepTime = self.sleepPeriod
                
            if not self.mqtt_client.is_connected():
                try:
                    self.mqtt_client.username_pw_set(self.username, self.password)
                    self.mqtt_client.connect(self.hostname, self.port, 60)
                    #for topic in self.subscribeTopics:
                    #    self.mqtt_client.subscribe(topic)
                    self.mqtt_client.loop_start()
                    self._logger.info(f"Connected to MQTT broker {self.hostname}:{self.port}")
                except Exception as e:
                    self._logger.error(f"Error connecting to MQTT broker: {e}")
                    sleepTime = self.sleepPeriodOnError
                    
            time.sleep(sleepTime)
            
        self._logger.info("Exiting MQTTClientConnector") 
        if self.connected and self.mqtt_client is not None:    
            self.mqtt_client.loop_stop()
            self.mqtt_client.disconnect()
            
    def getConnectedClient(self) -> Optional[mqtt.Client]:
        if self.connected:
            return self.mqtt_client
        return None
    
    def getClient(self) -> mqtt.Client:
        return self.mqtt_client
    
    def isConnected(self) -> bool:
        return self.connected
    
    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            self._logger.debug("Connected to MQTT broker successfully: " + str(flags))
        else:
            self.connected = False
            if rc == 1:
                self._logger.error("Connection refused - incorrect protocol version")
            elif rc == 2:
                self._logger.error("Connection refused - invalid client identifier")
            elif rc == 3:
                self._logger.error("Connection refused - server unavailable")
            elif rc == 4:
                self._logger.error("Connection refused - bad username or password")
            elif rc == 5:
                self._logger.error("Connection refused - not authorised")
            else:
                self._logger.error("Connection refused - unknown error")
            if rc != 3:
                self._logger.error("Unable to connect and probably not recoverable. Exiting...")
                self.exiting = True

    def _on_message(self, client, userdata, msg):
        #self._logger.debug(f"MQTT message received: {msg.topic} {msg.payload}")
        if self.messageCallback is not None:
            self.messageCallback(client, userdata, msg)

    def stop(self):
        self.exiting = True
        