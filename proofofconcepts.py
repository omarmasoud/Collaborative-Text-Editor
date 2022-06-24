from concurrent.futures import thread
import threading
from AWSLambdaConnectionManager import connection_manager

cm=connection_manager()
def reciever():
    while True:
        resp=cm.ws.recv()
        print(resp)
mythr=threading.Thread(target=reciever)

mythr.start()



cm.BroadCast("alo")
cm.GetDocument()