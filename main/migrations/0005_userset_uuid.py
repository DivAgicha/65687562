# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-24 05:23
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_userset_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='userset',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]