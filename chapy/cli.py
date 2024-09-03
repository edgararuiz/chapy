from argparse import ArgumentParser


def app_cli():
    parser = ArgumentParser()
    parser.add_argument("--prompt", default="")
    parser.add_argument("--stream", type=bool, default=True)
    parser.add_argument("--history", default="")
    parser.add_argument("--default", default="")
    args = parser.parse_args()
    if args.prompt != "":
        import chapy

        if args.history != "":
            chapy.chat(
                prompt=args.prompt,
                stream=args.stream,
                _history_file=args.history,
                _default_file=args.default,
            )
        else:
            chapy.chat(prompt=args.prompt, stream=args.stream)


if __name__ == "__main__":
    app_cli()
