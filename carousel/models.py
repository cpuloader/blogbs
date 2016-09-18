#coding: utf-8
from django.db import models
from django.utils import timezone
from PIL import Image

class Picture(models.Model):
    title = models.CharField(max_length=200, default=None, blank=True, null=True, verbose_name=u'Заголовок')
    text = models.TextField(default=None, blank=True, null=True, verbose_name=u'Текст описания')
    created_date = models.DateTimeField(default=timezone.now, db_index = True, verbose_name=u'Дата')
    picture = models.ImageField(default=None, blank=True, null=True, verbose_name=u'Фото')

    def __unicode__(self):
        return self.title

