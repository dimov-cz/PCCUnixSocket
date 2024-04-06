import time
import logging
#import EpsonProjCommander
from EpsonProjCommander import EpsonProjCommander

#logging.basicConfig(level=logging.DEBUG)


ep = EpsonProjCommander("192.168.0.18", "EPSONWEB", "")
ep.requestStateOfPower()



i = 0

try:
    while True:
        i = i + 1
        while (r := ep.getResponse()) is not None:
            print(r)
            #if r == "state|PWR|04":
            #    ep.requestPowerOn()
            #if r == "state|PWR|01":
            #    ep.requestPowerOff()

        if i == 10:
            ep.requestInputSource("HDMI1")
            ep.requestColorMode("CINEMA")

        if i % 5 == 0:
            ep.requestStateOfPower()
            ep.requestStateOfSource()
            ep.requestStateOfColorMode()
        time.sleep(1)

except KeyboardInterrupt:
    ep.stop()
    print("Stopped")
