import sys
import os
import subprocess


def locate_executable(user_input):
    executable = user_input.split()[0]
    paths = os.environ.get("PATH").split(os.pathsep)
    for path in paths:
        exec_path = os.path.join(path, executable)
        if os.path.isfile(exec_path) and os.access(exec_path, os.X_OK):
            return exec_path  # Return the full path of the executable

    return None

def handle_input(user_input):
    builtin = ["exit", "echo", "type"]

    match user_input.split():
        case ["exit", "0"]:
            sys.exit(0)
        case ["echo", *args]:
            sys.stdout.write(" ".join(args)+"\n")
            sys.stdout.flush()     
        case ["type", arg] if arg in builtin:
            sys.stdout.write(f"{arg} is a shell builtin\n")
            sys.stdout.flush()
        case ["type", arg] if arg not in builtin:
            if path := locate_executable(arg):
                sys.stdout.write(f"{arg} is {path}\n")
                sys.stdout.flush()
            else:
                sys.stdout.write(f"{arg}: not found\n")
                sys.stdout.flush()
            
        case _:
            if path := locate_executable(user_input):
                command, *args = user_input.split()
                subprocess.run([command, *args])
            else:
                sys.stdout.write(f"{user_input}: command not found\n")
            sys.stdout.flush()

def main():
    while True:
        user_input = input("$ ")
        handle_input(user_input)

if __name__ == "__main__":
    main()
