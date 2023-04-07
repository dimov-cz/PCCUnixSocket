import time
from Settings import Settings
from UnixSocketTool import UnixSocketServer
from PccCommander import PccCommander as PccCommanderDaemon
import json
from enum import Enum
import threading

settingsFile = 'settings.yaml'
defaultSocketFile = '/tmp/pcc.sock'
defaultTokensPathPrefix = '~/pcc-'
loopSleepTime = 0.1 #seconds

class JSONEnumsEncoder(json.JSONEncoder):
    def default(self, obj):
        if issubclass(obj.__class__, Enum):
            #return "{value{obj.name}:{obj.value}"
            return {"str": obj.name, "int": obj.value}
        return super().default(obj)        


settings = Settings(settingsFile)

socketServer = UnixSocketServer(settings.get('socket', defaultSocketFile))
socketServer.open()
print(f"Listening on {socketServer.socket_file}...")

tokensPathPrefix = settings.get('tokensPathPrefix', defaultTokensPathPrefix)
pcc = PccCommanderDaemon(settings.get('mainAccount.login'), settings.get('mainAccount.password'), tokensPathPrefix + 'main')

#registration of subaccounts is time consuming and it's not neccessary to be done immediately:
def registerSubAccount():
    for account in settings.get('subAccounts', []):
        pcc.addSubAccount(account['login'], account['password'], tokensPathPrefix + account['login'])
        
if settings.get('delayedSubAccountsRegistration', False):
    threading.Thread(target=registerSubAccount).start()
else:
    registerSubAccount()


autoUpdateTime = settings.get('autoUpdate', 0)
print(f"autoUpdateTime={autoUpdateTime}")
lastUpdate = 0

# accept incoming connections
while True:
    socketServer.serviceLoop()
    
    # 1) read from clients
    client, msg = socketServer.read()
    while client is not None:
        
        try:
            print(f"Received: {msg} from #{client.fileno()}")

            tokens = msg.strip().split()
            if (len(tokens) == 0):
                raise Exception("Empty command.")

            # Call the appropriate method on the device control object
            if tokens[0] == "list":
                pcc.fireCommand("all", "list")
            elif tokens[0] == "status":
                pcc.fireCommand("all" if len(tokens) == 1 else tokens[1], "status")
            elif tokens[0] in ["setpower", "setmode", "settemp"]:
                if len(tokens) == 3:
                    pcc.fireCommand(tokens[1], tokens[0], tokens[2])
                else:
                    raise Exception(f"Missing arguments for {tokens[0]}.")
            else:
                raise Exception(f"Unknown command: {tokens[0]}")

        except Exception as e:
            print(f"Error: {e}")
            d = {
                'commandId': 0,
                'deviceId': None,
                'type': 'error',
                'data': str(e)
            }
            socketServer.writeAll(json.dumps(d, cls=JSONEnumsEncoder) + "\n")
        
        #next:
        client, msg = socketServer.read()
        
    # 2) auto update check
    if autoUpdateTime > 0:
        if time.time() - lastUpdate > autoUpdateTime:
            lastUpdate = time.time()
            pcc.fireCommand("all", "status")

    # 3) read from PCC
    response = pcc.getResponse()
    while response is not None:
        d = {
            'commandId': response.commandId,
            'deviceId': response.acDevice.getDeviceInfo().deviceId if response.acDevice is not None else None,
            'type': response.type,
            'data': response.data
        }
        socketServer.writeAll(json.dumps(d, cls=JSONEnumsEncoder) + "\n")
        #next:
        response = pcc.getResponse()
        
    
    time.sleep(loopSleepTime)

conn.close()

