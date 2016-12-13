#coding: utf-8
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.translation import ugettext_lazy as _

class UserExtraFields(models.Model):
    user = models.OneToOneField(User)
    text = models.TextField(max_length=255, verbose_name=_(u'Пара слов о себе'))

    def __unicode__(self):
        return self.user.username

class Post(models.Model):
    author = models.ForeignKey(User,editable=False)
    title = models.CharField(max_length=255, verbose_name=_(u'Заголовок')) # заголовок поста
    datetime = models.DateTimeField(default = datetime.now, db_index = True, editable=False, verbose_name=_(u'Дата публикации')) # дата публикации
    content = models.TextField(max_length=10000, verbose_name=_(u'Основной текст')) # текст поста

    class Meta:
        ordering = ["-datetime"]

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs = {"pk": self.pk})
