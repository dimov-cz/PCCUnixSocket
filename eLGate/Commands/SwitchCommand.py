from ..__space__ import *

class SwitchCommand(ACommand):
    def __init__(self, 
            device: ProjectorDevice,
            state: bool,
    ):
        self.device = device
        self.state = state

    def __str__(self):
        return f"SwitchCommand({self.device}, {self.state})"