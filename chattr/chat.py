from .backend_ollama import _ch_submit_ollama
from os import path
from time import sleep
from socket import socket
from subprocess import Popen, PIPE
from webbrowser import open
from json import dumps

_history = []

def chat(prompt, stream = True, preview = False):
    global _history
    _history.append(dict(role = "user", content = prompt))
    response = _ch_submit_ollama(
        prompt = dumps(_history), 
        stream = stream,
        preview = preview
    )
    _history.append(dict(role = "assistant", content = response))
    return()

def app(host = '127.0.0.1', port = 'auto'):
    
    if port=='auto':
        sock = socket()
        sock.bind(('', 0))
        port = sock.getsockname()[1]

    app_dir = path.dirname(__file__)
    app_file = path.join(app_dir, "app.py")
    
    args = [
    'shiny',
    'run', 
    app_file,
    '--port=' + str(port)
    ]
    Popen(args, stdout= PIPE)

    sleep(1)
    open('http://' + host + ":" + str(port))



