from .__space__ import *

class Gateway(ALoggable):
    
    deviceControllers: DeviceControllerList = DeviceControllerList()
    manageControllers: ManageControllerList = ManageControllerList()
    controlers = []
    
    def __init__(self) -> None:
        ALoggable.__init__(self)
        
    def addDeviceController(self, controller: ADeviceController):
        self.deviceControllers.append(controller)
        
    def addManageController(self, controller: AManageController):
        self.manageControllers.append(controller)

    def loop(self):
        
        if len(self.deviceControllers) == 0:
            self._logger.warning("No device controller added, u are missing settings or the point")

        for controller in self.deviceControllers:
            controller.loop()
            for message in iter(controller.popMessage, None):
                self._logger.debug(f"Delivering message: {message}")
                for manageController in self.manageControllers:
                    if isinstance(message, NewDeviceMessage):
                        manageController.processNewDevice(message)
                    elif isinstance(message, ClimateStateMessage):
                        manageController.processClimateState(message)
                    else:
                        self._logger.error(f"Unknown message type: {message}")
                    
        if len(self.manageControllers) == 0:
            self._logger.warning("No manage controller added, u are missing settings or the point")
            
        for controller in self.manageControllers:
            controller.loop()
            for command in iter(controller.popCommand, None):
                self._logger.debug(f"Delivering command: {command}")
                for deviceController in self.deviceControllers:
                    if isinstance(command, ClimateCommand):
                        deviceController.processClimateCommand(command)
                    else:
                        self._logger.error(f"Unknown command type: {command}")
    def stop(self):
        for controller in self.deviceControllers:
            controller.stop()
        for controller in self.manageControllers:
            controller.stop()
