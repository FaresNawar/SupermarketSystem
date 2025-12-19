# Ensure file is only imported and not ran
if __name__ == '__main__':
    print("This is a library file. Please run 'main.py' instead.")
    exit(0)

from classes import Settings
def error(msg = ""):
    print(msg, end='' if msg == "" else "\n")
    print("Press [Enter] to continue...")
    input()

def success(msg = ""):
    print(msg, end='' if msg == "" else "\n")
    print("Press [Enter] to continue...")
    input()