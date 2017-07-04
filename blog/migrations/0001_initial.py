# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('content', models.TextField(verbose_name='Текст комментария')),
                ('datetime', models.DateTimeField(verbose_name='Опубликовано', default=datetime.datetime.now, editable=False)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['datetime'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(verbose_name='Заголовок', max_length=255)),
                ('datetime', models.DateTimeField(verbose_name='Дата публикации', default=datetime.datetime.now, editable=False, db_index=True)),
                ('content', models.TextField(verbose_name='Текст', max_length=10000)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False)),
            ],
            options={
                'ordering': ['-datetime'],
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='parent_post',
            field=models.ForeignKey(to='blog.Post', verbose_name='Блог', related_name='comments'),
        ),
    ]
