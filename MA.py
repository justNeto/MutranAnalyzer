'''
|----------------------------------|
Program created by github/justNeto
|----------------------------------|
'''
#import libraries
import sys, os, re


def input_options():
    try:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print_options()
            os._exit(1)

        elif sys.argv[1] == "-f" or sys.argv[1] == "--file":
            MUTRAN_FILE = open(sys.argv[2])
            return MUTRAN_FILE

        elif sys.argv[1] == "-v" or sys.argv[1] == "--version":
            print("Version 1.0")
            os._exit(1)

    except:
        print("Missing arguments. Try python", sys.argv[0], "-h or python", sys.argv[0], "--help for more information.\n")
        os._exit(1)

    else:
        print("Invalid option. Try python", sys.argv[0], "-h or python", sys.argv[0], "--help for more information.\n")
        os._exit(1)


def regex_validation(word):
    if re.fullmatch(r'(([A-G]|[A-G]([+-]*))[0-9]|(R))((W|H|Q|E|S|T|F)|(W|H|Q|E|S|T|F)(([.]+)|(T|3|5|7|9)))', word):
        return 0
    else:
        return 1


def print_options():
    print("Usage: python MA.py [OPTIONS] ... [FILE] ...\n")
    print("Analyzes a MUTRAN music file writing and produces the song accordingly.\n")
    print("Options for the analyzer.\n")
    print("-f, --file       file in MUTRAN to be analyzed.\n")
    print("-h, --help       shows this help menu and exits.\n")
    print("-v, --version    current version of project.\n")


''' Main python loop'''
def main():

    MUTRAN_FILE = input_options()
    MUTRAN_EXPRESSION = ""

    for line in MUTRAN_FILE:
        if line[0] == '*': # Drops everyline starting with *
            continue
        else:
            for i in range(len(line)):

                if (line[i] == " ") or (i == len(line)-1): # Checks if there is a space or a delimitator

                    if regex_validation(MUTRAN_EXPRESSION) == 0: # Checks if expression is valid
                        print(f"Expression read: {MUTRAN_EXPRESSION} - Expression validated")
                        # Play sound for a duration


                    else:
                        print(f"Expression read: {MUTRAN_EXPRESSION} - Expression is not validated - STOPPING THE PROGRAM")
                        os._exit(1)
                    MUTRAN_EXPRESSION = ""

                elif (line[i] !=  " "): # If there is not delimitator, it adds it to MUTRAN_EXPRESSION variable
                    MUTRAN_EXPRESSION += line[i]

    print("\nCode analyzed")

# Main Code
main()
