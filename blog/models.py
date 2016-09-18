#coding: utf-8
from django.db import models
from django.core.urlresolvers import reverse
from datetime import datetime

class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name=unicode('Заголовок', 'utf-8')) # заголовок поста
    datetime = models.DateTimeField(default = datetime.now, db_index = True, verbose_name=unicode('Дата публикации', 'utf-8')) # дата публикации
    content = models.TextField(max_length=10000, verbose_name=unicode('Основной текст', 'utf-8')) # текст поста

    class Meta:
        ordering = ["-datetime"]

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        #return "/blog/%i/" % self.id
        return reverse("post_detail", kwargs = {"pk": self.pk})
