from .backend_ollama import _ch_submit_ollama, _ch_models_ollama, _ch_available_ollama
from .utils import _ch_open_config
from os import path
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
    models = []
    model_no = 0
    model = ''
    if provider == '':
        if _ch_available_ollama():
           models = models + _ch_models_ollama()
        print("\033[3m--- chattr ----------------\033[0m")
        for mod in models:
            model_no = model_no + 1
            print(str(model_no) + " - " + mod.get("label"))
        selection = input("\033[3mChoose a model to use: \033[0m")
        m = models[int(selection) - 1]
        provider = m.get("provider")
        model = m.get("model")
    if provider == "ollama":
        defaults = _ch_open_config("ollama")
    defaults = defaults.get("default")
    if len(kwargs) > 0:
        def_names = tuple(defaults.keys())
        new_defs = kwargs
        for n in def_names:
            if isinstance(new_defs.get(n), str):
                x = 0
            else:
                new_defs[n] = defaults.get(n)
        defaults = new_defs
    if model != '':
        defaults['model'] = model
    open(_default_file, "w").write(dumps(defaults))

def _defaults():
    global _default_file
    if not path.isfile(_default_file): 
        use()
    f = open(_default_file, "r").read()
    return(loads(f))

def chat(prompt, stream = True, preview = False, **kwargs):
    global _history
    global _history_file
    global _default_file
    hf = kwargs.get("_history_file")
    if isinstance(hf, str):
        _history_file = hf
        if path.isfile(_history_file):
            _history = loads(open(_history_file, "r").read())
    _history.append(dict(role = "user", content = prompt))
    defaults = _defaults()
    provider = defaults.get("provider")
    if(provider == "Ollama"):        
        response = _ch_submit_ollama(dumps(_history), stream, preview, defaults)
    else:
        return
    _history.append(dict(role = "assistant", content = response))
    open(_history_file, "w").write(dumps(_history))

def app(host = '127.0.0.1', port = 'auto'):
    global _history_file
    global _default_file
    global _shiny_url
    if _shiny_url == '':
        if port=='auto':
            sock = socket()
            sock.bind(('', 0))
            port = sock.getsockname()[1]
        app_file = path.join(path.dirname(__file__), "app.py")
        py_script  = open(app_file, "r").read()
        defaults = _defaults()
        py_script = "" +\
            "_history_file = '"+ _history_file + "'\n" +\
            "_default_file = '"+ _default_file + "'\n" +\
             py_script
        temp_script = NamedTemporaryFile()
        temp_script = str(temp_script.name) + '.py' 
        open(temp_script, "w").write(py_script)

        args = ['shiny', 'run', temp_script, '--port=' + str(port)]
        Popen(args, stdout= PIPE)
        _shiny_url = 'http://' + host + ":" + str(port)
        sleep(1)
    webbrowser.open(_shiny_url)
