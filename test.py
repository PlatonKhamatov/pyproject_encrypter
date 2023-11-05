import unittest
from encrypt import TextEncrypter
import  os

class TestEncrypter(unittest.TestCase):
    def setUp(self):
        self.enc = TextEncrypter('tests/exam.txt')

    def test_cae(self):
        self.enc.caesar_encrypt(5, 'tests/f1.txt')
        with open('tests/f1.txt') as f1, open('tests/test1.txt') as f2:
            self.assertEqual(f1.read(), f2.read())
        os.remove('tests/f1.txt')

    def test_cae2(self):
        self.enc.caesar_decrypt(5, 'tests/f2.txt')
        with open('tests/f2.txt') as f1, open('tests/test2.txt') as f2:
            self.assertEqual(f1.read(), f2.read())
        os.remove('tests/f2.txt')

    def test_cae3(self):
        self.enc.caesar_decrypt(-5, 'tests/f3.txt')
        with open('tests/f3.txt') as f1, open('tests/test1.txt') as f2:
            self.assertEqual(f1.read(), f2.read())
        os.remove('tests/f3.txt')

    def test_cae4(self):
        self.enc.caesar_encrypt(-5, 'tests/f4.txt')
        with open('tests/f4.txt') as f1, open('tests/test2.txt') as f2:
            self.assertEqual(f1.read(), f2.read())
        os.remove('tests/f4.txt')

    def test_vig(self):
        self.enc.vigenere_encrypt('tests/vigkey.txt', 'tests/f5.txt')
        with open('tests/f5.txt') as f1, open('tests/test3.txt') as f2:
            self.assertEqual(f1.read(), f2.read())
        os.remove('tests/f5.txt')

    def test_vig2(self):
        self.enc.vigenere_decrypt('tests/vigkey.txt', 'tests/f6.txt')
        with open('tests/f6.txt') as f1, open('tests/test4.txt') as f2:
            self.assertEqual(f1.read(), f2.read())
        os.remove('tests/f6.txt')

    def test_xor(self):
        self.enc.xor_encrypt('tests/test1.txt', 'tests/f7.txt')
        with open('tests/f7.txt') as f1, open('tests/test5.txt') as f2:
            self.assertEqual(f1.read(), f2.read())
        os.remove('tests/f7.txt')


    def test_xor2(self):
        self.enc.xor_decrypt('tests/test1.txt', 'tests/f8.txt')
        with open('tests/f8.txt') as f1, open('tests/test6.txt') as f2:
            self.assertEqual(f1.read(), f2.read())
        os.remove('tests/f8.txt')

    def test_brcae(self):
        TextEncrypter('tests/test7.txt').break_caesar('freq.json', 'tests/f9.txt')
        with open('tests/f9.txt') as f1, open('tests/test8') as f2:
            self.assertEqual(f1.read(), f2.read())
        os.remove('tests/f9.txt')


if __name__ == '__main__':
    unittest.main()
