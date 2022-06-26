
import websocket
import threading
import json
import time
class connection_manager:
    def __init__(self):
        self.wsconnectionurl='wss://bp491r2577.execute-api.eu-central-1.amazonaws.com/production'
        self.ws = websocket.WebSocket()
        self.ws.connect(self.wsconnectionurl)


    def reciever_function(self):
        while True:
            resp=self.ws.recv()
            ### todo
            ## process recieved data
            print(resp)
    def BroadCast(self,msg,documentStruct="None",documentname="firstDocument"):

        print("going to broadcast this msg")
        print(msg)
        self.ws.send(json.dumps({"action":"updateAll","data":msg,"documentStruct":documentStruct,"docName":documentname}))


    def setname(self,name):
        self.ws.send(json.dumps({"action":"setName","name":name}))
    def setPosition(self,pos):
        self.ws.send(json.dumps({"action":"setPosition","position":pos}))

    def GetDocument(self,name="firstDocument"):
        self.ws.send(json.dumps({"action":"GetDocument","name":name}))

    def GetID(self):
        self.ws.send(json.dumps({"action":"getID"}))

    def SendText(self,txt):
        self.ws.send(json.dumps({"action":"getText","text":txt}))
    def CreateDocument(self,name):
        self.ws.send(json.dumps({"action":"createDocument","name":name}))
    def SendTextDictionary(self,txtDict):
        self.ws.send(json.dumps({"action":"getText","text":txtDict}))

cm=connection_manager()
cm.CreateDocument("omar and ghonaim")
def reciverrr():
    while True:
            resp=cm.ws.recv()
            ### todo
            ## process recieved data
            print(resp)

#cm.GetDocument()
th=threading.Thread(target=reciverrr)
th.start()
# while True:
   
#     cm.GetDocument()
#     time.sleep(10)
