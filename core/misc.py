from clipboard import copy
from os import path, chdir, listdir, remove
from .crypt import Cipher
from time import sleep
from pyotp import TOTP


def read_secret(secret_filename):
    secret_file = open(secret_filename).read().strip().replace(' ', '')
    cipher = Cipher()
    secret = cipher.decrypt(secret_file).strip().replace(' ', '')
    return secret