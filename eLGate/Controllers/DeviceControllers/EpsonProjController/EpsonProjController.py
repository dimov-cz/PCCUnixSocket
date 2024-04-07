from eLGate.__space__ import ProjectorCommand, Settings
from ....__space__ import *
import time
from typing import Self

from .EpsonProjCommander import EpsonProjCommander



class EpsonProjController(ADeviceController):
    autoUpdateTime: float
    lastUpdateStart: float

    def __init__(self, settings: Settings) -> None:
        super().__init__()
        self.projector = EpsonProjCommander(
            host = settings.getString('host', 'localhost'),
            username = settings.getString('username', None), # default is 'EPSONWEB' if used by this firmware
            password = settings.getString('password', ""),
        )

        self.projectorID = settings.getString('ID', 'EpsonProj_01')
        self.projectorName = settings.getString('name', 'Projector')
        self.sourcesList = settings.getList('sources', [ "HDMI1", "HDMI2", "LAN", "WFD" ])
        self.colorModesList = settings.getList('color_modes', [ "CINEMA", "BRIGHT" ])

        self.sendMessage(
            NewDeviceMessage(
                ProjectorDevice(
                    self.projectorID,
                    self.projectorName,
                    "",
                    "Epson",
                    self.sourcesList,
                    self.colorModesList,
                )
            )
        )

        self.autoUpdateTime = 10
        self.lastUpdateStart = 0

        self.projector.requestStateOfPower()
        self.projector.requestStateOfSource()
        self.projector.requestStateOfColorMode()


    def loop(self):
        while (response := self.projector.getResponse()) != None:
            self._logger.debug("Raw msg: '" + str(response) + "'")
            responseType, responseValue = response.split('|', maxsplit=1)
            if responseType == "state":
                stateKey, stateValue = responseValue.split('=', maxsplit=1)
                if stateKey == "PWR":
                    powerIsON, readyState = stateValue.split(',')
                    self.sendMessage(
                        ProjectorStateMessage(
                            deviceId= self.projectorID,
                            available= True,
                            availableSettings= True if int(powerIsON) else False,
                            power= True if int(powerIsON) else False,
                            ready= True if int(readyState) else False,
                        )
                    )
                elif stateKey == "SOURCE":
                    self.sendMessage(
                        ProjectorStateMessage(
                            deviceId= self.projectorID,
                            source= stateValue
                        )
                    )
                elif stateKey == "CMODE":
                    self.sendMessage(
                        ProjectorStateMessage(
                            deviceId= self.projectorID,
                            colorMode= stateValue
                        )
                    )
                else:
                    self._logger.error("Unknown state key: '" + str(stateKey) + "'")
            elif responseType == "ack":
                commandAck, valueAck = responseValue.split('|', maxsplit=1)
                if valueAck == "OK":
                    if commandAck == "PWR ON" or commandAck == "PWR OFF":
                        self.sendMessage(
                            ProjectorStateMessage(
                                deviceId= self.projectorID,
                                power= commandAck == "PWR ON",
                            )
                        )
                    elif commandAck.startswith("SOURCE_"):
                        self.sendMessage(
                            ProjectorStateMessage(
                                deviceId= self.projectorID,
                                source= commandAck.split('_', maxsplit=1)[1]
                            )
                        )
                    elif commandAck.startswith("CMODE_"):
                        self.sendMessage(
                            ProjectorStateMessage(
                                deviceId= self.projectorID,
                                colorMode= commandAck.split('_', maxsplit=1)[1]
                            )
                        )
                    else:
                        self._logger.info("Unknown OK ack: '" + str(commandAck) )
                else:
                    self._logger.info("Unknown ack: '" + str(commandAck) + " - " + str(valueAck) )
            else:
                self._logger.error("Unknown response type: '" + str(responseType) + "'")

        if self.lastUpdateStart + self.autoUpdateTime < time.time():
            self.lastUpdateStart = time.time()
            self.projector.requestStateOfPower()
            self.projector.requestStateOfSource()
            self.projector.requestStateOfColorMode()

    def processProjectorCommand(self, command: ProjectorCommand):
        if (command.power is not None):
            if command.power == True:
                self.projector.requestPowerOn()
            else:
                self.projector.requestPowerOff()
        if (command.source is not None):
            self.projector.requestInputSource(command.source)
        if (command.colorMode is not None):
            self.projector.requestColorMode(command.colorMode)

    
    def stop(self):
        self.projector.stop()
        
    
    def factoryBuild(settings: Settings) -> Self:
        return EpsonProjController(settings)