metachall = {
        'name'      : 'Good Ciph',
        'author'    : 'gtux',
        'email'     : 'krp@gtux.in',
        'web'       : 'https://gtux.in',
        'comments'  : 'Meh. Nothing much to see here',
        }

class BadCiph:
    def __init__(self, pkey="dumb"):
        self.pkey = pkey

    def encrypt(self, plaintext):
        return plaintext.encode("rot13")

    def decrypt(self, ciphertext):
        return ciphertext.decode("rot13")


