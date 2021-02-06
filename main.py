#!/usr/bin/env python3
from pyotp import TOTP
from os import chdir, listdir
from stoyled import *
banner = """
 ______       _______ ___  
 |  _  \     (_)  ___/ _ \ 
 | | | |_   _ _| |_ / /_\ \\
 | | | | | | | |  _||  _  |
 | |/ /| |_| | | |  | | | |
 |___/  \__,_|_\_|  \_| |_/

"""[1:-1]

print(banner)
print(info(f'Initialized [at] -> {fetchFormatedTime()}'))

chdir('.secrets')
secret_files = []

for _ in listdir():
    if  _.endswith('_secret.txt'):
        secret_files.append(_)

for _ in range(len(secret_files)):
    print(info(f'{_} -> {secret_files[_][:-11]}'))

try:
    choice = int(coolInput('App no'))

except Exception as exception:
    print(warn(f'Exception -> {exception}'))
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
    print(good(f'OTP -> {otp.now()}'))
    chdir('..')

coolExit()
