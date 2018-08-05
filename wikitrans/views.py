#-*- coding: utf-8 -*-

from django.template.loader import get_template
#from django.template import Context
from django.http import HttpResponse
from django.conf import settings
from django.template.context_processors import csrf
from django.shortcuts import render_to_response

from wikitrans import *
from models import WikitrDemo, WikitrHistory

from utils import cyr2lat

import datetime, codecs, os

#def wikitranslatorshort(request, req):
#    reques.GET['req'] = req
#    wikitranslator(request)

header = {'ru': u'translate', 'en': u'перевод'}
translation_wasnt_found = {'ru': u"Эх, перевод не найден",
                           'en': "Sorry, translation wasn't found"}
versions_header_text = {'ru': u'Возможно, Вы имели в виду что-то из нижеперечисленного:',
                        'en': 'Maybe you meant something from the following:'}
message_text = {'ru': u'Добрый день',
                'en': 'Have a good day'}
translation_direction = {'ru': u'Направление перевода',
                         'en': 'Translation direction'}
translate_button_text = {'ru': u'перевести',
                         'en':' translate'}

def wikiperevod(request, req=''):                         
    return wikitranslator(request, req, 'en', 'ru')

def wikitranslator(request, req='', fromlang='ru', tolang='en'):
    global header, translation_wasnt_found, versions_header_text, greeting_text
    t = get_template('wikitranslator.html')
    text_lang = tolang #сообщения должны выводиться на языке tolang
    if not text_lang in header: text_lang = 'en' #язык по умолчанию - английский
    ctx = {'header' : header[text_lang],
           'show_form' : 'show',
           'show_table' : 'hidden', 'show_req' : 'show', 'show_trans' : 'show', 'show_redir' : 'hidden',
           'show_versions' : 'hidden', 'versions': {},
           'fromlang' : fromlang,
           'tolang' : tolang,
           'translattion_direction' : translation_direction[text_lang],
           'translate_button_text' : translate_button_text[text_lang],}
    history = None

    if 'req' in request.GET:
        req = request.GET['req']
        history = WikitrHistory(create_date = datetime.date.today(), client_ip = request.META['REMOTE_ADDR'], fromLang = fromlang, toLang = tolang, word = req)
        history.save()
    else:   
        rWord = WikitrDemo.objects.filter(**{'fromLang': fromlang, 'toLang': tolang}).order_by('?').first()
        req = rWord.word if rWord else ''

    ctx['thumbnail_show'] = 'none' # default value
    if req!='':
        ctx['show_table']='show'        
        reqWord = req
        wt = Wikitrans(fromlang, tolang)
        if wt.translate(reqWord):                        
            thumb = wt.getTranslatedThumbnail()
            if thumb and thumb.get('original'):
                ctx['thumbnail_show'] = 'block'
                ctx['thumbnail_url'] = thumb['original']
            if history != None:
                history.success = 'y'
                history.save()
            #text = 'Request: '+reqWord+r'<br/>' + 'Translation: '+wt.translation            
            ctx['request_text']=r'<span>' + reqWord + r' <a href="' + wt.fromWiki + reqWord + r'" target="_blank">&#127759;</a></span>'
            ctx['translation_text']=r'<a href="%s" target="_blank">%s</a>' % (wt.toWiki+wt.translation, wt.translation)
            if wt.redirect_from:
                ctx['show_redir']='show'
                ctx['redirected_text']=wt.redirect_from
        else:
            ctx['request_text']=reqWord            
            ctx['translation_text']=translation_wasnt_found[text_lang]
            ctx['versions_header_text']=versions_header_text[text_lang]
            if wt.versions:
                if history != None:
                    history.success = 'v'
                    history.save()
                ctx['show_versions']='show'
                versions = []
                for v in wt.versions:
                    versions = versions + [v]
                ctx['versions']=versions
        #saving reqWord to log
        LogReq(request, reqWord, wt.versions)

    else:
      ctx['text'] = message_text[text_lang]
    html = t.render(ctx)
    return HttpResponse(html)

def LogReq(request, reqWord, found):
    now = datetime.datetime.now()
    reqLogFile = codecs.open('reqlog.txt', 'a', 'utf-8')
    reqLogFile.write('\n');
    reqLogFile.write(now.strftime("%Y-%m-%d %H:%M")+'\n')
    reqLogFile.write(request.META['HTTP_USER_AGENT']+'\n')
    reqLogFile.write(request.META['REMOTE_ADDR']+'\n')
    reqLogFile.write(reqWord+'\n')
    if found:
        reqLogFile.write('*found versions*\n')            
    else:
        reqLogFile.write('*not found*\n')
    reqLogFile.close()
    
def translateListElem(wt, reqWord, recursive=True, strict=False):
    if not reqWord: return ''
    if wt.translate(reqWord):
        return r'<a href="%s">%s</a>' % (wt.toWiki+wt.translation, wt.translation)
    else:        
        if wt.versions:
            vers = ''
            for v in wt.versions:
                if vers: vers = vers + r', '
                vers = vers + translateListElem(wt, v, False)
            return reqWord + r' {<a href="/wikitranslator?req=%s">vers</a>: %s}' % (reqWord, vers)
        else:
            if not recursive:
                return cyr2lat(reqWord) if not strict else ''
                #return reqWord + r' (%s)' % cyr2lat(reqWord)    
            else:
                ans2 = ''
                for r in reqWord.split(' '):
                    if ans2: ans2 = ans2 + ' '
                    ans2 = ans2 + translateListElem(wt, r, False, True)
                return reqWord + r' (%s) [%s]' % (cyr2lat(reqWord), ans2)
    
def wikitranslatorlist(request, reqlist='', fromlang='ru', tolang='en'):
    global header, translation_wasnt_found, versions_header_text, greeting_text
    t = get_template('wikitranslatorlist.html')
    text_lang = tolang #сообщения должны выводиться на языке tolang
    if not text_lang in header: text_lang = 'en' #язык по умолчанию - английский
    ctx = {'header' : header[text_lang],
           'show_form' : 'show',
           'show_table' : 'hidden', 'show_req' : 'show', 'show_trans' : 'show', 'show_redir' : 'hidden',
           'show_versions' : 'hidden', 'versions': {},
           'fromlang' : fromlang,
           'tolang' : tolang,
           'translattion_direction' : translation_direction[text_lang],
           'translate_button_text' : translate_button_text[text_lang],
           'redirected_text' : '',
           'translation_text' : ''}
    if 'reqlist' in request.POST:
        reqlist = request.POST['reqlist']        
    #if 'tolang' in request.GET:
    #    tolang = request.GET['tolang']
    #if 'fromlang' in request.GET:
    #    fromlang = request.GET['fromlang']        
    ctx['show_table'] = 'show'
    ctx['request_text'] = '(list)'
    wt = Wikitrans(fromlang, tolang)
    LogReq(request, reqlist, False)
    reqlist = reqlist.replace("\r","")
    for req in reqlist.split("\n"):        
        ans = ''
        for reqpart in req.split(","):
            if not reqpart: continue            
            if ans: ans = ans + ', '
            ans = ans + translateListElem(wt, reqpart)
            #saving reqWord to log
            #LogReq(request, reqWord, wt.versions)
        ctx['translation_text'] = ctx['translation_text'] + ans + r'<br/>'
    # рендерим шаблон        
    ctx.update(csrf(request))
    html = t.render(ctx)
    return HttpResponse(html)
    
#FTW
def translate(request):
    return request
    
def main(request):
    with open(os.path.join(settings.BASE_DIR,'static/main.html'), 'rU') as f:
        html = f.read()    
    return HttpResponse(html)
