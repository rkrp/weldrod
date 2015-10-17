
metachall = {
        'name'      : 'Ugly Ciph',
        'author'    : 'gtux',
        'email'     : 'krp@gtux.in',
        'web'       : 'https://gtux.in',
        'comments'  : 'Very Simple Ceasar Cipher Implementation',
        }

class Start:
	def __init__(self):
	    self.mainclass = CeasarCiph

class CeaserCiph:
    def __init__(self, pkey="dumb"):
        self.pkey = pkey

    def encrypt(self, plaintext, key):
        return plaintext.encode("rot13")

    def decrypt(self, ciphertext, key):
        return ciphertext.decode("rot13")
