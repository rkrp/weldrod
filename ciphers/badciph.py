
metachall = {
        'name'      : 'Bad Ciph',
        'author'    : 'gtux',
        'email'     : '***@gtux.in',
        'web'       : 'https://gtux.in',
        'comments'  : 'Meh. Nothing much to see here',
        }

class Start:
	def __init__(self):
	    self.mainclass = BadCiph

class BadCiph:
    def __init__(self, pkey="dumb"):
        self.pkey = pkey

    def encrypt(self, plaintext, key):
        return plaintext.encode("rot13")

    def decrypt(self, ciphertext, key):
        return ciphertext.decode("rot13")
