# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-24 13:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20170724_1806'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formstatusset',
            name='source_id',
        ),
        migrations.AlterField(
            model_name='ccset',
            name='uuid',
            field=models.CharField(default='t9qf66x7-1500901864406-CC', editable=False, max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='clset',
            name='uuid',
            field=models.CharField(default='jhfshftw-1500901864406-CL', editable=False, max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='formstatusset',
            name='status',
            field=models.CharField(choices=[('A', 'Approved'), ('R', 'Rejected'), ('W', 'Waiting')], default='W', max_length=1),
        ),
        migrations.AlterField(
            model_name='ptset',
            name='uuid',
            field=models.CharField(default='armkft0p-1500901864390-PT', editable=False, max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='shset',
            name='uuid',
            field=models.CharField(default='yivkzxu0-1500901864390-SH', editable=False, max_length=40, unique=True),
        ),
    ]