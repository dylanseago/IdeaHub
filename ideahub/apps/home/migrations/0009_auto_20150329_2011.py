# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20150326_2327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='idea',
            name='about',
        ),
        migrations.RemoveField(
            model_name='idea',
            name='summary',
        ),
        migrations.AddField(
            model_name='idea',
            name='description',
            field=models.TextField(max_length=4000, default=''),
            preserve_default=False,
        ),
    ]
