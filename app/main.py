import sys 
import os

def main():
    commands = {"exit", "echo", "type"}
    PATH = os.environ.get("PATH")
    
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
            args = userInput.split(" ")[1]
            cmd_path = None
            paths = PATH.split(":")
            for path in paths:
                if os.path.isfile(f"{path}/{args}"):
                    cmd_path = f"{path}/{args}"
            if args in commands:
                print(f"{args[1]} is a shell builtin")
            elif cmd_path:
                print(f"{args} is {cmd_path}\n")
            else:
                print(f"{args[1]}: not found")          
        else:
            print(f"{userInput}: command not found")
    


if __name__ == "__main__":
    main()
