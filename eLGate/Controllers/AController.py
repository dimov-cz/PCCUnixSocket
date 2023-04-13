from ..__space__ import *


class AController(ABC):
    
    logger: logging.Logger
    
    def __init__(self) -> None:
        self.initLogger()
        
    def initLogger(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.setLogLevel(logging.INFO)
        
    def setLogLevel(self, level):
        self.logger.setLevel(level)
    
    @abstractmethod
    def processAnnouncement(self, device: ACDevice):
        pass
