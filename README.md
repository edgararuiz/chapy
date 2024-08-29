# `chattr`

## Installation

To install from Github:

```python
pip install git+https://github.com/edgararuiz/chattr-python
```

## Usage (from Positron)

This application has been developed and tested in the [Positron IDE](https://github.com/posit-dev/positron). 

### Console 

To use in the console, use the `chat()` function:

```python
import chattr
chattr.chat("What package should I use to read parquet files?")
```

### Shiny app

As with it's sister R package, `chattr` comes with a Shiny for Python app that provides chat-like interface with the LLM. To 
use, make sure to have the VSCode [Shiny extension](https://marketplace.visualstudio.com/items?itemName=Posit.shiny) installed. 

To run the app use: 

```python
import chattr
chattr.app()
```

## Limitations

This package is very very new, so it has ALL the limitations :) At this time it only works with [Olama](https://ollama.com/download), 
and it is hard coded to use the [Llama 3.1](https://ollama.com/library/llama3.1) model. 

The Shiny app lacks much of the capabilities of its R countepart. At this time it is an MVP, which it is being enhanced with each
passing day. The rest of the package lacks the infrastructure of session tracking, and user CLI messaging. 