#coding: utf-8
import hashlib, random
from django.core.urlresolvers import reverse
from django.db import models


class TempUrl(models.Model):
    url_hash = models.CharField(default = "def" + hashlib.sha1(str(random.random())).hexdigest()[:5], 
                                 max_length=32, unique = True)
    expires = models.DateTimeField(verbose_name=unicode('Действует до', 'utf-8'))
    text = models.CharField(default = hashlib.sha1(str(random.random())).hexdigest()[:5], 
                 max_length=32, verbose_name=unicode('Случайный текст', 'utf-8'))

    def __unicode__(self):
        return self.url_hash


