# duifa
```
 ______       _______ ___  
 |  _  \     (_)  ___/ _ \ 
 | | | |_   _ _| |_ / /_\ \
 | | | | | | | |  _||  _  |
 | |/ /| |_| | | |  | | | |
 |___/  \__,_|_\_|  \_| |_/
```

A simple script to generate TOTP for 2FA on Online Applications.

## FAQ
Q: I'm getting this `Not Implemented Error`:
```
pyperclip.PyperclipException: 
    Pyperclip could not find a copy/paste mechanism for your system.
```
A: Then, run this:
```
$ sudo apt install xclip -y
```
---
Q: How do I see OTP of all applications I'd added?

A: Just give it a negative number. (Example: -1) and It'll throw all OTPs on right to your face.
