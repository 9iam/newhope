#-*- coding: utf-8 -*-

from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse

from mimicu import load_dct, make_title, make_text, get_runglish_words
from models import HelloStory
from datetime import datetime

from django.shortcuts import redirect
 
import logging # <- not working

from django.conf import settings
import os

logger = logging.getLogger(__name__)
module_dir = os.path.dirname(__file__)

def runglish(request):
    t = get_template('hello.html')    
    dct = load_dct(os.path.join(module_dir, 'mimic-unicode.txt'))
    header = 'Runglish mini-dict'
    text = ", ".join(get_runglish_words(dct))
    html = t.render(Context({'header': header, 'text': text}))
    return HttpResponse(html)
    
def hello(request, id=None):    
    if id == 0:
        t = get_template('hello.html')
        html = t.render({'header': 'Error', 'text': 'Hi, how are you today?'})
        return HttpResponse(html)
    elif id > 0:
        story = HelloStory.objects.get(id=id)
        t = get_template('hello.html')
        html = t.render({'header': story.header, 'text': story.body})
        return HttpResponse(html)
    else:
        dct = load_dct(os.path.join(module_dir, 'mimic-unicode.txt'))
        header = make_title(dct, 3, 19)
        text = make_text(dct, 100)

        story = HelloStory(create_date = datetime.today(), client_ip = request.META['REMOTE_ADDR'], header = header, body = text)
        story.save()

        logger.info('story =', story)

        if story.id is None:
            story.id = 0             
            logger.error('story.id is None!', story)

        return redirect('/hello/' + str(story.id))

def poem(request):
    with open(os.path.join(settings.BASE_DIR,'static/poem.html'), 'rU') as f:
        html = f.read()    
    return HttpResponse(html)