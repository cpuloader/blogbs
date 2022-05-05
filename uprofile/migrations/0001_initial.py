# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserExtraFields',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('text', models.TextField(default='Я новый юзер.', verbose_name='Пара слов о себе', max_length=255, blank=True)),
                ('picture', models.ImageField(default='profile_pics/default_profile.jpg', verbose_name='Фото', upload_to='profile_pics', blank=True)),
                ('baseuser', models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
    ]
