from subprocess import Popen, PIPE
from tempfile import NamedTemporaryFile
from shiny import App, Inputs, Outputs, Session, reactive, render, ui
from json import dumps, loads
from os import _exists

if "_history_file" not in locals():
    _history_file = NamedTemporaryFile().name

def app_temp_script(path):
    code = "" +\
        "import chattr" + "\n" +\
        "import argparse" + "\n" +\
        "parser = argparse.ArgumentParser()" + "\n" +\
        "parser.add_argument('--prompt', default = '')" + "\n" +\
        "parser.add_argument('--stream', type = bool, default = True)" + "\n" +\
        "args = parser.parse_args()" + "\n" +\
        "if args.prompt != '':" + "\n" +\
        "    chattr.chat(args.prompt, args.stream, _history_file='" + path + "')"
    temp_file = NamedTemporaryFile().name
    open(temp_file, "w").write(code)
    return(temp_file)

app_ui = ui.page_fluid(
    ui.tags.style(".bslib-gap-spacing { padding:4px; font-size:90%; margin:1px; } "),
    ui.tags.style(".bslib-mb-spacing { padding:1px; margin:1px;}"),
    ui.tags.style(".bslib-grid-item { padding:1px; margin:1px;}"),
    ui.layout_columns(
      ui.div(
        ui.input_dark_mode(id = "mode"), 
      ),        
      ui.input_text_area("prompt", "", width="100%", resize=False),
      ui.div(
        ui.input_task_button("submit", "Submit", style = "font-size:65%; padding:4px; margin:2px"), 
      ),
      col_widths= (1, 9, 2)
    ),
    ui.layout_columns(
        ui.output_ui("value"),
        ui.p(),
        col_widths= (11, 1)
        ),    
    ui.output_ui(id = "main")
    )

temp_script = app_temp_script(_history_file)

def server(input: Inputs, output: Outputs, session: Session):
    response = ''
    proc = ''
    @reactive.effect
    @reactive.event(input.submit)
    def _():
        nonlocal proc   
        if input.prompt() != '':            
            args = [
                'python',
                temp_script, 
                f"--prompt=" + input.prompt() + ""
                ]
            proc = Popen(
                args,
                stdout = PIPE
                )        
            ui.update_text("prompt", value= "")
            ui.insert_ui(  
                ui.layout_columns(
                    ui.p(), 
                    ui.card(
                        ui.markdown(input.prompt()), 
                        style = "background-color: #376CA4; color: white;"
                        ),                                
                    col_widths= (1, 11)
                ), 
                selector= "#main", 
                where = "afterEnd"
                )                        
                
    @render.text
    def value():
        nonlocal response
        nonlocal proc
        out = ''
        reactive.invalidate_later(0.1)
        if hasattr(proc, "stdout"):
            out = proc.stdout.read(3)
            if out:
                out = str(out.decode())
                response = response + out
            else:
                if response != '':    
                    ui.insert_ui(                        
                        ui.layout_columns(
                            ui.card(
                                ui.markdown(response), 
                                style = "padding:0; margin:0; border-color: #ccc;"
                                ),
                            ui.p(),
                            col_widths= (11, 1)
                            ), 
                        selector= "#main", 
                        where = "afterEnd"
                    )            
                    response = ''         
        return ui.markdown(response)

app = App(app_ui, server)