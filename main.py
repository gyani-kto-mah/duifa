#!/usr/bin/env python3

from core import *
from fire import Fire


banner = """
 ______       _______ ___  
 |  _  \     (_)  ___/ _ \ 
 | | | |_   _ _| |_ / /_\ \\
 | | | | | | | |  _||  _  |
 | |/ /| |_| | | |  | | | |
 |___/  \__,_|_\_|  \_| |_/

"""[1:-1]


print('\x1b[1m'+ banner +'\x1b[0m')


class Duifa:

    def __init__(self, add: bool = False, remove: bool = False, a: bool = False, r: bool = False, rm: bool = False):
        
        print(info(f'Initialized [at] -> {fetchFormatedTime()}'))
        
        self.secret_files = self.list_secret_files()
        
        if any((add, a)):
            self.add()

        elif any((remove, rm, r)):
            self.remove()

        else:
            print(good('Select an App. no -> whoose you wish to see OTP of.'))
            self.display()

        coolExit()


    def list_secret_files(self):
        secret_files = []
        
        for _ in listdir():
            if  _.endswith('_secret.txt'):
                secret_files.append(_)

        if not secret_files:
            print(bad('No secret files -> You should first add a TOTP secret using `-a` flag.'))
            coolExit(1)

        self.secret_files = secret_files
        
        return secret_files


    def display(self, choice=None):

        if type(choice) != int:
            choice = self.choice()
        
        if type(choice) is bool and choice:
            for secret_filename in self.secret_files:
                otp = TOTP(read_secret(secret_filename))
                print(good(f'{secret_filename[:-11]} -> {otp.now()}'))
        
        else:
            secret_filename = self.secret_files[choice]
            app_name = secret_filename[:-11]
            otp = TOTP(read_secret(secret_filename))
            print(good(f'{app_name}\'s OTP (Copied to clipboard.) -> {otp.now()}'))
            copy(str(otp.now()))


    def add(self):
        
        app_name = coolInput('App name')
        secret = get_secret('App secret')
        filename = f'{app_name}_secret.txt'
        cipher = Cipher()
        c_secret = cipher.encrypt(secret.strip().replace(' ', ''))
        
        if not path.isfile(filename):
            open(filename, 'w').write(c_secret)
            sleep(0.4)
            self.display(self.list_secret_files().index(filename))
            print(good(f'{app_name} -> has been added to your TOTP secret storage.'))
        
        else:
            print(bad(f'{app_name} -> a TOTP secret already exists.'))
            coolExit(1)


    def choice(self):

        for _ in range(len(self.secret_files)):
            print(info(f'{_} -> {self.secret_files[_][:-11]}'))

        try:
            choice = int(coolInput('App no'))

        except Exception as exception:
            print(bad(f'Exception -> {exception}'))
            coolExit(1)

        if choice > _:
            print(bad("Error -> Given App no doesn't exist."))
            coolExit(1)

        elif choice < 0:
            return True

        return choice


    def remove(self):
        
        print(bad('Specify an App. no -> that you want to get rid of.'))
        
        choice = self.choice()
        
        if type(choice) is bool and choice:
            print(bad(f'Are you sure? -> you want to remove all TOTP secrets?'))
            prompt = coolInput('yes/[N]o')
            sleep(3.14285)
            if prompt.lower() in ('y', 'yes'):
                try:
                    for secret_filename in self.secret_files:
                        remove(secret_filename)
                        print(good(f'{secret_filename[:-11]}\'s TOTP secret -> \x1b[1mRemoved sucessfully.'))
                        sleep(0.7142857143)
                except Exception as e:
                    print(bad(f'Exception -> {e}'))
                    coolExit(1)
            else:
                coolExit()

        else:
            secret_filename = self.secret_files[choice]
            app_name = secret_filename[:-11]
            print(bad(f'Are you sure? -> You want to remove {app_name}\'s TOTP secret.'))
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


if __name__ == '__main__':
    chdir('.secrets')
    Fire(Duifa)