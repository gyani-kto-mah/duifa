#!/usr/bin/env python3

from pyotp import TOTP
from os import path, chdir, listdir, remove
from stoyled import *
from platform import system as platform
from sys import argv
from clipboard import copy
from uuid import getnode
from speck import SpeckCipher

banner = """
 ______       _______ ___  
 |  _  \     (_)  ___/ _ \ 
 | | | |_   _ _| |_ / /_\ \\
 | | | | | | | |  _||  _  |
 | |/ /| |_| | | |  | | | |
 |___/  \__,_|_\_|  \_| |_/

"""[1:-1]

REMOVE = False
print('\x1b[1m'+ banner +'\x1b[0m')

if '-h' in argv or '--help' in argv:
    print('Usage: python3 main.py [flags...]')
    print('-h,  --help\t Shows this help screen.')
    print('-a,  --add\t Adds a new TOTP secret.')
    print('-r,  --remove\t Remove a TOTP secret.', end='\n'*2)
    print('If used without any flag, would default to display OTP mode.')
    exit()

print(info(f'Initialized [at] -> {fetchFormatedTime()}'))


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

class Cipher:
    def __init__(self, key):
        self.key = key

    def chunks(self, l, n):
        n = max(1, n)
        return (l[i:i+n] for i in range(0, len(l), n))

    def encode(self, string: str) -> int:
        num = 0
        for ch in str(string):
            num = num * 100
            num += (ord(ch) - 23)
        return num


    def decode(self, num: int) -> str:
        res = ""
        num = int(num)
        while num > 0:
            lastDigit = num % 100
            res += chr(lastDigit+23)
            num = num // 100
        return res[::-1]


    def encrypt(self, plaintext):
        out = []
        number_str = str(self.encode(str(plaintext)))
        chunked_number_str = self.chunks(number_str, 19)
        for nstr in chunked_number_str:
            encrypted_str = SpeckCipher(self.key).encrypt(int(nstr))
            out.append(encrypted_str)

        return ".".join([str(x) for x in out])


    def decrypt(self, ciphertext):
        out = ""
        for n in ciphertext.split("."):
            out += str(SpeckCipher(self.key).decrypt(int(n)))
        return self.decode(int(out))


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
    cipher = Cipher(getnode())
    secret = cipher.encrypt(secret.strip().replace(' ', ''))
    if not path.isfile(filename):
        open(filename, 'w').write(secret)
        return True
    return False


def read_secret(secret_filename):
    secret_file = open(secret_filename).read().strip().replace(' ', '')
    cipher = Cipher(getnode())
    secret = cipher.decrypt(secret_file).strip().replace(' ', '')
    return secret


if any(_ in argv for _ in ('-a', '-ad', '-add', '--add')):
    app_name = coolInput('App name')
    secret = get_secret('App secret')
    if not write_secret(app_name, secret):
        print(bad(f'Failed to write secret of -> {app_name}'))
        coolExit(1)
    print(good(f'{app_name} -> was added to TOTP secret storage.'))
    coolExit()

if any(_ in argv for _ in ('-r', '-rm', '--rm',
                            '-remove', '--remove')):
    REMOVE = True

for _ in listdir():
    if  _.endswith('_secret.txt'):
        secret_files.append(_)

if not secret_files:
    print(bad('No secret files -> You should first add a TOTP secret using `-a` flag.'))
    coolExit(1)

if REMOVE:
    print(bad('Select the App. no you want to remove.'))

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
    if REMOVE:
        print(bad(f'Are you sure, you want to remove all TOTP secrets?'))
        prompt = coolInput('yes/[N]o')
        if prompt.lower() in ('y', 'yes'):
            # Recursive removal
            try:
                for secret_filename in secret_files:
                    remove(secret_filename)
                    print(good(f'{secret_filename[:-11]}\'s TOTP secret -> Removed sucessfully.'))
            except Exception as e:
                print(bad(f'Exception -> {e}'))
                coolExit(1)
        else:
            coolExit()
    else:
        for secret_filename in secret_files:
            print(info(f'App -> {secret_filename[:-11]}'))
            otp = TOTP(read_secret(secret_filename))
            print(good(f'OTP -> {otp.now()}'))
else:
    secret_filename = secret_files[choice]
    app_name = secret_filename[:-11]
    if REMOVE:
        print(bad(f'Are you sure? You want to remove {app_name}\'s TOTP secret.'))
        prompt = coolInput('yes/[N]o')
        if prompt.lower() in ('y', 'yes'):
            try:
                remove(secret_filename)
                print(good(f'{app_name}\'s TOTP secret -> Removed sucessfully.'))
            except Exception as exp:
                print(bad(f'Exception -> {exp}'))
                coolExit(1)
        else:
            coolExit()
    else:
        print(info(f'App -> {app_name}'))
        otp = TOTP(read_secret(secret_filename))
        print(good(f'OTP (Copied to clipboard.) -> {otp.now()}'))
        copy(str(otp.now()))

chdir('..')

coolExit()
