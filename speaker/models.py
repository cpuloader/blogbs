#coding: utf-8
import mimetypes, os
from django.db import models
from datetime import datetime
from django.utils.translation import ugettext_lazy as _

class TextToSay(models.Model):
    text_to_say = models.TextField(max_length=800, verbose_name=_(u'Текст'))
    file_to_play = models.FileField(upload_to='speaker_mp3s')
    expires = models.DateTimeField(default=datetime.now, verbose_name=_(u'Действует до'))
    auto_next = models.BooleanField(default=False, blank=False, verbose_name=_(u'Зациклить'));

    def __unicode__(self):
        return self.text_to_say[0:10] + '..'

    def __str__(self):
        return self.text_to_say[0:10] + '..'

    def delete(self, *args, **kwargs):
        if self.file_to_play is not None:
            mp3_storage, mp3_path = self.file_to_play.storage, self.file_to_play.path
            mp3_storage.delete(mp3_path)
        super(TextToSay, self).delete(*args,**kwargs)

    @property
    def mimetype(self):
        if not hasattr(self, '_mimetype'):
            self._mimetype = mimetypes.guess_type(self.file_to_play.path)[0]
        return self._mimetype

    @property
    def snd_filetype(self):
        if '/' in self.mimetype:
            type_names = {'mpeg': 'MP3', 'ogg': 'Ogg Vorbis'}
            snd_filetype = self.mimetype.split('/')[1]
            return type_names.get(snd_filetype, snd_filetype)
        else:
            return self.mimetype
