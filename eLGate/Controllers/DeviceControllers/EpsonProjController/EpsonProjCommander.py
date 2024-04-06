import time
import random
import logging
from typing import Optional, List

import asyncio
import aiohttp
import threading
import queue

try:
    from .epLocal.epson_projector import Projector
    from .epLocal.epson_projector.error import ProjectorUnavailableError, ProjectorError
    from .epLocal.epson_projector.const import (
        HTTP, BUSY, 
        POWER, PWR_ON, PWR_OFF, PWR_OFF_STATE, PWR_ON_STATE, PWR_GOING_ON_STATE, PWR_GOING_OFF_STATE, 
        SOURCE, SOURCE_LIST, CMODE, CMODE_LIST, CMODE_LIST_SET
    )
except ImportError:
    try:
        #only for local testing
        from epLocal.epson_projector import Projector
        from epLocal.epson_projector.error import ProjectorUnavailableError, ProjectorError
        from epLocal.epson_projector.const import (
            HTTP, BUSY, 
            POWER, PWR_ON, PWR_OFF, PWR_OFF_STATE, PWR_ON_STATE, PWR_GOING_ON_STATE, PWR_GOING_OFF_STATE, 
            SOURCE, SOURCE_LIST, CMODE, CMODE_LIST, CMODE_LIST_SET
        )
    except ImportError:
        logging.getLogger().warn("Using local espon projector lib")
        from epson_projector import Projector
        from epson_projector.error import ProjectorUnavailableError, ProjectorError
        from epson_projector.const import (
            HTTP, BUSY,
            POWER, PWR_ON, PWR_OFF, PWR_OFF_STATE, PWR_ON_STATE, PWR_GOING_ON_STATE, PWR_GOING_OFF_STATE,
            SOURCE, SOURCE_LIST, CMODE, CMODE_LIST, CMODE_LIST_SET
        )

class EpsonProjCommander:
    def __init__(self, host: str, username: str, password: str) -> None:
        self.host = host
        self.username = username
        self.password = password

        self.projector = None
        self.projectorCurrentPowerState = None
        self.websession = None

        self.inProgressProperty = []
        self.inProgressCommand = []
        self.queue = queue.Queue()
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.__internalThread, args=(self.loop,))
        self.thread.start()
        

    def stop(self):
        if self.loop:
            asyncio.run_coroutine_threadsafe(self.__stop(), self.loop).result(5)
            self.loop.call_soon_threadsafe(self.loop.stop)
        self.thread.join()

    def __internalThread(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def __getWebSession(self):
        if self.websession is None:
            self.websession = aiohttp.ClientSession()
        return self.websession

    def __getProjector(self):
        if self.projector is None:
            try:
                self.projector = Projector(
                    type=HTTP,
                    host=self.host,
                    websession=self.__getWebSession(),
                    username=self.username,
                    password=self.password,
                )
            except Exception as e:
                logging.log(logging.ERROR, "Error in __getProjector: " + str(e))
        return self.projector
    
    async def __stop(self):
        if self.projector is not None:
            self.projector.close()
        if self.websession is not None:
            await self.websession.close()
        self.websession = None

    async def async_get_property(self, property_name):
        try:
            logging.log(logging.INFO, "Getting state " + property_name)
            result = BUSY
            while result == BUSY:
                result = await self.__getProjector().get_property(command=property_name)
                if result == "ERR": #error reported by projector, retry
                    result = BUSY
                if result == BUSY:
                    await asyncio.sleep(3)

            if property_name == POWER:
                if result == PWR_ON_STATE:              
                    result = "1,1"
                    self.projectorCurrentPowerState = True
                elif result == PWR_GOING_OFF_STATE:     
                    result = "0,1"
                    self.projectorCurrentPowerState = False
                elif result == PWR_OFF_STATE:           
                    result = "0,0"
                    self.projectorCurrentPowerState = False
                elif result == PWR_GOING_ON_STATE:      
                    result = "1,0" #going up, but not ready
                    self.projectorCurrentPowerState = True
                else:raise Exception("Failed to get power state: " + str(result))

            elif property_name == SOURCE:
                if result in SOURCE_LIST: result = SOURCE_LIST[result]
                else:raise Exception("Failed to get source: " + str(result))

            elif property_name == CMODE:
                if result in CMODE_LIST:  result = CMODE_LIST_SET[CMODE_LIST[result]].replace("CMODE_", '')
                else:raise Exception("Failed to get color mode: " + str(result))

            self.queue.put("state|" + property_name + "=" + str(result))
        except ProjectorUnavailableError as e:
            self.queue.put("state-error|" + property_name + "|" + str(e))
        except Exception as e:
            self.queue.put("state-error|" + property_name + "|" + str(e))
        
        self.inProgressProperty.remove(property_name)

    async def async_send_command(self, command):
        try:
            logging.log(logging.INFO, "Sending command " + command)
            result = False
            while result == False:
                result = await self.__getProjector().send_command(command)
                if result == "ERR": result = BUSY
                if result == False:
                    await asyncio.sleep(1)

            if isinstance(result, aiohttp.ClientResponse) and result.status == 200:
                result = "OK"
            else:
                result = "ERROR"
            self.queue.put("ack|" + command + "|" + str(result))
        except Exception as e:
            self.queue.put("error|command|" + command + "|" + str(e))

        self.inProgressCommand.remove(command)

    def _get_property(self, command):
        if command in self.inProgressProperty:
            return
        self.inProgressProperty.append(command)
        asyncio.run_coroutine_threadsafe(self.async_get_property(command), self.loop)
    
    def _send_command(self, command):
        if command in self.inProgressCommand:
            return
        self.inProgressCommand.append(command)
        asyncio.run_coroutine_threadsafe(self.async_send_command(command), self.loop)

    def requestStateOfPower(self): self._get_property(POWER)
    def requestStateOfSource(self): self._get_property(SOURCE)
    def requestStateOfColorMode(self): self._get_property(CMODE)

    def requestPowerOn(self): 
        if self.projectorCurrentPowerState:
            return
        self._send_command(PWR_ON)
        self.projectorCurrentPowerState = True
    def requestPowerOff(self): 
        if not self.projectorCurrentPowerState:
            return
        self._send_command(PWR_OFF)
        self.projectorCurrentPowerState = False

    def requestInputSource(self, sourceId): self._send_command("SOURCE_" + str(sourceId))
    def requestColorMode(self, colorModeId): self._send_command("CMODE_" + str(colorModeId))


    def getResponse(self):
        # Metoda loop() volaná looperem
        try:
            return self.queue.get_nowait()  # Zkusíme získat výsledek z fronty
        except queue.Empty:
            return None
