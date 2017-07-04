# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(verbose_name='Заголовок', max_length=200)),
                ('text', models.TextField(verbose_name='Текст описания')),
                ('created_date', models.DateTimeField(verbose_name='Дата', default=django.utils.timezone.now, db_index=True)),
                ('picture', models.ImageField(verbose_name='Фото', upload_to='')),
            ],
        ),
    ]
