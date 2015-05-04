# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_auto_20150407_1321'),
    ]

    operations = [
        migrations.RenameField(
            model_name='idea',
            old_name='user',
            new_name='creator',
        ),
    ]
