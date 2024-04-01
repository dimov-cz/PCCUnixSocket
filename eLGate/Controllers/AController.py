from ..__space__ import *
from typing import Self

class AController(ALoggable, ABC):

    @abstractmethod
    def factoryBuild(settings: Settings) -> Self:
        pass

    # use to quit all activity befeore exit, especially threads
    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def loop(self):
        pass
    
