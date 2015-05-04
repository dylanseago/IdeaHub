# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20150330_1857'),
    ]

    operations = [
        migrations.RenameField(
            model_name='idea',
            old_name='creator',
            new_name='user',
        ),
    ]
