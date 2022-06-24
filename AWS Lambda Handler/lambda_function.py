import json
import urllib3
import boto3#python apis for AWS resources
import os
import sys
import subprocess
import random

# pip install custom package to /tmp/ and add to path
subprocess.call('pip install names -t /tmp/ --no-cache-dir'.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# subprocess.call('pip install decimal -t /tmp/ --no-cache-dir'.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# from decimal import Decimal #for decimal objects of dynamo db

sys.path.insert(1, '/tmp/')
#importing random name generator
import names
# validating import
print("this is an import validation message, please ignore")
print(names.get_full_name())
apigatewayUrl='https://bp491r2577.execute-api.eu-central-1.amazonaws.com/production/'
client=boto3.client('apigatewaymanagementapi',endpoint_url=apigatewayUrl)

connections=list()
currconection=None# placeholder for new connection
NamesDict={}
serverLastRecievedChangeTimeStamp=0


#Custom json encoder to avoid json errors with Dynamodb Decimal types
# class JSONEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, Decimal):
#             return float(obj)
#         return json.JSONEncoder.default(self, obj)



class DbConnectionManager:
    def __init__(self):
        self.dbagent= boto3.resource('dynamodb',region_name='eu-central-1')#initializing dynamodb object
        try:
            self.t1=self.dbagent.Table('Collaborative-Text-Editor-Data')#primary dynamodb table
        except:
            self.t1=None
            print("couldn't reference table 1")
            
        try:
            print("will fill later")
            #self.t2=self.dbagent.Table('collaborativedump')#primary dynamodb table
        except:
            self.t2=None
            print("couldn't reference table 2")
        self.t2=self.dbagent.Table('collaborativedump')#eplica table to be changed when creating replica
        self.table1down=False# value to be set when a table is down to replicate when it is up and running again
        self.table2down=False
        
    def insert_to_db(self,item):
        try:
            self.t1.put_item(Item=item)
            #self.t2.put_item(Item=item)#inserting to replica
            self.table1down=False
        except:
            self.table1down=True
        try:
           # self.t2.put_item(Item=item)
            #self.t2.put_item(Item=item)#inserting to replica
            self.table2down=False
        except:
            self.table2down=True
        pass
    def remove_from_db(self,partKey):
        try:
            self.t1.delete_item(Ket=partKey)
            #self.t2.put_item(Item=item)#inserting to replica
            self.table1down=False
        except:
            self.table1down=True
        try:
           # self.t2.delete_item(Ket=partKey)
            #self.t2.put_item(Item=item)#inserting to replica
            self.table2down=False
        except:
            self.table2down=True
        pass
    def retreive_from_db(self,key):
        self.t1.get_item(Key=key)
        try:
            self.t1.get_item(Key=key)
            #self.t2.put_item(Item=item)#inserting to replica
            self.table1down=False
        except:
            self.table1down=True
        try:
           # self.t2.get_item(Key=key)
            #self.t2.put_item(Item=item)#inserting to replica
            self.table2down=False
        except:
            self.table2down=True
        
    def scan_db(self):
        
        scanlst=None
        
        try:
           # scanlst=self.t2.scan()
            #self.t2.put_item(Item=item)#inserting to replica
            self.table2down=False
        except:
            self.table2down=True
        try:
            scanlst=self.t1.scan()
            #self.t2.put_item(Item=item)#inserting to replica
            self.table1down=False
        except:
            self.table1down=True
            
            
        return list(scanlst['Items'])
        
        pass
    
    
db_connection_manager=DbConnectionManager()

def lambda_handler(event, context):
    
    connectionId=event['requestContext']['connectionId']
    routeKey=event['requestContext']['routeKey']
    
    #on calling updateAll action for broadcasting a new change
    if routeKey =='updateAll':
        print('available connections are')
        print(NamesDict)
        body=event['body']
        body=body.replace("'", "\"")
        body=json.loads(body)
        #recepientname=body['receiver']
        #print('recepient of name {} has id {}'.format(recepientname,NamesDict[recepientname]))
        
        #retrieving body data as msg to be broadcasted (document change)
        msgdata=body['data']
        #client.post_to_connection(ConnectionId=NamesDict[recepientname],Data=json.dumps(msgdata).encode('utf-8'))
        print("character data is {}".format(body['data']))
        #broadcasting change activity to all connections
        broadcast(msgdata,connectionId)
        
        #logging change activity into database
        db_connection_manager.insert_to_db({"charid":names.get_full_name(),"data":names.get_full_name(),"delta": msgdata})
        # trying to broadcast all datbase entries
        #dblistentries=db_connection_manager.scan_db()
        #print(dblistentries[1]["charid"])
        #temp=json.dumps({"entries":dblistentries})
        #broadcast(dblistentries,connectionId)
        #sendto(NamesDict[recepientname],msgdata)
        
    ## on new user connecting
    elif routeKey =='$connect':
        print('somebody connected wow')
        connections.append(connectionId)
        currconection=connectionId
        #Generate Random Name for new Connection,set initial cursor position at 0 
        NamesDict[connectionId]=[names.get_full_name(),0]
        notifymsg='{} has joined the session'.format(connectionId)
        print(notifymsg)
        print('event is  ')
        print(event)
        #broadcast(json.dumps(notifymsg))
    ##Custom Set Name for a connection
    elif routeKey =='setName':
        print('new name entered')
        body=event['body']
        body=body.replace("'", "\"")
       
        body=json.loads(body)
        NamesDict[connectionId][0]=body['name']
        #broadcast("{} has joined say hello".format(body['name']))
    elif routeKey =='setPosition':
        
        
        print('new name Position entered')
        body=event['body']
        body=body.replace("'", "\"")
        body=json.loads(body)
        NamesDict[connectionId][1]=body['position']
        
    elif routeKey=='GetDocument':
        
        dblistentries=db_connection_manager.scan_db()
        #print(dblistentries[1]["charid"])
        sendMsgToConnection(connectionId,dblistentries)
        print("document sent to connection {}".format(NamesDict[connectionId]))
        
    elif routeKey =='$disconnect':
        
        print('disconnecting now from connection {} '.format(connectionId))
        #print(event)
        currconn=event['requestContext']['connectionId']
        if currconn in connections:
            print('connection was already there at {}'.format(connections.index(currconn)))
        else:
            print(currconn)
            print(connections)
        
        try:
            NamesDict.pop(currconn)
            connections.remove(currconn)
        except:
            print('no name for connection {}'.format(currconn))

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
    
    

def sendto(Name,Data):
    msgtobesent={
    "freeze": "false",
    "delta":Data,
    "numusers":len(connections),
    "Userslocations" :json.dumps(list(NamesDict.values()))
    }
    client.post_to_connection(ConnectionId=str(NamesDict[Name]),Data=json.dumps(msgtobesent).encode('utf-8'))

def sendMsgToConnection(uniqueConnection,Data):
    client.post_to_connection(ConnectionId=str(uniqueConnection),Data=json.dumps(Data).encode('utf-8'))
    
    
def broadcast(Data,sender):
    #currconn=event['requestContext']['connectionId']
    msgtobesent={
    "freeze": "false",
    "delta":Data,
    "numusers":len(connections),
    "Userslocations" : json.dumps(list(NamesDict.values()))
    }
    for currentConnection in connections:
        if currentConnection != sender:
            try:
                client.post_to_connection(ConnectionId=currentConnection,Data=json.dumps(msgtobesent).encode('utf-8'))
            except:
                pass
            #sendto(connectionId=currentConnection,Data=Data)
            