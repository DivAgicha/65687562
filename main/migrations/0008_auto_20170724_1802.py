# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-24 12:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('main', '0007_auto_20170724_1122'),
    ]

    operations = [
        migrations.AddField(
            model_name='ccset',
            name='uuid',
            field=models.CharField(default='3lqv8xvy-1500899492887-CC', editable=False, max_length=40, unique=True),
        ),
        migrations.AddField(
            model_name='clset',
            name='uuid',
            field=models.CharField(default='h3wo07cu-1500899492887-CL', editable=False, max_length=40, unique=True),
        ),
        migrations.AddField(
            model_name='formstatusset',
            name='form_type_contentType',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='formstatusset',
            name='object_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ptset',
            name='uuid',
            field=models.CharField(default='i6964p7b-1500899492887-PT', editable=False, max_length=40, unique=True),
        ),
        migrations.AddField(
            model_name='shset',
            name='uuid',
            field=models.CharField(default='1ep0xrjc-1500899492887-SH', editable=False, max_length=40, unique=True),
        ),
    ]
