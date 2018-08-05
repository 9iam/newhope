#-*- coding: utf-8 -*-

from random import randint

CAPITALS = set(['А','Б','В','Г','Д','Е','Ж','З','И','К','Л','М','Н','О','П','Р','С','Т','У','Ф','Х','Ц','Ч','Ш','Щ','Я']) #set(open('rus-capitals-unicode.txt').read().split())
BADSIGNES = set(['.',','])

RUNGLISH_LETTERS = set(['А','а','В','Е','e','З','з','К','к','М','м','Н','н','О','о','Р','р','С','с','Т','т','У','у','Х','х','Ь','ь'])

def load_dct(fn):
    dct = {}
    f=open(fn,'r')
    s=f.read()
    a=s.split()
    i = 0
    #обрабатываем все слова, кроме последнего
    while i < len(a)-1:
        if a[i] in dct:
            dct[a[i]].append(a[i+1])
        else:
            dct[a[i]]=[a[i+1]]
        i = i + 1
    #обрабатываем последне слово
    if not a[i] in dct:
        dct[a[i]]=[a[0]]
    return dct
    
def isRunglishWord(word):    
    for c in word:
        if not c in RUNGLISH_LETTERS:
            return False
    return True

def get_runglish_words(dct):
    result = []    
    for key in dct.keys():
        if isRunglishWord(key):
            result.append(key)
    return result
    
def make_text(dct, q):
    s = ''
    #print dct.values()
    dct_keys = dct.keys()
    #print 'dct_keys='+", ".join(dct_keys)
    key = dct_keys[randint(0,len(dct_keys)-1)]
    dotFound = False
    capFound = False
    while (q>0) or (not dotFound):
        #print 'picked up: [%s]'%", ".join(dct[key])
        if q<=0: dotFound=key[-1]=='.'
        if capFound or (key[0:2] in CAPITALS):
            s = s + key + ' '
            q = q - 1
            capFound = True
        linked_keys=dct[key]
        if len(linked_keys)>0:
            key = linked_keys[randint(0,len(linked_keys)-1)]
        else:
            key = dct_keys[randint(0,len(dct_keys)-1)]
    return s

def make_title(dct, q, r):
    s=''
    while s=='': s=make_title_unsafe(dct, q)
    #если получили заголовок длиннее r символов, удаляем последнее слово
    #*2 из-за юникода
    if len(s)>r*2: s=' '.join(s.split()[0:-1])
    #удаляем лишний знак препинания в конце заголовка
    if s[-2:] in BADSIGNES: s=s[0:-2]
    return s
    
def make_title_unsafe(dct, q):
    s = ''
    dct_keys = dct.keys()
    #print 'dct_keys='+", ".join(dct_keys)
    key = dct_keys[randint(0,len(dct_keys)-1)]
    capFound = False
    while q>0:
        if capFound or (key[0:2] in CAPITALS):
            s = s + key + ' '
            q = q - 1
            capFound = True
        linked_keys=dct[key]
        if len(linked_keys)>0:
            key = linked_keys[randint(0,len(linked_keys)-1)]
        else:
            key = dct_keys[randint(0,len(dct_keys)-1)]
        if key[-1]=='.': break
    return s

def make_string(dct, q):
    s = ''
    #print dct.values()
    dct_keys = dct.keys()
    #print 'dct_keys='+", ".join(dct_keys)
    key = dct_keys[randint(0,len(dct_keys)-1)]
    while q>0:
        #print 'picked up: [%s]'%", ".join(dct[key])
        s = s + key + ' '
        q = q - 1
        linked_keys=dct[key]
        if len(linked_keys)>0:
            key = linked_keys[randint(0,len(linked_keys)-1)]
        else:
            key = dct_keys[randint(0,len(dct_keys)-1)]
    return s