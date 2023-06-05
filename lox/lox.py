import sys
from scanner import Scanner, Token
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)-10s%(asctime)s %(filename)s:%(lineno)s - %(funcName)10s() %(message)s")

LOGGER = logging.getLogger(__name__)

had_error=False

def error(line: int, message: str) -> None:
    report(line, "", message)

def report(line: int, where: str, message: str) -> None:
    global had_error
    LOGGER.error(f"line {line} Error {where} : {message}")
    had_error = True

def run(code: str) -> None:
    scanner = Scanner(code)
    for token in scanner.scan_tokens():
        LOGGER.info(token)
    # LOGGER.info(code)

def run_file(file_path: str) -> None:
    try:
        with open(file_path, 'r') as file:
            run(file.read())
    except Exception:
        LOGGER.error("Error ", exc_info=True)
        if had_error:
            sys.exit(1)

def run_prompt() -> None:
    global had_error
    while True:
        try:
            line = input()
            run(line)
            had_error = False
        except (KeyboardInterrupt, EOFError):
            sys.exit(1)

def main():
    if len(sys.argv) == 2:
        run_file(sys.argv[1])
    elif len(sys.argv) == 1:
        run_prompt()
    else:
        LOGGER.info("Usage: python pylox [script]")

if __name__ == '__main__':
    main()