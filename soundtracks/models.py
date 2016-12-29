#coding: utf-8
import mimetypes
from datetime import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

class Track(models.Model):
    author = models.ForeignKey(User, editable=False)
    title = models.CharField(max_length=200, verbose_name=_(u'Заголовок'))
    text = models.TextField(verbose_name=_(u'Текст описания'))
    created_date = models.DateTimeField(default=timezone.now, db_index = True, editable=False, verbose_name=_(u'Дата'))
    soundtrack = models.FileField(upload_to='audio', verbose_name=_(u'Аудиофайл'),  blank=False)

    class Meta:
        ordering = ["-created_date"]

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('track_detail', kwargs = {'pk': self.pk})

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


class TrackComment(models.Model):
    parent_track = models.ForeignKey(Track, related_name='comments', verbose_name = _(u'Трек'), editable=False)
    author = models.CharField(max_length=50, verbose_name = _(u'Автор'), editable=False)
    content = models.TextField(verbose_name = _(u'Текст комментария'))
    datetime = models.DateTimeField(default = datetime.now, editable=False, 
         verbose_name = _(u'Опубликовано'))

    class Meta:
        ordering = ['datetime']

    def __unicode__(self):
        if len(self.content) > 20:
            return self.content[:20] + '..'
        else:
            return self.content

    def get_absolute_url(self):
        return reverse('track_detail', kwargs = {'pk': self.parent_track.pk})


@receiver(post_delete, sender=Track)
def track_post_delete_handler(sender, **kwargs):
    track = kwargs['instance']
    storage, path = track.soundtrack.storage, track.soundtrack.path
    storage.delete(path)
