# !! Install pycryptodome Package
from Crypto.Cipher import AES
from Crypto.Hash import SHA1
from cmd import Cmd
import os


KEY = b'1107795287110779'


class MyCmd(Cmd):
    def __init__(self):
        super(MyCmd, self).__init__()
        self.prompt = ">>> "

    def emptyline(self):
        print('\r', end='')

    def do_encrypt(self, args):
        strs = args.split()
        if len(strs) == 2:
            input_file_name = strs[0] + '.bin'
            output_file_name = strs[1] + '.bin'
            try:
                file_plain = open(input_file_name, 'rb')
            except IOError as err:
                print("Open File Error:" + str(err))
                return

            # generate middle file
            file_tmp = open('__tmp__', 'wb')
            sha1_obj = SHA1.new()
            while True:
                plain = file_plain.read(16)
                if not plain:
                    break
                if len(plain) < 16:
                    plain = plain.ljust(16, b'\xFF')
                sha1_obj.update(plain)
                file_tmp.write(plain)

            # append sha1 in Plain IMG
            sha1 = sha1_obj.digest()
            sha1 = sha1.ljust(32, b'\xFF')
            file_tmp.write(sha1[0:16])
            file_tmp.write(sha1[16:32])
            file_tmp.flush()
            file_tmp.close()
            file_plain.close()

            # generate output file
            aes_obj = AES.new(KEY, AES.MODE_ECB)
            file_tmp = open('__tmp__', 'rb')
            file_cypher = open(output_file_name, 'wb')
            while True:
                plain = file_tmp.read(16)
                if not plain:
                    break
                encrypt = aes_obj.encrypt(plain)
                file_cypher.write(encrypt)

            file_cypher.flush()
            file_cypher.close()
            file_tmp.close()

            # delete middle file
            os.remove('__tmp__')

            output_file_name = output_file_name + " Generate Complete"
            print(output_file_name)
        else:
            print("Syntax error")

    def help_encrypt(self):
        print("encrypt [plain img file name] [encrypt img file name]\n"
              "Encrypt and Sign the firmware binary file\n"
              "e.g.: encrypt input output\n"
              "\tGenerate output.bin file based on input.bin file")

    def do_quit(self, args):
        exit(0)

    def help_quit(self):
        print("quit\n"
              "Quit this application")


def main():
    myca = MyCmd()
    myca.cmdloop(intro="Encrypt Tool")


if __name__ == "__main__":
    main()
