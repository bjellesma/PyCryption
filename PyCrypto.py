from Crypto import Random
from Crypto.Cipher import AES
import Tkinter
import tkFileDialog
import tkMessageBox

#symetric key for encrypting and decrypting
key = b'\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18'
#global variable for fileName
fileName = None

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
print "After going through an encryption and decryption process on " , message , ", we get back: " , dec

"""
now to make it as a gui program
"""

"""
function to encrypt a file
"""
def encrypt_file(file_name, key):
    with open(file_name, 'rb') as f: #open file and read it as binary
        plainText = f.read() #store the text as a variable
    enc = encrypt(plainText, key) #encrypt text using symmetric key
    with open(file_name + '.enc', 'wb') as f: #create a new encrypted version of the file using a .enc file extension, and write as binary
        f.write(enc) #write the encrypted ciphertext in the file that we just created
        f.close() #housekeeping

"""
function to decrypt a file
"""
def decrypt_file(file_name, key):
    with open(file_name, 'rb') as f: #open file and read it as binary
        cipherText = f.read() #store the ciphertext as a variable
    enc = decrypt(cipherText, key) #decrypt text using symmetric key
    with open(file_name[:-4], 'wb') as f: #open the original file without the enc extension
        #remember we're calling this function when we have the enc file extension
        f.write(dec) #write the decrypted text in the file that we just created
        f.close() #housekeeping

"""
function to load file
"""
def load_file():
    global key, fileName
    text_file = tkFileDialog.askopenfile(filetypes =[('Text Files', '.txt'),('Encrypted File', '.enc')]) #built in function
    if text_file.name != None: #if file was properly selected
        fileName = text_file.name #set the global variable filename to the selected file's name

"""
function to create a gui button for encryption
"""
def encrypt_file_gui():
    global key, fileName
    if fileName != None: #decrypt the file
        encrypt_file(fileName, key)
    else: #show error
        tkMessageBox.showerror(title="Error:", message="There was no file loaded for encryption")

"""
function to create a gui button for decrption
"""
def decrypt_file_gui():
    global key, fileName
    if fileName != None: #decrypt the file
        fname = fileName + '.enc' #we add the enc file extension
        decrypt_file(fname, key)
    else: #show error
        tkMessageBoxmessagebox.showerror(title="Error:", message="There was no file loaded for decryption")

#create GUI
root = Tkinter.Tk()
root.title("AES256 Encryption and Decryption") #set window

#create buttons
load_file_button = Tkinter.Button(root, text="Load", command=load_file)
load_file_button.pack()
enc_file_button = Tkinter.Button(root, text="Encrypt", command=encrypt_file_gui)
enc_file_button.pack()
dec_file_button = Tkinter.Button(root, text="Decrypt", command=decrypt_file_gui)
dec_file_button.pack()

#to start the GUI
root.mainloop()
