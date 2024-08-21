from .backend_ollama import _ch_submit_ollama, _ch_models_ollama
from .utils import _ch_open_config
from os import path, _exists
from time import sleep
from socket import socket
from subprocess import Popen, PIPE
import webbrowser
from json import dumps, loads
from tempfile import NamedTemporaryFile

_history_file = NamedTemporaryFile().name
_default_file = NamedTemporaryFile().name
_shiny_url = ''
_history = []

def use(provider = '', **kwargs):
    global _default_file
    if not _exists(_default_file):
        defaults = _ch_open_config("ollama")
        open(_default_file, "w").write(dumps(defaults.get("default")))

def chat(prompt, stream = True, preview = False, **kwargs):
    global _history
    global _history_file
    global _default_file
    hf = kwargs.get("_history_file")
    if isinstance(hf, str):
        _history_file = hf
        if _exists(_history_file):
            _history = loads(open(_history_file, "r").read())
    _history.append(dict(role = "user", content = prompt))
    use()
    defaults = loads(open(_default_file, "r").read())
    provider = defaults.get("provider")
    if(provider == "Ollama"):        
        response = _ch_submit_ollama(dumps(_history), stream, preview)
    else:
        return
    _history.append(dict(role = "assistant", content = response))
    open(_history_file, "w").write(dumps(_history))

def app(host = '127.0.0.1', port = 'auto'):
    global _history_file
    global _shiny_url
    if _shiny_url == '':
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
        _shiny_url = 'http://' + host + ":" + str(port)
        sleep(1)
    webbrowser.open(_shiny_url)
