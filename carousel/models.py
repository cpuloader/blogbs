#coding: utf-8
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_delete
from django.dispatch import receiver

from PIL import Image

class Picture(models.Model):
    title = models.CharField(max_length=200, verbose_name=u'Заголовок'.encode('utf-8'))
    text = models.TextField(verbose_name=u'Текст описания'.encode('utf-8'))
    created_date = models.DateTimeField(default=timezone.now, db_index = True, verbose_name=u'Дата'.encode('utf-8'))
    picture = models.ImageField(verbose_name=u'Фото'.encode('utf-8'))

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        try:
            this_record = Picture.objects.get(pk = self.pk)
            if this_record.picture != self.picture:
                this_record.picture.delete(save = False)
        except:
            pass
        super(Picture, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super(Picture, self).delete(*args,**kwargs)


@receiver(post_delete, sender=Picture)
def photo_post_delete_handler(sender, **kwargs):
    picture = kwargs['instance']
    storage, path = picture.picture.storage, picture.picture.path
    print(picture.picture.path)
    storage.delete(path)
        
