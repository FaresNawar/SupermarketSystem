"""
error_handling.py
This is a helper file that is specifically used for printing
error and success messages easily
"""

# Ensure file is only imported and not ran
if __name__ == '__main__':
    print("This is a library file. Please run 'main.py' instead.")
    exit(0)


def error(msg=""):
    print(msg, end='' if msg == "" else "\n")
    print("Press [Enter] to continue...")
    input()


def success(msg=""):
    print(msg, end='' if msg == "" else "\n")
    print("Press [Enter] to continue...")
    input()
