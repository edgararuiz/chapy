from .backend_ollama import _ch_submit_ollama
from os import path
from time import sleep
from socket import socket
from subprocess import Popen, PIPE
import webbrowser
from json import dumps
from tempfile import NamedTemporaryFile

_history_file = NamedTemporaryFile().name
_history = []

def chat(prompt, stream = True, preview = False):
    global _history
    global _history_file
    _history.append(dict(role = "user", content = prompt))
    response = _ch_submit_ollama(
        prompt = dumps(_history), 
        stream = stream,
        preview = preview
    )
    _history.append(dict(role = "assistant", content = response))
    open(_history_file, "w").write(dumps(_history))

def app(host = '127.0.0.1', port = 'auto'):
    global _history_file

    if port=='auto':
        sock = socket()
        sock.bind(('', 0))
        port = sock.getsockname()[1]

    app_file = path.join(path.dirname(__file__), "app.py")
    
    py_script  = open(app_file, "r").read()
    py_script = "_history_file = '"+ _history_file + "'\n" + py_script
    temp_script = NamedTemporaryFile()
    temp_script = str(temp_script.name) + '.py' 
    open(temp_script, "w").write(py_script)

    args = ['shiny', 'run', temp_script, '--port=' + str(port)]
    Popen(args, stdout= PIPE)
    
    sleep(1)
    webbrowser.open('http://' + host + ":" + str(port))



