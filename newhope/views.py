#-*- coding: utf-8 -*-

from django.http import HttpResponse
from django.conf import settings
import os

def main(request):
    with open(os.path.join(settings.BASE_DIR,'static/main.html'), 'rU') as f:
        html = f.read()    
    return HttpResponse(html)