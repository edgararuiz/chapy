import subprocess
from tempfile import NamedTemporaryFile
from shiny import App, Inputs, Outputs, Session, reactive, render, ui
from json import dumps 

def ui_general(x = ''):
    return(
        "padding-top: 3px;" +\
        "padding-bottom: 3px;" +\
        "padding-left: 5px;" +\
        "padding-right: 5px;" +\
        x
    )

app_ui = ui.page_fluid(
    ui.tags.style(".bslib-gap-spacing { padding:4px; font-size:90%;} "),
    ui.tags.style(".bslib-mb-spacing { padding:1px; margin:1px;}"),
    ui.tags.style(".bslib-grid-item { padding:1px;}"),
    ui.tags.style(".bslib-grid { padding:10px;}"),
    ui.layout_columns(
      ui.div(
        ui.input_dark_mode(), 
      ),        
      ui.input_text_area("prompt", "", width="100%", resize=False),
      ui.div(
        ui.input_task_button("submit", "Submit", style = ui_general("font-size:65%; padding:4px; margin:2px")), 
        #ui.input_task_button("options", "Options", style = ui_general("font-size:65%; padding:3px; margin:2px;"))
      ),
      col_widths= (1, 10, 1)
    ),
    ui.layout_columns(
        ui.output_ui("value"),
        ui.p(),
        col_widths= (11, 1)
        ),    
    ui.output_ui(id = "main")
    )

history = []

code = "" +\
    "import chattr" + "\n" +\
    "import argparse" + "\n" +\
    "parser = argparse.ArgumentParser()" + "\n" +\
    "parser.add_argument('--prompt', default = '')" + "\n" +\
    "parser.add_argument('--stream', type = bool, default = True)" + "\n" +\
    "args = parser.parse_args()" + "\n" +\
    "if args.prompt != '':" + "\n" +\
    "    chattr.chat(args.prompt, args.stream)"

temp_file = NamedTemporaryFile()
with open(temp_file.name, 'w') as f:
    f.writelines(code)

temp_script = temp_file.name

def server(input: Inputs, output: Outputs, session: Session):
    response = ''
    proc = ''
    @reactive.effect
    @reactive.event(input.submit)
    def _():
        nonlocal proc   
        if input.prompt() != '':
            history.append(dict(role = "user", content = input.prompt()))
            args = [
                'python',
                temp_script, 
                f"--prompt=" + dumps(history) + ""
                ]
            proc = subprocess.Popen(
                args,
                stdout=subprocess.PIPE
                )        
            print(args)    
            ui.update_text("prompt", value= "")
            ui.insert_ui(  
                ui.layout_columns(
                    ui.p(), 
                    ui.card(
                        ui.markdown(input.prompt()), 
                        style = "background-color: #196FB6; color: white;"
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
                    history.append(dict(
                        role = "assistant",
                        content = response
                        ))                 
                    response = ''           
        return ui.markdown(response)

app = App(app_ui, server)
