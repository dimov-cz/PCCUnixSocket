import logging
import sys
import os

print("INIT")

#early logging setup:
loggingHandler = logging.StreamHandler(sys.stdout)
logging.basicConfig(
    format='%(asctime)s - %(levelname)s@%(name)s - %(message)s', 
    handlers=[loggingHandler]
)
if int(os.environ.get('DEBUG', '0')) > 0: #works as global filter for all loggers
    loggingHandler.setLevel(logging.DEBUG)
else:
    loggingHandler.setLevel(logging.INFO)
    
if int(os.environ.get('DEBUG', '0')) == 3: #global logger level
    logging.getLogger().setLevel(logging.DEBUG)
    
