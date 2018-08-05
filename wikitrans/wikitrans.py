#-*- coding: windows-1251 -*-

#version: 1.2, 3.07.2011
#several bugs fixed
#version: 1.3, 11.07.2011
#multiple languages added

from wikitools import *
import sys

class Wikitrans:
    reqWord = u''
    #reqWord = 'Christmas'
    toLang = "ru"
    fromLang = "en"    
    site = None
    translation_site = None
    cat = None
    versions = None
    redirect = None
    translation = ""
    url, translation_url = None, None
    fromWiki, toWiki = None, None
    redirect_from, redirect_to = None, None
    
    def __init__(self, fromLang, toLang):
        self.fromLang = fromLang
        self.toLang = toLang
        # api urls
        apiurl = "https://"+fromLang+".wikipedia.org/w/api.php"
        translation_apiurl = "https://"+toLang+".wikipedia.org/w/api.php"
        # site and translation site for api calls
        self.site = wiki.Wiki(apiurl)
        self.translation_site = wiki.Wiki(translation_apiurl) # is not widely used
        #fromWiki: used for links
        self.fromWiki = ''.join((self.site.domain,'/wiki/'))
        #toWiki: used for links
        self.toWiki = ''.join((self.translation_site.domain,'/wiki/'))
        
    def getTranslatedThumbnail(self):
        return self.__gethumbnail(self.translation_site, self.translation)
        
    def __gethumbnail(self, site, word):
        params = {'action': 'query', 'prop': 'pageimages', 'format': 'json', 'piprop': 'original', 'titles': word}
        request = api.APIRequest(site, params)
        respond = request.query()['query']        
        try:
            pageid = respond['pages'].values()[0]['pageid']
        except:
            return(False)
        return respond['pages'].get(str(pageid)).get('thumbnail')
        
    def translate(self, word, quick=False):
        reqWord = word.capitalize()        
        params = {'action':'query','titles':reqWord, 'prop':'langlinks', 'lllimit':100, 'redirects':''}
        request = api.APIRequest(self.site, params)        
        
        #инициализация
        self.translation = ""
        self.versions = []

        #попытка открыть страницу
        respond = request.query()['query']        
        try:
            pageid = respond['pages'].values()[0]['pageid']
        except:
            return(False)

        #request2 = api.APIRequest(site,{'action':'query','titles':reqWord,'prop':'langlinks','lllimit':100})
        #respond = request2.query()['query']['pages']

        #print 'Query: ' +  reqWord

        translation_ru = "" #xm
        translation_en = "" #xmm
        self.translation = ""
        pageinfo = respond['pages'][str(pageid)]        
        if 'langlinks' in pageinfo:
            #print pageinfo['langlinks']
            langlinks = pageinfo['langlinks']
            for ll in langlinks:
                #print ll['lang']
                if ll['lang']=='ru':
                    #print 'Russian term found!'              
                    url = ll['*']   
                    translation_ru = url
                if ll['lang']=='en':
                    #print 'English term found!'
                    url = ll['*']   
                    translation_en = url   
                if ll['lang']==self.toLang:
                    url = ll['*']   
                    self.translation = url                   
        else:
            #print 'langlinks not found'
            #print pageinfo            
            pass
            
        #was it a debug?
        #if self.toLang == 'en': self.translation = translation_en
        #else: self.translation = translation_ru    
        
        #wat's this?..
        #urlbits = urlparse(translation_apibase)
        #print urlbits #debug
        #translation_domain = '://'.join([urlbits.scheme, urlbits.netloc])
        #selft.translation_url = ''.join(translation_domain,'/wiki/',self.translation)
        
        #normalization:        
        if 'normalized' in respond:            
            norm = respond['normalized'][0]
            reqWord = norm['to']
            
        #redirects:
        if 'redirects' in respond:
            redirects = respond['redirects'][0]
            self.redirect_from = redirects['from']
            self.redirect_to = redirects['to']
            reqWord = self.redirect_to
        else:
            self.redirect_from = ""
            self.redirect_to = ""
        
        if quick: return(self.translation)
            
        #categories:
        lst = pagelist.listFromQuery(self.site, respond['pages'])
        ##print 'lst:', lst
        p = lst[0]
        self.url = ''.join((self.site.domain, '/wiki/', p.urltitle))
        ##print ''.join(('Title: ', p.title))
        ##print ''.join(('URL: ', p_url))
        self.cat = p.getCategories()

        #versions:
        params2 = {'action': 'query', 'titles': reqWord,'rnnamespace': 0, 'prop': 'links', 'pllimit': 50}
        request2 = api.APIRequest(self.site,params2)
        respond2 = request2.query()['query']        
        try:
            pageinfo = respond2['pages'][str(p.pageid)]            
            links = pageinfo['links']        
            for l in links:
                url = l['title']
                if url.startswith(reqWord) and url!=reqWord:
                    self.versions = self.versions + [url]
        except:
            pass
                
        if self.translation == "": return(False)
        else: return(True)

#request2 = api.APIRequest(site,{'action':'query','titles':rword,'prop':'langlinks','lllimit':100,'format':'json'})
#llinfo = request2.query()['query']['pages'][str(p.pageid)]
#print llinfo