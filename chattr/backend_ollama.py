from .utils import _ch_open_config
from requests import post
from json import dumps, loads
from sys import stdout

def _ch_submit_ollama(prompt, stream = True, preview = False):
    defaults = _ch_open_config("ollama").get("default")

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