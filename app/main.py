import sys 
from os import chdir
from os.path import expanduser
import os
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
    if (args.startswith("'") and args.endswith("'")):
        message = args[6:-1]
    else:
        message = (" ".join(args))
    print(message)

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
        userInput, *args = input().split(" ")

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
