ECHO OFF
ECHO setting up virtual python environment
python -m venv venv
ECHO installing requirements.txt
venv\scripts\python.exe -m pip install -r requirements.txt
ECHO installing ttkbootstrap
venv\scripts\python.exe -m pip install -e .
ECHO ttkbootstrap environment setup is complete
venv\scripts\python.exe -m pip install awscli .
ECHO AWS CLI environment setup is complete