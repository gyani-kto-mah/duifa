from speck import SpeckCipher
from uuid import getnode


class Cipher:
    def __init__(self, key=0):
        if key:
            self.key = key
        else:
            self.key = getnode()

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