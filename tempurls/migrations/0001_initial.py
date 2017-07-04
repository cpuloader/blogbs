# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TempUrl',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('url_hash', models.CharField(unique=True, default='def7c09b', max_length=32)),
                ('expires', models.DateTimeField(verbose_name='Действует до')),
                ('text', models.CharField(default='1cf27', verbose_name='Случайный текст', max_length=32)),
            ],
        ),
    ]
