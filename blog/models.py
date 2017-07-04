#coding: utf-8
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.translation import ugettext_lazy as _


class Post(models.Model):
    author = models.ForeignKey(User, editable=False)
    title = models.CharField(max_length=255, verbose_name=_(u'Заголовок')) # заголовок поста
    datetime = models.DateTimeField(default = datetime.now, db_index = True, 
           editable=False, verbose_name=_(u'Дата публикации')) # дата публикации
    content = models.TextField(max_length=10000, verbose_name=_(u'Текст')) # текст поста

    class Meta:
        ordering = ["-datetime"]

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs = {'pk': self.pk})

class Comment(models.Model):
    parent_post = models.ForeignKey(Post, related_name='comments', verbose_name = _(u'Блог'))
    author = models.ForeignKey(User)
    #author = models.CharField(max_length=50, verbose_name = _(u'Автор'))
    content = models.TextField(verbose_name = _(u'Текст комментария'))
    datetime = models.DateTimeField(default = datetime.now, editable=False, 
         verbose_name = _(u'Опубликовано'))

    class Meta:
        ordering = ['datetime']
        #verbose_name = u'комментарий блога'
        #verbose_name_plural = u'комментарии блога'

    def __unicode__(self):
        if len(self.content) > 20:
            return self.content[:20] + '..'
        else:
            return self.content

    def __str__(self):
        if len(self.content) > 20:
            return self.content[:20] + '..'
        else:
            return self.content

    def get_absolute_url(self):
        return reverse('post_detail', kwargs = {'pk': self.parent_post.pk})
