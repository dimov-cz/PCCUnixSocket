from ..__space__ import *
import inspect

class ALoggable(ABC):
    _logger: logging.Logger
    
    def __init__(self) -> None:
        self.__initLogger()
        
    def __initLogger(self):
        loggerId = self.__class__.__name__
        logLevel = logging.DEBUG #no limit by default
        
        caller = self.__get_caller()
        #print(self.__class__.__name__ + " -> " + str(caller.__class__.__name__) + str(caller))
        caller = None
        if isinstance(caller, ALoggable):
            loggerId += "|" + caller._getLoggerId()
            logLevel = caller.getLogLevel()
        elif caller:
            loggerId += "|" + str(self.__qualname__)  # type: ignore
        
        self._logger = logging.getLogger(loggerId)
        self.setLogLevel(logLevel)
        
        
    def _getLoggerId(self):
        return self._logger.name
        
    def setLogLevel(self, level):
        self._logger.setLevel(level)
        
    def getLogLevel(self):
        return self._logger.level
            
    def __get_caller(self):
        stack = inspect.stack()
        for frame in stack:
            method_name = frame[3]
            calling_obj = frame[0].f_locals.get('self', None)
            if calling_obj and isinstance(calling_obj, type):
                # Class method or static method
                return calling_obj
            elif calling_obj:
                # Instance method
                if calling_obj.__class__.__name__ == self.__class__.__name__:
                    continue
                return calling_obj
            elif method_name == '<module>':
                # Top-level module
                return None
        return None