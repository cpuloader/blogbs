# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('soundtracks', '0003_auto_20171218_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='duration',
            field=models.FloatField(blank=True, default=0),
            preserve_default=False,
        ),
    ]
