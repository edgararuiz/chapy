from chapy.utils import _ch_open_config
import ollama 

def _ch_submit_ollama(prompt, stream=True, preview=False, defaults={}):
    messages = []
    messages.append(dict(role="system", content=defaults.get("system_msg")))

    try:
        prompt = loads(prompt)
        messages = messages + prompt
    except ValueError:
        messages.append(dict(role="user", content=prompt))

    data = dict(model=defaults.get("model"), messages=messages, stream=stream)

    if preview:
        print(data)
        return ""

    response = ollama.chat(
        messages=messages, 
        keep_alive="5m", 
        model=defaults.get("model"), 
        stream=stream
        )

    full_out = ""
    for chunk in response:
        out = chunk['message']['content']
        full_out = full_out + out 
        print(out, end='', flush=True)

    return full_out

def _ch_models_ollama():
    defaults = _ch_open_config("ollama").get("default")
    tags = ollama.list()
    models = tags.get("models")
    out = []
    for model in models:
        m = dict(
            provider="ollama",
            model=model.get("model"),
            label="Ollama - " + model.get("name"),
        )
        out.append(m)
    return out


def _ch_available_ollama():
    out = True
    try:
        ollama.list()
    except:
        out = False

    return out
