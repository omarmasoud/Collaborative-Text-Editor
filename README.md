# Collaborative-Text-Editor
## This is a course Project by team 38 for Distributed Computing Course CSE 354 Faculty of Engineering Ain Shams University
### Team Members:
* Omar Khaled Mahmoud Mohamed	18P3067
* Mohamed Amr Mohamed Ghonaim	18P2783
* Bishoy Hany Kamel Mikhael	1807854
#### Discription:
this is a collaborative text editor developed by tkinter GUI for frontend  AWS Lambda,DynamoDB,API GateWay for Backend Services, CRDT (Conflict-free replicated data type)
logic for Conflict resolution 
---------------------------------------
#### in order to run the project there is a setup_project.bat file you can run as long as you have python 3 and pip 3 on your machine, this batch file will install requirements in requirements.txt file
#### you can also use pip install -r requirements.txt
#### next to launch the project if you have your lambda instance up and running you just open txtedtr.py file and you will get navigated to the GUI
---------------------------------------
*initially you will be set to no document, but you can create documents or navigate to documents on database by the last two buttons on the left pannel*
*the label below will let you view number of users using this document and editing it and the other buttons let you open new document and create node structure for it using crdt*
---------------------------------------
the provided .yaml files are **infrastructure as a code for AWS backend** you will have to use AWS cloud formation to deploy it or through AWS CLI
*installation batch files might be provided later due to timing constraints*
