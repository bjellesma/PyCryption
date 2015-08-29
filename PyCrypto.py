from Crypto import Random
from Crypto.Cipher import AES
import Tkinter
import tkFileDialog
import tkMessageBox

#symetric key for encrypting and decrypting
key = b'\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18'

"""
add padding to make the string look like a feasible block size
"""
#the b"\0" returns the binary of the char
#aes.block_size is built in from our import
def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

"""
function to encrypt the string using AES256
"""
#since this is symetric encryption, we only need one key
def encrypt(message, key, key_size=256):
    message = pad(message) #pad message up to a string sizze of 256 bytes
    initVector = Random.new().read(AES.block_size) #initialization vector to prevent repitious encryption. this encryption makes the hash patternless so that it is impossible to find break encryption on any sort of pattern
    cipher = AES.new(key, AES.MODE_CBC, initVector) #create the cipher object to encrypt with
    return initVector + cipher.encrypt(message) #return the full, ciphertext version of the string

"""
function to decrypt ciphertext
"""
def decrypt(cipherText, key):
    initVector = cipherText[:AES.block_size] #the initialization vector will be the first part of the encrypted hash
    cipher = AES.new(key, AES.MODE_CBC, initVector) #create the cipher object to decrypt with, notice this code is also present in the encrypt function
    plainText = cipher.decrypt(cipherText[AES.block_size:]) #decrypt the actual cipher, which is the part after the init vector
    return plainText.rstrip(b"\0") #take out the padded characters in order to get the original text

#you can use the following lines to test this
message = "secret"
enc = encrypt(message, key)
dec = decrypt(enc, key)
print dec
