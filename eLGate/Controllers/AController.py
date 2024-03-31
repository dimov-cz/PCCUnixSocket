from ..__space__ import *


class AController(ALoggable, ABC):
    

    # use to quit all activity befeore exit, especially threads
    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def loop(self):
        pass
    
