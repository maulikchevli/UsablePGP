# UsablePGP
Making PGP usable again!
A simple and intuitive to use [PGP](https://en.wikipedia.org/wiki/Pretty_Good_Privacy) application.
- It is simple to use.
- It is flexible. It is usable for all email providers.
- Runs all computation locally on the machine. Hence, it is end-to-end secure [unlike In-Browser Cryptography](https://tonyarcieri.com/whats-wrong-with-webcrypto). More on this [here](https://security.stackexchange.com/questions/173620/what-s-wrong-with-in-browser-cryptography-in-2017).

## Tools used
- Python3: [PGPy](https://github.com/SecurityInnovation/PGPy) as backend for pgp related functions, [flask](https://github.com/pallets/flask/) for web UI controller and Key server APIs.
- html + css + js for front end

## Usage
Install python requirements
```
pip3 install -r requirements.txt
```

### For Unix-like systems
Run the script to launch the application. To exit of the loop type 'exit'. (To flexibly use mutiple python3 versions, python command is taken as argument)
```
<python cmd> startup.py <python cmd>
For example:
python3 startup.py python3
```
[startup.py](./startup.py) starts two process:
1. Runs [key-server/server.py](./key-server/server.py) at 5000 port of localhost.
2. Runs [app/app.py](./app/app.py) at 8000 port.

### For windows
Double click start.bat file.

## Architecture
- A server which holds user credentials and their public key (localhost in testing).
- Python (flask) backend to serve Frontend.
- On executing our app, a server process will be created in python and UI will be served in browser. Web app acts as front end to the services provided by flask and pgpy.

## Restrictions
- A username/email can only have *single* key pair at any instance.
- User can only created encrypted message for people who have registered on our server.

## Future extensions
- Verifying users' email address to sign public key for web of trust
- Provide secure backup option
