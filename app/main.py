import sys 
from os import chdir
from os.path import expanduser
import os
import shlex
import subprocess

from typing import Optional

def find_executable(command) -> Optional[str]:
    PATH = os.environ.get("PATH", "")
    directories = PATH.split(":")
    
    for dir in directories:
        file_path = os.path.join(dir, command)
        if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
            return file_path
    return None

def handle_pwd(args):
    print(f"{os.getcwd()}")

def handle_exit(args):
    sys.exit(int(args[0]) if args else 0)

def handle_echo(args):
    # Join the list into a single string if it's a list
    if isinstance(args, list):
        args = " ".join(args)
    
    result = []
    current = []
    in_quotes = False
    quote_char = ""

    # Iterate through each character in the string
    for char in args:
        if char in ("'", '"'):  # Check for the start/end of quotes
            if in_quotes and char == quote_char:
                in_quotes = False
                result.append(''.join(current))
                current = []
            elif not in_quotes:
                in_quotes = True
                quote_char = char
            else:
                current.append(char)
        elif char == " " and not in_quotes:  # Handle spaces outside quotes
            if current:
                result.append(''.join(current))
                current = []
        else:
            current.append(char)

    if current:  # Add the last part if exists
        result.append(''.join(current))

    # Join everything with a space between the tokens
    print(" ".join(result))


def handle_type(args):
    if args[0] in builtins:
        print(f"{args[0]} is a shell builtin")
    elif executable := find_executable(args[0]):
        print(f"{args[0]} is {executable}")
    else:
        print(f"{args[0]}: not found")

def handle_cd(args):
    dir = args[0]
    try:
        chdir(expanduser(dir))
    except OSError:
        print(f"cd: {dir}: No such file or directory")

builtins = { "exit": handle_exit, "echo": handle_echo, "type": handle_type, "pwd": handle_pwd, "cd": handle_cd }

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        # Wait for user input
        userInput = input()
        tokens = shlex.split(userInput)
        userInput, *args = tokens

        if userInput in builtins:
            builtins[userInput](args)
            continue
        elif executable := find_executable(userInput):
            subprocess.run([executable, *args])   
        else:
            print(f"{userInput}: command not found")

        sys.stdout.flush()

if __name__ == "__main__":
    main()
