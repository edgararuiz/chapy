from .backend_ollama import _ch_submit_ollama
from os import path
import subprocess

def chat(prompt, stream = True, history = [], preview = False):
    return(
        _ch_submit_ollama(
            prompt = prompt, 
            stream = stream,
            history = history,
            preview = preview
            )
        )

def app():
    app_dir = path.dirname(chattr.__file__)
    app_file = path.join(app_dir, "app.py")
    args = [
    'shiny',
    'run', 
    app_file
    ]
    proc = subprocess.Popen(
        args,
        stdout=subprocess.PIPE
        )
