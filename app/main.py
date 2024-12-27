import sys 
import os
import shutil

def find_executable(command, path):
    directories = path.split(":")
    for dir in directories:
        file_path = os.path.join(dir, command)
        if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
            return file_path
    return None
def main():
    commands = {"exit", "echo", "type"}
    PATH = os.environ.get("PATH", "")
    
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        # Wait for user input
        userInput = input()

        if (userInput == "exit 0"):
            sys.exit(0)
        
        elif (userInput.startswith("echo ")):
            print(userInput[len("echo ") :])
        
        elif (userInput.startswith("type ")):
            args = userInput.split()
            if len(args) == 2:
                if args[1] in commands:
                    print(f"{args[1]} is a shell builtin")
                else:
                    executable_path = find_executable(args[1], PATH)
                    if executable_path:
                        print(f"{args[1]} is {executable_path}")
                    else:
                        print(f"{args[1]}: not found")
            else:
                print(f"type: expected a command")          
        
        else:
            print(f"{userInput}: command not found")



if __name__ == "__main__":
    main()
