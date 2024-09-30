# chapy

This package is meant to make it easy to chat with LLM's inside your IDE. You select an LLM to use
for your Python session, and you can simply ask questions directly it, or use an included Shiny
app. The Shiny app recognizes code, and adds a "copy" button, which allows you to easily bring
it into your code. `chapy` also includes a default System Message, that tells the LLM that you
want code in Python, so your chat will already have that context.

The currently supported back ends are:

- [Ollama](https://ollama.com/)
- [OpenAI](https://platform.openai.com/docs/api-reference/introduction) 

## Installation

To install from Github:

```python
pip install git+https://github.com/edgararuiz/chapy
```

## Usage (from Positron)

This application has been developed and tested in the [Positron IDE](https://github.com/posit-dev/positron). 

### Console 

To use in the console, use the `chat()` function:

```python
import chapy
chapy.chat("What package should I use to read parquet files?")
```

If you have not specify the model you wish to use, `chapy` will prompt you to select one. The options will
be based on your environment. If it finds Ollama, it will list your currently installed models. If it
detects your OpenAI Token loaded in the **OPENAI_API_KEY** environment variable, it will display the current
OpenAI models. Here is an example:

```python
import chapy
chapy.chat("What package should I use to read parquet files?")

--- chapy ----------------
1 - Ollama - llama3.1:latest
2 - OpenAI - gpt-3.5
3 - OpenAI - gpt-4
4 - OpenAI - gpt-4o
Choose a model to use: 
```

### Shiny app

As with it's sister R package, `chapy` comes with a Shiny for Python app that provides chat-like interface with the LLM. To 
use, make sure to have the VSCode [Shiny extension](https://marketplace.visualstudio.com/items?itemName=Posit.shiny) installed. 

To run the app use: 

```python
import chapy
chapy.app()
```
