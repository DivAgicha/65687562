# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-29 16:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_auto_20170728_2036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shset',
            name='board',
        ),
        migrations.AddField(
            model_name='sourceset',
            name='board',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='ccset',
            name='gform_link',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='ccset',
            name='uuid',
            field=models.CharField(default='j030x4dw-1501344195215-CC', editable=False, max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='clset',
            name='gform_link',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='clset',
            name='uuid',
            field=models.CharField(default='l3vme4pm-1501344195211-CL', editable=False, max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='ptset',
            name='gform_link',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='ptset',
            name='uuid',
            field=models.CharField(default='9osnry0r-1501344195202-PT', editable=False, max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='shset',
            name='gform_link',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='shset',
            name='uuid',
            field=models.CharField(default='cf16wsgo-1501344195207-SH', editable=False, max_length=40, unique=True),
        ),
    ]
