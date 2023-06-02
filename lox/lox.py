import sys

def run(code: str):
    print(code)

def run_file(file_path: str):
    file = open(file_path, 'r')
    run(file.read())

def run_prompt():
    while True:
        try:
            line = input()
            run(line)
        except (KeyboardInterrupt, EOFError):
            sys.exit(1)

def main():
    if len(sys.argv) == 2:
        run_file(sys.argv[1])
    elif len(sys.argv) == 1:
        run_prompt()
    else:
        print("Usage: python pylox [script]")

if __name__ == '__main__':
    main()