#coding: utf-8
import hashlib, random
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

class TempUrl(models.Model):
    url_hash = models.CharField(default = "def" + hashlib.sha1(str(random.random())).hexdigest()[:5], 
                                 max_length=32, unique = True)
    expires = models.DateTimeField(verbose_name=_(u'Действует до'))
    text = models.CharField(default = hashlib.sha1(str(random.random())).hexdigest()[:5], 
                 max_length=32, verbose_name=_(u'Случайный текст'))

    def __unicode__(self):
        return self.url_hash


