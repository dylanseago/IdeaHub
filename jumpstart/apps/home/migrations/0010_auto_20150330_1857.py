# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20150329_2011'),
    ]

    operations = [
        migrations.RenameField(
            model_name='idea',
            old_name='poster',
            new_name='creator',
        ),
        migrations.AlterField(
            model_name='idea',
            name='tags',
            field=models.CharField(default='', max_length=250, blank=True),
            preserve_default=True,
        ),
    ]
