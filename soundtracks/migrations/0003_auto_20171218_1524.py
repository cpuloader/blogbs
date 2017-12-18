# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('soundtracks', '0002_track_peaks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='peaks',
            field=models.TextField(blank=True),
        ),
    ]
