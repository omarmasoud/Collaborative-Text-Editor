
import websocket
import threading
import json

class connection_manager:
    def __init__(self):
        self.wsconnectionurl='wss://bp491r2577.execute-api.eu-central-1.amazonaws.com/production'
        self.ws=websocket.create_connection(self.wsconnectionurl)
        # self.receiverthread=threading.Thread(target=self.reciever_function)
        # self.receiverthread.start()

    def reciever_function(self):
        while True:
            resp=self.ws.recv()
            ### todo
            ## process recieved data
            print(resp)
    def BroadCast(self,msg):
        print("going to broadcast this msg")
        print(msg)
        self.ws.send(json.dumps({"action":"updateAll","data":msg}))
    def setname(self,name):
        self.ws.send(json.dumps({"action":"setName","name":name}))
    def setPosition(self,pos):
        self.ws.send(json.dumps({"action":"setPosition","position":pos}))
    def GetDocument(self):
        self.ws.send(json.dumps({"action":"GetDocument"}))

#cm=connection_manager()