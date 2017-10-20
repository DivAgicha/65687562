# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-24 12:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20170724_1802'),
    ]

    operations = [
        migrations.RenameField(
            model_name='formstatusset',
            old_name='form_type_contentType',
            new_name='form_type',
        ),
        migrations.AlterField(
            model_name='ccset',
            name='uuid',
            field=models.CharField(default='awl4eh3x-1500899801148-CC', editable=False, max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='clset',
            name='uuid',
            field=models.CharField(default='y5d2sauu-1500899801148-CL', editable=False, max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='ptset',
            name='uuid',
            field=models.CharField(default='gztzu4l2-1500899801132-PT', editable=False, max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='shset',
            name='uuid',
            field=models.CharField(default='qfo3m1hm-1500899801148-SH', editable=False, max_length=40, unique=True),
        ),
    ]
