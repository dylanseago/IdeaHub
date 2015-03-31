# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0007_project_about'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Idea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('name', models.TextField(max_length=100)),
                ('summary', models.TextField(max_length=250)),
                ('about', models.TextField(max_length=20000)),
                ('tags', models.CharField(max_length=250)),
                ('category', models.ForeignKey(to='home.Category', related_name='ideas')),
                ('poster', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='ideas')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('positive', models.BooleanField(default=True)),
                ('idea', models.ForeignKey(to='home.Idea', related_name='ratings')),
                ('rater', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='ratings_given')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='community',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='community',
            name='subscribers',
        ),
        migrations.RemoveField(
            model_name='funding',
            name='project',
        ),
        migrations.RemoveField(
            model_name='funding',
            name='user',
        ),
        migrations.DeleteModel(
            name='Funding',
        ),
        migrations.RemoveField(
            model_name='project',
            name='community',
        ),
        migrations.DeleteModel(
            name='Community',
        ),
        migrations.RemoveField(
            model_name='project',
            name='initiator',
        ),
        migrations.DeleteModel(
            name='Project',
        ),
    ]
