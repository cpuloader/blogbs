# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tempurls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tempurl',
            name='text',
            field=models.CharField(default=b'a19c0', max_length=32, verbose_name='\u0421\u043b\u0443\u0447\u0430\u0439\u043d\u044b\u0439 \u0442\u0435\u043a\u0441\u0442'),
        ),
        migrations.AlterField(
            model_name='tempurl',
            name='url_hash',
            field=models.CharField(default=b'deff479d', unique=True, max_length=32),
        ),
    ]
