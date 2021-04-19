def run_test_from_filename(filename):
    try:
        with open(args.filename) as file:
            try:
                print(yaml.safe_load(file))

            except yaml.YAMLError as exc:
                print(exc)
    except FileNotFoundError:
        print("Error: System cannot find file specified")