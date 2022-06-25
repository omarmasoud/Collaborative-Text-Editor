from concurrent.futures import thread
from socket import timeout
import threading
import json
import time
from AWSLambdaConnectionManager import connection_manager
#############################################
# testing connection manager APIs
# cm=connection_manager()
# def reciever():
#     while True:
#         resp=cm.ws.recv()
#         resp=json.loads(resp)
#         try:
#             print(resp["yourID"])
#         except:
#             print(resp)
# mythr=threading.Thread(target=reciever)

# mythr.start()



# cm.BroadCast("alo")

# cm.GetID()

# cm.GetDocument()

####################################
## testing 
i=1
def sayhello():
    while True:
        global i
        print("hello {}".format(i))
        i+=1
        time.sleep(2)

timethr=threading.Thread(target=sayhello)
timethr.start()