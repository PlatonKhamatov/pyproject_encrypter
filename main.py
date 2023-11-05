import argparse
from encrypt import TextEncrypter
parser = argparse.ArgumentParser()
parser.add_argument('sourcefile', type=str, help='Source of text')
parser.add_argument('enc_type', type=str, help='EncryptionType')
parser.add_argument('--key', default='freq.json', required=False, type=str, help='EncryptionKey')
parser.add_argument('--printfile', default=None, required=False)
args = parser.parse_args()
enc = TextEncrypter(args.sourcefile)
if args.enc_type == "cae":
    enc.caesar_encrypt(int(args.key), args.printfile)
elif args.enc_type == "vig":
    enc.vigenere_encrypt(args.key, args.printfile)
elif args.enc_type == "xor":
    enc.xor_encrypt(args.key, args.printfile)
elif args.enc_type == "decae":
    enc.caesar_decrypt(int(args.key), args.printfile)
elif args.enc_type == "devig":
    enc.vigenere_decrypt(args.key, args.printfile)
elif args.enc_type == "dexor":
    enc.xor_decrypt(args.key, args.printfile)
elif args.enc_type == "brcae":
    enc.break_caesar(args.key, args.printfile)
else:
    raise ValueError("Invalid mode")
