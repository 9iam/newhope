# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class HelloStory(models.Model):
    id = models.AutoField(primary_key=True)
    create_date = models.DateField()
    client_ip = models.CharField(max_length=25)
    header = models.CharField(max_length=100)
    body = models.CharField(max_length=1000)
    class Meta:
        db_table = u'hello_story'