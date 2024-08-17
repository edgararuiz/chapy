from .backend_ollama import _ch_submit_ollama

def chat(prompt, stream = True, history = [], preview = False):
    return(
        _ch_submit_ollama(
            prompt = prompt, 
            stream = stream,
            history = history,
            preview = preview
            )
        )
