from ..__space__ import *

class AMessage(ABC):
    
    @abstractmethod
    def __str__(self) -> str:
        pass