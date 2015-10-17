
metachall = {
        'name'      : 'Good Ciph',
        'author'    : 'gtux',
        'email'     : 'krp@gtux.in',
        'web'       : 'https://gtux.in',
        'comments'  : 'Meh. Nothing much to see here',
        }

class Start:
	def __init__(self):
	    self.mainclass = GoodCiph

class GoodCiph:
    def __init__(self, pkey="dumb"):
        self.pkey = pkey

    def encrypt(self, plaintext, key):
        return plaintext.encode("rot13")

    def decrypt(self, ciphertext, key):
        return ciphertext.decode("rot13")
