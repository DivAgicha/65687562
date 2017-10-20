# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-31 05:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20170729_2133'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ccset',
            options={'verbose_name': 'CoachingCentre Form', 'verbose_name_plural': 'CoachingCentre Forms'},
        ),
        migrations.AlterModelOptions(
            name='clset',
            options={'verbose_name': 'College Form', 'verbose_name_plural': 'College Forms'},
        ),
        migrations.AlterModelOptions(
            name='ptset',
            options={'verbose_name': 'PrivateTuition Form', 'verbose_name_plural': 'PrivateTuition Forms'},
        ),
        migrations.AlterModelOptions(
            name='shset',
            options={'verbose_name': 'School Form', 'verbose_name_plural': 'School Forms'},
        ),
        migrations.AlterField(
            model_name='ccset',
            name='uuid',
            field=models.CharField(default='g8nydevd-1501478673339-CC', editable=False, max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='clset',
            name='uuid',
            field=models.CharField(default='sq8kzbsg-1501478673337-CL', editable=False, max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='ptset',
            name='uuid',
            field=models.CharField(default='gonib97n-1501478673332-PT', editable=False, max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='shset',
            name='uuid',
            field=models.CharField(default='6oni148t-1501478673334-SH', editable=False, max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='sourceset',
            name='password',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='userset',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]