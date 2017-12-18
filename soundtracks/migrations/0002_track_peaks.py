# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('soundtracks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='peaks',
            field=models.CommaSeparatedIntegerField(max_length=2000, blank=True),
        ),
    ]
