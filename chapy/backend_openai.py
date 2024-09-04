from chapy.utils import _ch_open_config
from openai import OpenAI
from json import loads 
import os

def _ch_submit_openai(prompt, stream=True, preview=False, defaults={}):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
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

    response = client.chat.completions.create(
        messages=messages, 
        model=defaults.get("model"), 
        stream=stream
        )

    full_out = ""
    for chunk in response:
        out = chunk.choices[0].delta.content or ""
        full_out = full_out + out 
        print(out, end='', flush=True)

    return full_out

def _ch_models_openai():
    models = ["gpt-3.5", "gpt-4", "gpt-4o"]
    out=[]
    for model in models:
        m = dict(
            provider="openai",
            model=model,
            label="OpenAI - " + model,
        )
        out.append(m)
    return out

def _ch_available_openai():
    return os.environ.get("OPENAI_API_KEY") != None
