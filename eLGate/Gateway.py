from .__space__ import *

class Gateway:
    
    deviceControllers: DeviceControllerList = DeviceControllerList()
    manageControllers: ManageControllerList = ManageControllerList()
    controlers = []
    
    def __init__(self) -> None:
        pass
    
    def addDeviceController(self, controller: ADeviceController):
        self.deviceControllers.append(controller)
        
    def addManageController(self, controller: AManageController):
        self.manageControllers.append(controller)

