import sys
import os
import subprocess
import shlex  # For parsing quoted strings

def main():
    # Define the list of built-in commands
    builtins = {"echo", "exit", "type", "pwd", "cd"}

    while True:
        # Display the shell prompt
        sys.stdout.write("$ ")
        sys.stdout.flush()

        try:
            # Read user input
            command = input().strip()

            # Parse input to handle quotes (both single and double)
            args = shlex.split(command, posix=True)
            
            if not args:
                continue  # Skip empty commands

            # Check for the '2>>' operator
            if "2>>" in args:
                redirect_index = args.index("2>>")
                cmd_args = args[:redirect_index]  # Command and its arguments
                output_file = args[redirect_index + 1] if redirect_index + 1 < len(args) else None

                if not cmd_args or not output_file:
                    print("syntax error: unexpected end of file")
                    continue

                # Execute the command and append stdout to the file
                try:
                    with open(output_file, "a") as file:
                        result = subprocess.run(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                        file.write(result.stderr)  # Append stderr to the file
                        if result.stdout:  # Print any errors to stdout
                            sys.stdout.write(result.stdout)
                except FileNotFoundError:
                    print(f"{cmd_args[0]}: command not found")
                except PermissionError:
                    print(f"Permission denied: {output_file}")
                except Exception as e:
                    print(f"Error: {e}")
                continue

            # Check for the '>>' or '1>>' operator
            if ">>" in args or "1>>" in args:
                # Normalize the operator to '>>' for simplicity
                operator = ">>" if ">>" in args else "1>>"
                redirect_index = args.index(operator)
                cmd_args = args[:redirect_index]  # Command and its arguments
                output_file = args[redirect_index + 1] if redirect_index + 1 < len(args) else None

                if not cmd_args or not output_file:
                    print("syntax error: unexpected end of file")
                    continue

                # Execute the command and append stdout to the file
                try:
                    with open(output_file, "a") as file:
                        result = subprocess.run(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                        file.write(result.stdout)  # Append stdout to the file
                        if result.stderr:  # Print any errors to stderr
                            sys.stderr.write(result.stderr)
                except FileNotFoundError:
                    print(f"{cmd_args[0]}: command not found")
                except PermissionError:
                    print(f"Permission denied: {output_file}")
                except Exception as e:
                    print(f"Error: {e}")
                continue

            # Check for the '2>' operator
            if "2>" in args:
                redirect_index = args.index("2>")
                cmd_args = args[:redirect_index]  # Command and its arguments
                output_file = args[redirect_index + 1] if redirect_index + 1 < len(args) else None

                if not cmd_args or not output_file:
                    print("syntax error: unexpected end of file")
                    continue

                # Execute the command and redirect output
                try:
                    with open(output_file, "w") as file:
                        result = subprocess.run(cmd_args, stdout=subprocess.PIPE, stderr=file, text=True)
                        if result.stdout:  # Print any errors to stderr
                            print(result.stdout.strip())
                except FileNotFoundError:
                    print(f"{cmd_args[0]}: command not found")
                except PermissionError:
                    print(f"Permission denied: {output_file}")
                except Exception as e:
                    print(f"Error: {e}")
                continue
            
            # Check for the `1>` operator
            if "1>" in args:
                redirect_index = args.index("1>")
                cmd_args = args[:redirect_index]  # Command and its arguments
                output_file = args[redirect_index + 1] if redirect_index + 1 < len(args) else None

                if not cmd_args or not output_file:
                    print("syntax error: unexpected end of file")
                    continue

                # Execute the command and redirect output
                try:
                    with open(output_file, "w") as file:
                        result = subprocess.run(cmd_args, stdout=file, stderr=subprocess.PIPE, text=True)
                        if result.stderr:  # Print any errors to stderr
                            sys.stderr.write(result.stderr)
                except FileNotFoundError:
                    print(f"{cmd_args[0]}: command not found")
                except PermissionError:
                    print(f"Permission denied: {output_file}")
                except Exception as e:
                    print(f"Error: {e}")
                continue


            # Check for output redirection
            if ">" in args:
                # Split the arguments into the command part and redirection part
                redirect_index = args.index(">")
                cmd_args = args[:redirect_index]  # Command and its arguments
                output_file = args[redirect_index + 1] if redirect_index + 1 < len(args) else None

                if not output_file:
                    print("syntax error: unexpected end of file")
                    continue

                # Open the file for writing (truncate if exists)
                with open(output_file, "w") as file:
                    # Run the command and redirect output to the file
                    result = subprocess.run(cmd_args, stdout=file, stderr=subprocess.PIPE, text=True)
                    if result.stderr:
                        print(result.stderr.strip(), file=sys.stderr)
                continue

            cmd = args[0]

            # Handle `exit` command
            if cmd == "exit":
                if len(args) > 1 and args[1].isdigit():
                    exit_code = int(args[1])
                else:
                    exit_code = 0
                sys.exit(exit_code)

            # Handle `type` command
            elif cmd == "type":
                if len(args) < 2:
                    print("type: missing operand")
                    continue

                cmd_to_check = args[1]
                if cmd_to_check in builtins:
                    print(f"{cmd_to_check} is a shell builtin")
                else:
                    # Search for the command in the directories listed in PATH
                    found = False
                    for directory in os.environ["PATH"].split(":"):
                        command_path = os.path.join(directory, cmd_to_check)
                        if os.path.isfile(command_path) and os.access(command_path, os.X_OK):
                            print(f"{cmd_to_check} is {command_path}")
                            found = True
                            break
                    
                    if not found:
                        print(f"{cmd_to_check}: not found")

            # Handle `pwd` command
            elif cmd == "pwd":
                print(os.getcwd())

            # Handle `cd` command (absolute, relative paths, and `~`)
            elif cmd == "cd":
                if len(args) < 2:
                    target_dir = os.environ.get("HOME", "/")  # Default to home directory
                else:
                    target_dir = args[1]

                # Handle `~` for home directory
                if target_dir == "~":
                    target_dir = os.environ.get("HOME", "/")

                try:
                    os.chdir(target_dir)  # Handles all valid paths
                except FileNotFoundError:
                    print(f"cd: {target_dir}: No such file or directory")
                except PermissionError:
                    print(f"cd: {target_dir}: Permission denied")

            # Handle `echo` command
            elif cmd == "echo":
                # Join the arguments to preserve spacing within quotes
                print(" ".join(args[1:]))

            # Handle running external programs
            else:
                # Search for the program in PATH
                found = False
                for directory in os.environ["PATH"].split(":"):
                    program_path = os.path.join(directory, cmd)
                    if os.path.isfile(program_path) and os.access(program_path, os.X_OK):
                        found = True
                        try:
                            # Run the program with its arguments
                            result = subprocess.run([program_path] + args[1:], capture_output=True, text=True)
                            # Print the program's output
                            print(result.stdout.strip())
                        except Exception as e:
                            print(f"Error running {cmd}: {e}")
                        break
                
                if not found:
                    print(f"{cmd}: not found")

        except EOFError:
            # Handle Ctrl+D (EOF)
            sys.exit(0)

if __name__ == "__main__":
    main()
