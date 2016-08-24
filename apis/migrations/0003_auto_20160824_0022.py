# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0002_auto_20160823_2353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='email',
            field=models.EmailField(max_length=100, unique=True, null=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='lastName',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='locale',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='picLink',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
