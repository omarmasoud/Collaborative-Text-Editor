from concurrent.futures import thread
import threading
import json
from AWSLambdaConnectionManager import connection_manager

cm=connection_manager()
def reciever():
    while True:
        resp=cm.ws.recv()
        resp=json.loads(resp)
        try:
            print(resp["yourID"])
        except:
            print(resp)
mythr=threading.Thread(target=reciever)

mythr.start()



cm.BroadCast("alo")
cm.GetID()

cm.GetID()
cm.GetDocument()