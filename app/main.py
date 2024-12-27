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
            exists = False
            for i in commands:
                if(userInput[len("type ") :] == commands[i]):
                    print(f"{commands[i]} is a shell builtin")
                    exists = True
            if (exists == False):
                print(userInput[len("type ") :] + ": not found")            
            
        else:
            print(f"{userInput}: command not found")



if __name__ == "__main__":
    main()
