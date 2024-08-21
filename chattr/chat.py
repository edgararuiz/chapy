from .backend_ollama import _ch_submit_ollama
from os import path, _exists
from time import sleep
from socket import socket
from subprocess import Popen, PIPE
import webbrowser
from json import dumps, loads
from tempfile import NamedTemporaryFile

_history_file = NamedTemporaryFile().name
_history = []

def chat(prompt, stream = True, preview = False, **kwargs):
    global _history
    global _history_file
    hf = kwargs.get("_history_file")
    if isinstance(hf, str):
        _history_file = hf
        if _exists(_history_file):
            _history = loads(open(_history_file, "r").read())

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



