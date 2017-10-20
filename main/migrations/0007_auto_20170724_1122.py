# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-24 05:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20170724_1054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sourceset',
            name='ehub_id',
            field=models.PositiveIntegerField(editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='userset',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1),
        ),
    ]
