# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-28 15:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_auto_20170728_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ccset',
            name='uuid',
            field=models.CharField(default='8jpp6ilg-1501254375131-CC', editable=False, max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='clset',
            name='uuid',
            field=models.CharField(default='083ff6pe-1501254375115-CL', editable=False, max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='ptset',
            name='uuid',
            field=models.CharField(default='9uxecx1q-1501254375115-PT', editable=False, max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='shset',
            name='uuid',
            field=models.CharField(default='24b9kwxf-1501254375115-SH', editable=False, max_length=40, unique=True),
        ),
    ]
