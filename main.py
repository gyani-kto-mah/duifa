#!/usr/bin/env python3

from pyotp import TOTP
from os import path, chdir, listdir
from stoyled import *
import platform #  import system
from sys import argv
import clipboard #  import copy

banner = """
 ______       _______ ___  
 |  _  \     (_)  ___/ _ \ 
 | | | |_   _ _| |_ / /_\ \\
 | | | | | | | |  _||  _  |
 | |/ /| |_| | | |  | | | |
 |___/  \__,_|_\_|  \_| |_/

"""[1:-1]

print('\x1b[1m'+ banner +'\x1b[0m')

if '-h' in argv or '--help' in argv:
    print('Usage: python3 main.py [flags...]')
    print('-h,  --help\t Shows this help screen.')
    print('-a,  --add\t Adds a new TOTP secret.', end='\n'*2)
    print('If used without any flag, would default to display OTP mode.')
    exit()

print(info(f'Initialized [at] -> {fetchFormatedTime()}'))


if platform.system() == "Windows":
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

chdir('.secrets')
secret_files = []

def get_secret(prompt='Enter secret', redact='*'):
    redact = str(redact)[0]
    if not redact:
        redact = '*'
    print(takenInput(f'{purple_l}{prompt}: '), end='', flush=True)
    chars = ''
    oops = 0
    while 1:
        # TESTED ONLY ON POSIX
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


def write_secret(app_name, secret):
    filename = f'{app_name}_secret.txt'
    if not path.isfile(filename):
        open(filename, 'w').write(secret)
        return True
    return False


if '-a' in argv or '--add' in argv:
    app_name = coolInput('App name')
    secret = get_secret('App secret')
    if not write_secret(app_name, secret):
        print(bad(f'Failed to write secret of -> {app_name}'))
        coolExit(1)
    print(good(f'{app_name} -> was added to TOTP secret storage.'))
    coolExit()

for _ in listdir():
    if  _.endswith('_secret.txt'):
        secret_files.append(_)

if not secret_files:
    print(bad('No secret files -> You should first add a TOTP secret using `-a` flag.'))
    coolExit(1)

for _ in range(len(secret_files)):
    print(info(f'{_} -> {secret_files[_][:-11]}'))

try:
    choice = int(coolInput('App no'))
except Exception as exception:
    print(bad(f'Exception -> {exception}'))
    coolExit(1)

if choice > _:
    print(bad("Error -> Given App no doesn't exist."))
    coolExit(1)
elif choice < 0:
    for secret_filename in secret_files:
        print(info(f'App -> {secret_filename[:-11]}'))
        otp = TOTP(open(secret_filename).read().strip().replace(' ', ''))
        print(good(f'OTP -> {otp.now()}'))
else:
    secret_filename = secret_files[choice]
    print(info(f'App -> {secret_filename[:-11]}'))
    otp = TOTP(open(secret_filename).read().strip().replace(' ', ''))
    clipboard.copy(str(otp.now()))
    print(good(f'OTP (Copied to clipboard.) -> {otp.now()}'))

chdir('..')

coolExit()
