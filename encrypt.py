import collections
import itertools
import json
import string
import os
__all__ = ['TextEncrypter', 'ImageEncrypter']
MAXsymb: int = 127
MINsymb: int = 32
TEXTFMT: str = 'txt'


class AbstractEncrypter(object):
    def __init__(self, filename: str):
        '''
        :param filename: path to the file you need to encrypt/decrypt
        '''
        if not isinstance(filename, str):
            raise TypeError("filename must be string")
        if not os.path.isfile(filename):
            raise ValueError("file does not exist")
        self.filename: str = filename
        self.check_filename(filename, TEXTFMT)

    @staticmethod
    def check_filename(filename: str, fmt: str):
        '''
        Method checks the extension of file
        If it doesn't match format, raises a ValueError
        :param filename: path to the file
        :param fmt: required extension type
        :return: None
        '''
        if filename.rsplit('.', 1)[-1] != fmt:
            raise ValueError("filename is not correct")


class TextEncrypter(AbstractEncrypter):
    def __init__(self, filename: str):
        '''
        :param filename: path to the file you need to encrypt/decrypt
        Also opens the file and stores the contents in the variable self.text
        '''
        super().__init__(filename)
        with open(filename, encoding='utf8') as file:
            self.text = file.read()

    def caesar_encrypt(self, key: int, printfile=None):
        '''
        Cyclically shifts the characters of a file by the alphabet, consisting of 32-126 ASCII symbols
        :param key: parameter of shift
        :param printfile: file to save the result. By default, is equal to self.filename
        :return:
        '''
        if printfile is None:
            printfile = self.filename
        else:
            self.check_filename(printfile, TEXTFMT)
        encr_table = {i: MINsymb + (i - MINsymb + key) % (MAXsymb - MINsymb) for i in range(MINsymb, MAXsymb)}
        with open(printfile, 'w') as pfile:
            pfile.write(self.text.translate(encr_table))

    def xor_encrypt(self, filekey: str, printfile=None):
        '''
        Encrypts a file using the Vernam method
        :param filekey: encryption key (path to file containing it), number of characters must be equal to len(self.text)
        :param printfile: file to save a result. By default, is equal to self.filename
        :return: None
        '''
        if printfile is None:
            printfile = self.filename
        if not os.path.isfile(filekey):
            self.check_filename(filekey, TEXTFMT)
            raise ValueError("Invalid key")
        with open(filekey) as file:
            enc_string = file.read()
        if len(enc_string) != len(self.text):
            raise ValueError("Invalid key")
        with open(printfile, 'w') as pfile:
            for symb, ksymb in zip(self.text, enc_string):
                pfile.write(chr(ord(symb) ^ ord(ksymb)))

    def vigenere_encrypt(self, filekey: str, printfile=None):
        '''
        Encrypts the file using the Vigenere method
        :param filekey: encryption key (path to file containing it)
        :param printfile: file to save a result By default, is equal to self.filename
        :return: None
        '''
        if printfile is None:
            printfile = self.filename
        if not os.path.isfile(filekey):
            self.check_filename(filekey, TEXTFMT)
            raise ValueError("Invalid key")
        with open(filekey) as file:
            enc_string = file.read()
        if not all(MINsymb <= ord(i) < MAXsymb for i in enc_string):
            print(repr(enc_string))
            raise ValueError("Invalid key")
        enc_iter = itertools.cycle(map(ord, enc_string))
        with open(printfile, 'w') as pfile:
            for symb in self.text:
                if MINsymb <= ord(symb) < MAXsymb:
                    pfile.write(chr(MINsymb + (ord(symb) + next(enc_iter) - MINsymb) % (MAXsymb - MINsymb)))
                else:
                    pfile.write(symb)

    def caesar_decrypt(self, key: int, printfile=None):
        '''
        Decrypts the file, encrypted by Caesar's method
        :param key: key of encryption
        :param printfile: file to save the result
        :return: None
        '''
        self.caesar_encrypt(-key, printfile)

    def xor_decrypt(self, filekey: str, printfile=None):
        '''
        Decrypts the file, encrypted by Vernam's method
        :param filekey: key of encryption
        :param printfile: file to save the result
        :return: None
        '''
        self.xor_encrypt(filekey, printfile)

    def vigenere_decrypt(self, filekey: str, printfile=None):
        '''
        Decrypts the file, encrypted by Vigenere's method
        :param filekey: key of encryption
        :param printfile: file to save the result
        :return: None
        '''
        with open(filekey) as file:
            enc_string = file.read()
        if not os.path.isfile(filekey):
            self.check_filename(filekey, TEXTFMT)
            raise ValueError("Invalid key")
        if not all(MINsymb <= ord(i) < MAXsymb for i in enc_string):
            raise ValueError("Invalid key")
        enc_iter = itertools.cycle(enc_string)
        with open(printfile, 'w') as pfile:
            for symb in self.text:
                if MINsymb <= ord(symb) < MAXsymb:
                    pfile.write(chr(MINsymb + (ord(symb) - MINsymb - ord(next(enc_iter))) % (MAXsymb - MINsymb)))
                else:
                    pfile.write(symb)

    def break_caesar(self, freqtable: str, printfile=None):
        '''
        Breaks the Caesar's shifre in the most simple case (cyclical shift on the alphabet a-z)
        :param freqtable: table of average frequencies of letters (path to json file)
        :param printfile: file to save the results
        :return: None
        '''
        if not os.path.isfile(freqtable):
            self.check_filename(freqtable, 'json')
            raise ValueError("Invalid frequency table")
        with open('freq.json') as f:
            ftable = collections.Counter(json.load(f))
        if printfile is None:
            printfile = self.filename
        c = collections.Counter((i for i in self.text.lower() if i in string.ascii_lowercase))
        trdct = {}
        for pair1, pair2 in zip(c.most_common(len(c)), ftable.most_common(len(c))):
            trdct[ord(pair1[0])] = ord(pair2[0])
            trdct[ord(pair1[0]) - 32] = ord(pair2[0]) - 32
        with open(printfile, 'w') as pfile:
            pfile.write(self.text.translate(trdct))


class ImageEncrypter(AbstractEncrypter):
    def __init__(self, filename: str):
        super().__init__(filename)
