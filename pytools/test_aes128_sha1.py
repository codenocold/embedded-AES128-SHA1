# !! Install pycryptodome Package
from Crypto.Cipher import AES
from Crypto.Hash import SHA1

KEY = b'1234567890123456'

file_input = open('Input.bin', 'rb')

file_plain = open('Plain.bin', 'wb')
file_cypher = open('Cypher.bin', 'wb')

aes_obj = AES.new(KEY, AES.MODE_ECB)
sha1_obj = SHA1.new()

# generate Plain.bin
while True:
    plain = file_input.read(16)
    if not plain:
        break
    if len(plain) < 16:
        plain = plain.ljust(16, b'\xFF')
    sha1_obj.update(plain)
    file_plain.write(plain)

# append sha1 in Plain.bin
sha1 = sha1_obj.digest()
sha1 = sha1.ljust(32, b'\xFF')
file_plain.write(sha1[0:16])
file_plain.write(sha1[16:32])
file_plain.flush()
file_plain.close()
file_input.close()

# generate Cypher.bin
file_plain = open('Plain.bin', 'rb')
while True:
    plain = file_plain.read(16)
    if not plain:
        break
    encrypt = aes_obj.encrypt(plain)
    file_cypher.write(encrypt)

file_cypher.flush()
file_cypher.close()
file_plain.close()
