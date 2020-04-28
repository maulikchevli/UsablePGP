#! /usr/bin/env python3.7

import os
import sys
import signal
import subprocess
url = 'http://localhost:8000'

if len(sys.argv) != 2:
    print("usage: <python> startup.py <python>")
    sys.exit(-1)
py_cmd = sys.argv[1]

# https://stackoverflow.com/questions/204017/how-do-i-execute-a-program-from-python-os-system-fails-due-to-spaces-in-path
serverp = subprocess.Popen([py_cmd, "key-server/server.py"], stdout=subprocess.PIPE,
         preexec_fn=os.setsid)
appp = subprocess.Popen([py_cmd, "app/app.py"], stdout=subprocess.PIPE,
         preexec_fn=os.setsid)

import time
time.sleep(2)
p = subprocess.Popen(["python3.7", "-mwebbrowser", url])

print("="*10)
print("Enter 'exit' to Exit all the processes")
ip = ""
while ip != "exit":
    ip = input()

os.killpg(os.getpgid(serverp.pid), signal.SIGTERM)
os.killpg(os.getpgid(appp.pid), signal.SIGTERM)

