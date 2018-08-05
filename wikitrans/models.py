# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class WikitrDemo(models.Model):
    id = models.AutoField(primary_key=True)
    fromLang = models.CharField(db_column='from', max_length=5)
    toLang = models.CharField(db_column='to', max_length=5)
    word = models.TextField()    
    class Meta:
        db_table = u'wikitranslator_demo'

class WikitrHistory(models.Model):
    id = models.AutoField(primary_key=True)
    fromLang = models.CharField(db_column='from', max_length=5)
    toLang = models.CharField(db_column='to', max_length=5)
    word = models.TextField()    
    create_date = models.DateField()
    success = models.CharField(max_length=1)
    client_ip = models.CharField(max_length=25)
    class Meta:
        db_table = u'wikitranslator_hist'