# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('userid', models.AutoField(serialize=False, primary_key=True)),
                ('email', models.EmailField(unique=True, max_length=100)),
                ('fbId', models.EmailField(unique=True, max_length=100)),
                ('acessToken', models.EmailField(unique=True, max_length=100)),
                ('firstName', models.CharField(max_length=40)),
                ('lastName', models.CharField(max_length=40)),
                ('gender', models.CharField(max_length=10)),
                ('locale', models.CharField(max_length=10)),
                ('picLink', models.CharField(max_length=10)),
                ('fbProfileLink', models.CharField(max_length=100)),
            ],
        ),
    ]
