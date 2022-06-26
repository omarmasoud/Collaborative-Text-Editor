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
# i=1
# def sayhello():
#     while True:
#         global i
#         print("hello {}".format(i))
#         i+=1
#         time.sleep(2)

# timethr=threading.Thread(target=sayhello)
# timethr.start()


#### testing updates on dynamodb table
import boto3
import json
dbagent= boto3.resource('dynamodb',region_name='eu-central-1')
t1=dbagent.Table('Collaborative-Text-Editor-Documents')

tcount=dbagent.tables.all()
resp=t1.put_item(
    
    Item={"documentName":"firstDocument",
    "currentVersion":"0",
    "currentDocument":[{"id":1,"pid":2,"cid":3},{"id":1,"pid":2,"cid":3}],
    "versions":[[{"id":1,"pid":2,"cid":3},{"id":1,"pid":2,"cid":3}],[{"id":1,"pid":2,"cid":3},{"id":1,"pid":2,"cid":3}],[{"id":1,"pid":2,"cid":3},{"id":1,"pid":2,"cid":3}]]
    }
       
)
res=t1.update_item(Key={"documentName":"firstDocument"},
    UpdateExpression="SET versions =  :newversion  , currentVersion = :ver , currentDocument = :doc ",
    ExpressionAttributeValues={
        ':newversion': [],
        ":ver":"0",
        ":doc": []
    },
    ReturnValues="UPDATED_NEW"

)
t1.put_item(Item={
                "documentName":"docName",
                "currentVersion":"0",
                "currentDocument":[],
                "versions":[]
                }
                )
res=t1.get_item(Key={"documentName":"docName"})
print (res['Item']['currentVersion'])