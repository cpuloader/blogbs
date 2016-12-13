#coding: utf-8
import mimetypes
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

class Track(models.Model):
    author = models.ForeignKey(User, blank=False)
    title = models.CharField(max_length=200, verbose_name=_(u'Заголовок'))
    text = models.TextField(verbose_name=_(u'Текст описания'))
    created_date = models.DateTimeField(default=timezone.now, db_index = True, verbose_name=_(u'Дата'))
    soundtrack = models.FileField(upload_to='audio', verbose_name=_(u'Трек'),  blank=False)

    class Meta:
        ordering = ["-created_date"]

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        try:
            this_record = Track.objects.get(pk = self.pk)
            if this_record.soundtrack != self.soundtrack:
                this_record.soundtrack.delete(save = False)
        except:
            pass
        super(Track, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super(Track, self).delete(*args,**kwargs)

    @property
    def mimetype(self):
        if not hasattr(self, '_mimetype'):
            self._mimetype = mimetypes.guess_type(self.soundtrack.path)[0]
        return self._mimetype

    @property
    def snd_filetype(self):
        if '/' in self.mimetype:
            type_names = {'mpeg': 'MP3', 'ogg': 'Ogg Vorbis'}
            snd_filetype = self.mimetype.split('/')[1]
            return type_names.get(snd_filetype, snd_filetype)
        else:
            return self.mimetype

@receiver(post_delete, sender=Track)
def track_post_delete_handler(sender, **kwargs):
    track = kwargs['instance']
    storage, path = track.soundtrack.storage, track.soundtrack.path
    storage.delete(path)
