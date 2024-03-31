from ..__space__ import *

class ACommand(ABC):
    
    @abstractmethod
    def __str__(self) -> str:
        pass