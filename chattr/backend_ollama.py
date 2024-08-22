from .utils import _ch_open_config
from requests import post, get
from json import dumps, loads
from sys import stdout

def _ch_submit_ollama(prompt, stream = True, preview = False, defaults = {}):
    messages = []
    messages.append(dict(
        role =  "system", 
        content = defaults.get("system_msg")
        ))

    try:
        prompt = loads(prompt)
        messages = messages + prompt
    except ValueError:
        messages.append(dict(
            role =  "user", 
            content = prompt
        ))
        
    data = dict(
        model = defaults.get("model"),
        messages =  messages, 
        stream = stream
    )

    if preview:    
        print(data)
        return()

    response = post(
        url = defaults.get("path") + "api/chat", 
        data = dumps(data),
        headers = {"Content-Type": "application/json"}, 
        stream = stream
        )
    
    out = ""
    for line in response.iter_lines():
        body = loads(line)
        resp = body.get("message")
        content = resp.get("content")
        out = out + content
        stdout.write(content)

    return(out)

def _ch_models_ollama():
    defaults = _ch_open_config("ollama").get("default")
    response = get(url = defaults.get("path") + "api/tags")
    tags = []
    for tag in response.iter_lines():
        tags.append(loads(tag))
    tags = tags[0]
    models = tags.get("models")
    out = []
    for model in models:
        m = dict(
            name = "ollama",
            model = model.get("model"),
            label = 'Ollama - ' + model.get("name")
            )
        out.append(m)
    return(out)