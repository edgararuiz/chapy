from .backend_ollama import _ch_submit_ollama
from os import path
from time import sleep
import socket
import subprocess
import webbrowser

def chat(prompt, stream = True, preview = False):
    return(
        _ch_submit_ollama(
            prompt = prompt, 
            stream = stream,
            preview = preview
            )
        )

def app(host = '127.0.0.1', port = 'auto'):
    
    if port=='auto':
        sock = socket.socket()
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
    subprocess.Popen(
        args,
        stdout=subprocess.PIPE
        )

    sleep(1)
    webbrowser.open('http://' + host + ":" + str(port))
