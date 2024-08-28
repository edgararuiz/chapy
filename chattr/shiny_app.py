from subprocess import Popen, PIPE
from tempfile import NamedTemporaryFile
from shiny import App, Inputs, Outputs, Session, reactive, render, ui
from json import loads
from os import path
import pyperclip
import faicons

if "_history_file" not in locals():
    _history_file = NamedTemporaryFile().name

if "_default_file" not in locals():
    _default_file = NamedTemporaryFile().name

if "_pkg_location" not in locals():
    _pkg_location = path.dirname(__file__)

btn_copy_no = 0
btn_copy_txt = []

_history_file = "/Users/edgar/Projects/chattr-python/out.out"

app_ui = ui.page_fluid(
    ui.tags.style(".bslib-gap-spacing { padding:4px; font-size:80%; margin:1px; } "),
    ui.tags.style(".bslib-mb-spacing { padding:1px; margin:1px;}"),
    ui.tags.style(".bslib-grid-item { padding:1px; margin:1px;}"),
    ui.tags.style(".bslib-card { padding:1px; margin:5px;}"),
    ui.tags.style(".col-sm-11 { margin: 0px; padding-left: 2px; padding-right: 2px; }"),
    ui.tags.style(".col-sm-1 { margin: 0px; padding-left: 2px; padding-right: 2px; }"),
    ui.tags.style("#prompt { font-size:80%; padding: 0; margin: 0;}"),
    ui.tags.style("#main { font-size:80%; padding: 3px; }"),
    ui.tags.style(".row { padding:0; margin:0px;}"),
    ui.tags.style(".shiny-input-container { padding:2px; margin:0px;}"),
    ui.panel_absolute(
        ui.div(
            ui.output_ui("value").add_style("margin-right: 40px; font-size:80%;"),
            ui.output_ui(id="main")
        ),
        top="70px",
        left="0px",
        width="96%"
    ),
    ui.panel_fixed(
        ui.row(
            ui.row(ui.input_text_area("prompt", "", width="100%", resize=False, autoresize=False)),
            ui.row(
                ui.input_task_button(
                    "submit",
                    "Submit",
                    style="font-size:65%; padding:4px; margin-left: auto;margin-right: 0; width: 50px;",
                )#,
                #ui.input_dark_mode(id="mode")
            )
        ).add_style("background-color: #ddd; padding-top: 2px; padding-bottom: 5px; padding-right: 2px; padding-left: 2px;"),
        width="100%",
        left="0px"
    )    
)

def app_add_user(x):
    ui.insert_ui(
        ui.card(
            ui.markdown(x), 
            style="background-color: #376CA4; color: white; margin-left: 50px; width: 92%;"
            ),
        selector="#main",
        where="afterEnd"
    )

def app_add_assistant(x, input):

    btn_curr = btn_copy_no
    ui.insert_ui(
        ui.card(
            parse_response(x), style="padding:0; margin-right: 20px; border-color: #ccc;"
        ),
        selector="#main",
        where="afterEnd",
    )
    if btn_curr != btn_copy_no:
        for btn in range(btn_curr + 1, btn_copy_no + 1):
            btn_id = "copy" + str(btn)
            @reactive.effect
            @reactive.event(getattr(input, btn_id))
            def _():
                pyperclip.copy(btn_copy_txt[btn - 1])

def parse_response(x):
    global btn_copy_no
    x_split = x.split("```")
    out = ""
    ret = ()
    is_code = False
    ignore_rw = False
    for i in x_split:
        out = out + i
        if is_code:
            if i == "":
                ignore_rw = True
            else:
                ignore_rw = False
            btn_copy_no = btn_copy_no + 1
            btn_id = "copy" + str(btn_copy_no)
            ci = "```" + i + "```"
            rw = ui.div(
                ui.row(
                    ui.input_task_button(
                        btn_id,
                        "", 
                        icon= faicons.icon_svg("copy", margin_left=0, margin_right=0, width="15px"),
                        style="font-size:65%; padding:2px; margin:1px; background-color: #bbb; " + 
                              "border-color: #ddd; width: 50px; margin-left: auto;margin-right: 0;" +
                              "margin-bottom: -30px;",
                        ),
                ui.row(ui.markdown(ci)),
                ))
        else:
            ignore_rw = False
            rw = ui.row(ui.markdown(i))
        if is_code == False:
            is_code = True
        else:
            code = i.split("\n")
            code = code[1:len(code) + 1]
            code = "\n".join(code)
            btn_copy_txt.append(code)
            is_code = False

        if i != "":
            ret = ret, rw
    return ret

def server(input: Inputs, output: Outputs, session: Session):
    response = ""
    proc = ""

    if path.isfile(_history_file):
        history = loads(open(_history_file, "r").read())
        for entries in history:
            role = entries.get("role")
            content = entries.get("content")
            if role == "user":
                app_add_user(content)
            if role == "assistant":
                app_add_assistant(content, input)

    @reactive.effect
    @reactive.event(input.submit)
    def _():
        nonlocal proc
        if input.prompt() != "":
            script_path = path.join(_pkg_location, "cli.py")
            args = [
                "python",
                script_path,
                f"--prompt={input.prompt()}",
                f"--history={_history_file}",
                f"--default={_default_file}",
            ]
            proc = Popen(args, stdout=PIPE)
            ui.update_text("prompt", value="")
            app_add_user(input.prompt())

    @render.text
    def value():
        nonlocal response
        nonlocal proc
        out = ""
        reactive.invalidate_later(0.1)
        if hasattr(proc, "stdout"):
            out = proc.stdout.read(3)
            if out:
                out = str(out.decode())
                response = response + out
            else:
                if response != "":
                    app_add_assistant(response, input)
                    response = ""
        return ui.markdown(response)


app = App(app_ui, server)
