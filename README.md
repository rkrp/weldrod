Weldrod
================
[![Build Status](https://img.shields.io/travis/rkrp/maraithal.svg)](https://travis-ci.org/rkrp/maraithal)
[![License](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://github.com/rkrp/lsb-steganography)
[![Downloads](https://img.shields.io/pypi/dm/maraithal.svg)](https://pypi.python.org/pypi/maraithal)

Server written in Twisted for plugging in various cryptosystems dynamically.

Work in Progress.

##Installation
- Create a virtual environment in Python 2
- Clone the repository to the virtual environment
- Activate the environment and run

```
pip install -r requirements.txt
```
- Run ./server.py and voila!

##Writing Crypto Modules
Let's write a module called `BadCipher` in file `badciph.py`. 

If you prefer looking at the sample modules directly and figure it out yourself, you can try looking at [badciph.py](ciphers/badciph.py)

- Define a dictionary `metachall` with the following keys
  - name
  - author
  - email
  - web
  - comments

So, `metachall` can be defined as
```
metachall = {
        'name'      : 'Bad Ciph',
        'author'    : 'gtux',
        'email'     : 'krp@****.in',
        'web'       : 'https://gtux.in',
        'comments'  : 'A very bad cipher',
        }
```
The cryptosystem is defined in a class (say, `BadCiph`) with both `encrypt` and `decrypt` methods.

For example:
```
class BadCiph:
    def encrypt(self, plaintext, key):
        return plaintext.encode("rot13")

    def decrypt(self, ciphertext, key):
        return ciphertext.decode("rot13")
```

A class `Start` is defined by the following construct with the property `mainclass` assigned the class name of your cryptosystem. 
```
class Start:
	def __init__(self):
	    self.mainclass = BadCiph
```
