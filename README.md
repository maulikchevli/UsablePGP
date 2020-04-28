# UserInterface


## Project Tools
- Python3 (PGPy) as backend for pgp related functions
- html + css + js for front end

## Usage
Install python requirements
```
pip3 install -r requirements.txt
```
Run the script to launch the application. To exit of the loop type 'exit'. (To flexibly use mutiple python3 versions, python command is taken as argument)
```
<python cmd> startup.py <python cmd>
For example:
python3 startup.py python3
```

[startup.py](./startup.py) starts two process:
1. Runs [key-server/server.py](./key-server/server.py) at 5000 port of localhost.
2. Runs [app/app.py](./app/app.py) at 8000 port.

## Architecture
- A server which holds user credentials and their public key (localhost in testing).
- On executing our app, a server process will be created in python and served in browser. Web app acts as front end to the services provided by pgpy

## Restrictions
- A user can only have *single* key pair at any instance.
- User can only created encrypted message for people who have pushed their keys on our server.
