from stoyled import *
from platform import system as platform


if platform() == "Windows":
    import msvcrt
    def getch():
        return msvcrt.getch()
else:
    from sys import stdin
    from termios import tcgetattr, tcsetattr, TCSADRAIN
    from tty import setraw
    def getch():
        f = stdin.fileno()
        o = tcgetattr(f)
        try:
            setraw(stdin.fileno())
            char = stdin.read(1)
        finally:
            tcsetattr(f, TCSADRAIN, o)
        return char


def get_secret(prompt='Enter secret', redact='*'):
    redact = str(redact)[0]
    if not redact:
        redact = '*'
    print(takenInput(f'{purple_l}{prompt}: '), end='', flush=True)
    chars = ''
    oops = 0
    while 1:
        # CAUTION: TESTED ONLY ON POSIX
        char = getch()
        chars += char
        print(redact, end='', flush=True)
        if char == '\x7f':
            if len(chars) > 1:
                chars = chars[:-2]
                print('\b\b  \b\b', end='', flush=True)
            else:
                chars = chars[:-1]
                print('\b \b', end='', flush=True)
        elif char == '\x17':
            lc = len(chars)
            chars = ''
            print('\b'*lc + ' '*lc + '\b'*lc, end='', flush=True)
        elif char in (
                        '\x01', '\x02', '\x05',
                        '\x06', '\x07', '\x08',
                        '\x10', '\x11', '\x12',
                        '\x13', '\x14', '\x15',
                        '\x19', '\x0b', '\x0c',
                        '\x0f', '\x1a', '\x18',
                        '\x16', '\x0e'
                    ):
            chars = chars[:-1]
            print('\b \b', end='', flush=True)
        elif char == '\x03':
            chars = chars[:-1]
            print('\b \b')
            raise KeyboardInterrupt()
        elif char == '\x04':
            chars = chars[:-1]
            print('\b \b')
            raise EOFError()
        elif char == '\r':
            chars = chars[:-1]
            print('\b \b')
            break
        elif char == '\x1b':
            oops += 1
        elif char == '[':
            if oops:
                oops += 1
        elif char in ('A', 'B', 'C', 'D'):
            if oops == 2:
                chars = chars[:-3]
                print('\b\b\b   \b\b\b', end='', flush=True)
                oops = 0
    return chars