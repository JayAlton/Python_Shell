import sys 

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        commands = {"exit", "echo", "type"}

        
        # Wait for user input
        userInput = input()
        if (userInput == "exit 0"):
            sys.exit(0)
        elif (userInput.startswith("echo ")):
            print(userInput[len("echo ") :])
        elif (userInput.startswith("type ")):
            args = userInput.split()
            if len(args) == 2 and args[1] in commands:
                print(f"{args[1]} is a shell builtin")
            else:
                print(f"{args[1]}: not found")          
        else:
            print(f"{userInput}: command not found")



if __name__ == "__main__":
    main()
