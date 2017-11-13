'''
Thanks to 101100 in providing the encryption methodology

http://stackoverflow.com/questions/6425131/encrypt-decrypt-data-in-python-with-salt
'''
import json
import Crypto.Random
from Crypto.Cipher import AES
import hashlib


class AESController:

	# salt size in bytes
	SALT_SIZE = 32

	# number of iterations in the key generation
	NUMBER_OF_ITERATIONS = 20

	# the size multiple required for AES
	AES_MULTIPLE = 16

	def generate_key(self, password, salt, iterations):
	    assert iterations > 0

	    key = password + salt

	    for i in range(iterations):
	        key = hashlib.sha256(key).digest()  

	    return key

	def pad_text(self, text, multiple):
	    extra_bytes = len(text) % multiple

	    padding_size = multiple - extra_bytes

	    padding = chr(padding_size) * padding_size

	    padded_text = text + padding

	    return padded_text

	def unpad_text(self, padded_text):
	    padding_size = ord(padded_text[-1])

	    text = padded_text[:-padding_size]

	    return text

	def encrypt(self, plaintext, password):
	    salt = Crypto.Random.get_random_bytes(self.SALT_SIZE)

	    key = self.generate_key(password, salt, self.NUMBER_OF_ITERATIONS)

	    cipher = AES.new(key, AES.MODE_ECB)

	    padded_plaintext = self.pad_text(plaintext, self.AES_MULTIPLE)

	    ciphertext = cipher.encrypt(padded_plaintext)

	    ciphertext_with_salt = salt + ciphertext

	    return ciphertext_with_salt

	def decrypt(self, ciphertext, password):
	    salt = ciphertext[0:self.SALT_SIZE]

	    ciphertext_sans_salt = ciphertext[self.SALT_SIZE:]

	    key = self.generate_key(password, salt, self.NUMBER_OF_ITERATIONS)

	    cipher = AES.new(key, AES.MODE_ECB)

	    padded_plaintext = cipher.decrypt(ciphertext_sans_salt)

	    plaintext = self.unpad_text(padded_plaintext)

	    return plaintext

