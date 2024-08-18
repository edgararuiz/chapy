from tempfile import NamedTemporaryFile

def temp_script():
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
    return(temp_file.name)


