import sys
from src.computer import Computer


def main():
    try: filename = sys.argv[1]
    except IndexError: filename = ''

    try: speed = sys.argv[2]
    except IndexError: speed = 0.02

    computer = Computer()
    computer.run(filename, speed)


if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: sys.exit()