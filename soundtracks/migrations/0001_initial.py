# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(verbose_name='Заголовок', max_length=200)),
                ('text', models.TextField(verbose_name='Текст описания')),
                ('created_date', models.DateTimeField(verbose_name='Дата', default=django.utils.timezone.now, editable=False, db_index=True)),
                ('soundtrack', models.FileField(verbose_name='Аудиофайл', upload_to='audio')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False, on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='TrackComment',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('content', models.TextField(verbose_name='Текст комментария')),
                ('datetime', models.DateTimeField(verbose_name='Опубликовано', default=datetime.datetime.now, editable=False)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
                ('parent_track', models.ForeignKey(to='soundtracks.Track', verbose_name='Трек', related_name='comments', editable=False, on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ['datetime'],
            },
        ),
    ]
