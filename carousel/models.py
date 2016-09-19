#coding: utf-8
from django.db import models
from django.utils import timezone
from PIL import Image

class Picture(models.Model):
    title = models.CharField(max_length=200, verbose_name=u'Заголовок')
    text = models.TextField(verbose_name=u'Текст описания')
    created_date = models.DateTimeField(default=timezone.now, db_index = True, verbose_name=u'Дата')
    picture = models.ImageField(verbose_name=u'Фото')

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Picture, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super(Picture, self).delete(*args,**kwargs)
        if self.picture:
            storage, path = self.picture.storage, self.picture.path
            storage.delete(path)
