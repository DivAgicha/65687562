# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-24 05:24
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_userset_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userset',
            name='email',
            field=models.EmailField(max_length=254, unique=True, validators=[django.core.validators.EmailValidator]),
        ),
    ]
