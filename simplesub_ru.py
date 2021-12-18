'''
implements simple substitution cipher
Author: James Lyons 
Created: 2012-04-28
'''

import re

class Cipher(object):
    def encipher(self,string):
        return string
        
    def decipher(self,string):
        return string
        
    def a2i(self,ch):
        ch = ch.upper()
        #АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ
        arr = {'А':0,'Б':1,'В':2,'Г':3,'Д':4,'Е':5,'Ё':6,'Ж':7,'З':8,'И':9,'Й':10,
           'К':11,'Л':12,'М':13,'Н':14,'О':15,'П':16,'Р':17,'С':18,'Т':19,'У':20,
           'Ф':21,'Х':22,'Ц':23,'Ч':24,'Ш':25,'Щ':26,'Ъ':27,'Ы':28,'Ь':29,'Э':30,'Ю':31,'Я':32}
        return arr[ch]

    def i2a(self,i):
        i = i%33
        arr = ('А','Б','В','Г','Д','Е','Ё','Ж','З','И','Й','К','Л','М','Н','О','П','Р','С','Т','У','Ф','Х','Ц','Ч','Ш','Щ','Ъ','Ы','Ь','Э','Ю','Я')
        return arr[i]
        
    def remove_punctuation(self,text,filter='[^А-Я]'):
        return re.sub(filter,'',text.upper())

class SimpleSubstitution(Cipher):
    """The Simple Substitution Cipher has a key consisting of the letters A-Z jumbled up.
    e.g. 'AJPCZWRLFBDKOTYUQGENHXMIVS'
    This cipher encrypts a letter according to the following equation::

        plaintext =  ABCDEFGHIJKLMNOPQRSTUVWXYZ
        ciphertext = AJPCZWRLFBDKOTYUQGENHXMIVS

    To convert a plaintext letter into ciphertext, read along the plaintext row until the desired
    letter is found, then substitute it with the letter below it. For more information see http://www.practicalcryptography.com/ciphers/simple-substitution-cipher/.
    
    :param key: The key, a permutation of the 26 characters of the alphabet.
    """           
    def __init__(self,key='ГЬЯФЫИЁЭЮАНУРОЛЗЦШВЧЙЖДПМКЪБЩСТЕХ'):
        assert len(key) == 33
        self.key = [k.upper() for k in key]
        self.invkey = ''

    def encipher(self,string,keep_punct=False):
        """Encipher string using Simple Substitution cipher according to initialised key.

        Example::

            ciphertext = SimpleSubstitution('AJPCZWRLFBDKOTYUQGENHXMIVS').encipher(plaintext)     

        :param string: The string to encipher.
        :param keep_punct: if true, punctuation and spacing are retained. If false, it is all removed. Default is False. 
        :returns: The enciphered string.
        """       
        if not keep_punct: string = self.remove_punctuation(string)
        ret = ''
        for c in string.upper():
            if c.isalpha(): ret += self.key[self.a2i(c)]
            else: ret += c
        return ret    

    def decipher(self,string,keep_punct=False):
        """Decipher string using Simple Substitution cipher according to initialised key.

        Example::

            plaintext = SimpleSubstitution('AJPCZWRLFBDKOTYUQGENHXMIVS').decipher(ciphertext)     

        :param string: The string to decipher.
        :param keep_punct: if true, punctuation and spacing are retained. If false, it is all removed. Default is False. 
        :returns: The deciphered string.
        """       
        # if we have not yet calculated the inverse key, calculate it now
        if self.invkey == '':
            for i in 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ': 
                self.invkey += self.i2a(self.key.index(i))
        if not keep_punct: string = self.remove_punctuation(string)
        ret = ''      
        for c in string.upper():
            if c.isalpha(): ret += self.invkey[self.a2i(c)]
            else: ret += c
        return ret
        
if __name__ == '__main__': 
    print('use "import pycipher" to access functions')
