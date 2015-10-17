#!/usr/bin/python2

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

import ciphers as cs
from ciphers import *

class Weldrod(LineReceiver):

    def __init__(self):
        self.settings = {}
        self.state = "PROMPT"
        self.MOTD = "Welcome user! You are successfully connected to server\n"
        self.prompt = "weldrod> "
        self.response_type = 'normal'
        self.ciphers = self.getCiphers()
        self.lastquery = ''
        self.params = { }
        self.settings = WeldrodSession()

    def connectionMade(self):
        print "Connection made from %s" %(self.transport.client[0])
        self.sendResponse(self.MOTD)

    def lineReceived(self, data):
        self.response_type = 'normal'
        resp = ''

        prompt_handler = {
            'help'      : self.HANDLE_help,
            'menu'      : self.HANDLE_menu,
            'encrypt'   : self.HANDLE_encrypt,
            'decrypt'   : self.HANDLE_decrypt,
            'set'       : self.HANDLE_set,
            'get'       : self.HANDLE_get,
        }

        if self.state.startswith('PROMPT'):

            try:
                cmd = data.strip().split()[0]
                resp = prompt_handler[cmd](data)
            except IndexError:
                resp = "Why u do tis??"
            except KeyError:
                resp = "Pacha Boodham! I don't understand what you are"\
		       " saying. Send 'help' for help"

        elif self.state.startswith('INPUT'):
            self.lastquery = data
            if self.state == 'INPUT_MENU':
                resp = self.HANDLE_menu_input()
                self.state = 'PROMPT'

        #Despatch the response accordingly
        if self.response_type == 'normal':
             self.sendResponse(resp)
        elif self.response_type == 'line':
            self.sendLine(resp)
        else:
            self.transport.write(resp)

    def sendResponse(self, data):
        payload = "%s\n%s" %(data, self.prompt)
        self.transport.write(payload)

    #
    #Handlers for the input from user prompt
    #

    def HANDLE_help(self, data):
        self.response_type = 'normal'
        return "I can't do anything much. Ask KRP :p"

    def HANDLE_menu(self, data):
        self.response_type = "raw"
        menu = ""
        i = 1
        for cipher in self.ciphers[:-1]:
            menu += "%2d %s\n" %(i, cipher.__name__)
            i += 1

        menu += "\nEnter your option: "
        self.state = 'INPUT_MENU'
        return menu


    def HANDLE_encrypt(self, data):
        try:
            pt = self.params['plaintext']
            key = self.params['passkey']

            if self.settings.get('hex_mode.pt') == "true":
                pt = pt.decode("hex")
            
            if self.settings.get('hex_mode.key') == "true":
                key = key.decode("hex")
        except KeyError as e:
            return "Parameter %s is not set" %(e)

        ciphertext = self.cipher.encrypt(pt, key)

        if self.settings.get('hex_mode.ct') == "true":
            return ciphertext.encode('hex')
        else:
            return ciphertext

    def HANDLE_decrypt(self, data):
        try:
            ct = self.params['ciphertext']
            key = self.params['passkey']

            if self.params['hex_mode'] == "true":
                ct = ct.decode("hex")
                key = key.decode("hex")
        except KeyError as e:
            return "Parameter %s is not set" %(e)

        plaintext = self.cipher.decrypt(ct, key)
        print plaintext
        return unicode(plaintext, 'utf-8')


    def HANDLE_set(self, data):
        args = data.strip().split()
        if len(args) < 3:
            return "Syntax error in set command!"
        prop = args[1]
        value = " ".join(args[2:])
        self.params[prop] = value
        return "Successfully set %s as %s" %(prop, value)

    def HANDLE_get(self, data):
        args = data.strip().split()
        resp = ''

        if len(args) == 1:
            for prop in self.params:
                resp += "%s\t=>\t%s\n" %(prop, self.params[prop])
            return resp
        elif len(args) == 2:
            try:
                resp += "%s\t=>\t%s\n" %(args[1], self.params[args[1]])
            except KeyError:
                resp = "%s is not set" %(args[1])
            return resp
        else:
            return "Invalid Syntax, girl."

    def HANDLE_menu_input(self):
        index = int(self.lastquery) - 1
        cipher = self.ciphers[index]

        try:
	    cipher_class = cipher.Start()
            self.cipher = cipher_class.mainclass()
	except Exception as e:
            print e
	    return "Uh oh! Something went wrong.."

        self.prompt = "%s | %s" %(cipher.__name__, self.prompt)

        resp = "Chosen cipher successfully!\n\n"
        for prop in ['name', 'author', 'email', 'web', 'comments']:
            try:
                resp += "%s\t: %s\n" %(prop,cipher.metachall[prop])
            except IndexError:
                pass
        resp += "\n"
        return resp

    #
    #Common methods
    #
    @staticmethod
    def getCiphers():
        foo = cs.__all__
        return [globals()[bar] for bar in foo]


class WeldrodSession:
	
	#Set the default session settings
	def __init__(self):
		self.storage = {}
		self.storage['hex_mode'] = {}
		self.storage['hex_mode']['pt'] = {'d_type' : str, 'value' : "false"}
		self.storage['hex_mode']['ct'] = {'d_type' : str, 'value' : "true"}
		self.storage['hex_mode']['key'] = {'d_type' : str, 'value': "true"}
		
	def set(self, data):
		try:
			update_settings(self, data)
		except SettingsKeyError:
			return "Incorrect Settings Key"
		except IncorrectTypeError:
			return "Data Type Mismatch"
	
	def update_settings(self, data):
		data = data.strip().split()
		settings_key, value = data[1], data[2]
		
		#Settings key existence check
		try:
			key = None
			for i in settings_key.split("."):
				key = self.storage[i]
		except KeyError:
			raise WeldrodSession.SettingsKeyError()
		
		if type(key) != dict:
			raise WeldrodSession.SettingsKeyError()
		
		#TypeCheck
		try:
			value = key[d_type](value)
		except Exception:
			raise WelrodSession.IncorrectTypeError()
			
		#Set the value in the key if everything is okay
		key['value'] = value
		
	def get(self, settings_key):
		try:
			key = self.storage
			for i in settings_key.split("."):
				key = key[i]
		except KeyError as e:
			raise WeldrodSession.SettingsKeyError(e)
		
		if type(key) != dict:
			raise WeldrodSession.SettingsKeyError("Uh uh")
		
		return key['value']
		
	# 
	# Exceptions
	#
	class SettingsKeyError(Exception):
		pass
		
	class IncorrectTypeError(Exception):
		pass
		
	
class WeldrodFactory(Factory):
    def buildProtocol(self, addr):
        return Weldrod()

if __name__ == '__main__':
    reactor.listenTCP(1234, WeldrodFactory())
    reactor.run()
