#from pycipher import SimpleSubstitution as SimpleSub # Библиотека для работы с английским текстом 
import random
import re
from simplesub_ru import SimpleSubstitution as SimpleSub # Переделанная библиотека для работы с русским текстом
#from ngram_score import *
from math import log10

class ngram_score():
    def __init__(self,sep=' '):
        ''' load a file containing ngrams and counts, calculate log probabilities '''
        self.ngrams = {}
        file = open('russian_quadgrams.txt', 'r', encoding="utf-8") # Загружаем файлы с комбинациями и их вероятностями
        
    #    with open('russian_quadgrams.txt','r', encoding="utf-8") as file:
    #json.dump(out, file, ensure_ascii=False)
        
        for line in file:
            key,count = line.split(sep) 
            self.ngrams[key] = int(count)
        self.L = len(key)
        self.N = sum(self.ngrams.values())
        #calculate log probabilities
        for key in self.ngrams.keys():
            self.ngrams[key] = log10(float(self.ngrams[key])/self.N)
        self.floor = log10(0.01/self.N)

    def score(self,text):
        ''' compute the score of text '''
        score = 0
        ngrams = self.ngrams.__getitem__
        for i in range(len(text)-self.L+1):
            if text[i:i+self.L] in self.ngrams: score += ngrams(text[i:i+self.L])
            else: score += self.floor          
        return score

fitness = ngram_score() # load our quadgram statistics

ctext='ЪИЗВЕВРСКНКПЪТАСИКБМТДКЗНМОДКЗНАКБМЛАНРЛКЩВОВДКПЬЯНВВЧВОЗЪНА' # Шифротекст
#ctext = re.sub('[^A-Z]','',ctext.upper()) # Переводит все символы в верхний регистр

#maxkey = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ') # Алфавит
maxkey = list('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ') # Алфавит
maxscore = -99e9
parentscore,parentkey = maxscore,maxkey[:]
print ("Substitution Cipher solver, you may have to wait several iterations")
print ("for the correct result. Press ctrl+c to exit program.")
# keep going until we are killed by the user
i = 0
while 1:
    i = i+1
    random.shuffle(parentkey)
    deciphered = SimpleSub(parentkey).decipher(ctext)
    parentscore = fitness.score(deciphered)
    count = 0
    while count < 1000:
        a = random.randint(0,32) # Рандомное значение буквы из алфавита (Англ от 0 до 25)
        b = random.randint(0,32) # Рандомное значение буквы из алфавита (Англ от 0 до 25)
        child = parentkey[:]
        # swap two characters in the child
        child[a],child[b] = child[b],child[a]
        deciphered = SimpleSub(child).decipher(ctext)
        score = fitness.score(deciphered)
        # if the child was better, replace the parent with it
        if score > parentscore:
            parentscore = score
            parentkey = child[:]
            count = 0
        count = count+1
    # keep track of best score seen so far
    if parentscore>maxscore:
        maxscore,maxkey = parentscore,parentkey[:]
        print ('\nbest score so far:',maxscore,'on iteration',i)
        ss = SimpleSub(maxkey)
        print ('    best key: '+''.join(maxkey))
        print ('    plaintext: '+ss.decipher(ctext))

