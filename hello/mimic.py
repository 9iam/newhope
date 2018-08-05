#-*- coding: utf-8 -*-

from random import randint

CAPITALS = set([u'А',u'Б',u'В',u'Г',u'Д',u'Е',u'Ж',u'З',u'И',u'К',u'Л',u'М',u'Н',u'О',u'П',u'Р',u'С','Т','У','Ф','Х','Ц','Ч','Ш','Щ','Я','"','-']) #set(open('rus-capitals-unicode.txt').read().split())

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

def make_title(dct, q):
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