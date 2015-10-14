class BadCiph:
    def __init__(self, pkey="dumb"):
        self.pkey = pkey

    def encrypt(self, plaintext):
        return plaintext.encode("rot13")

    def decrypt(self, ciphertext):
        return ciphertext.decode("rot13")


