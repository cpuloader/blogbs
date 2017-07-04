# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TextToSay',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('text_to_say', models.TextField(verbose_name='Текст', max_length=800)),
                ('file_to_play', models.FileField(upload_to='speaker_mp3s')),
                ('expires', models.DateTimeField(verbose_name='Действует до', default=datetime.datetime.now)),
                ('auto_next', models.BooleanField(verbose_name='Зациклить', default=False)),
            ],
        ),
    ]
