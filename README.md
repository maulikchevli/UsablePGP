# UserInterface


## Project Tools
- Python (PGPy) as backend for pgp related functions
- html + css + js for front end

## Architecture
- A server which hols user credentials and their public key (localhost in testing)
- On executing our app, a server process will be created in python and served in browser. Web app acts as front end to the services provided by pgpy

## Restrictions
- A user can only have *single* key pair at any instance.
- User can only created encrypted message for people who have pushed their keys on our server.
