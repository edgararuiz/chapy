from requests import post
from json import dumps, loads
from sys import stdout

def _ch_submit_ollama(prompt, stream = True, preview = False):
    url = "http://localhost:11434/api/chat"

    headers = {
        "Content-Type": "application/json"
    }

    messages = []
    messages.append(dict(
        role =  "system", 
        content = "You are a helpful coding assistant that uses Python for data analysis. Keep comments to a minimum."
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
        model = "llama3.1",
        messages =  messages, 
        stream = stream
    )

    if preview:    
        print(data)
        return()

    response = post(url, data = dumps(data), headers = headers, stream = stream)
    for line in response.iter_lines():
        body = loads(line)
        resp = body.get("message")
        content = resp.get("content")
        stdout.write(content)
