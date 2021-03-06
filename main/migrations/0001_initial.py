# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-23 15:04
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import main.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CCSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.CharField(max_length=100)),
                ('fee', models.PositiveIntegerField()),
                ('fee_type', models.CharField(choices=[('PM', 'Per Month'), ('PY', 'Per Year'), ('PS', 'Per Sem'), ('PC', 'Per Course')], max_length=2)),
                ('timing', models.CharField(max_length=150)),
                ('number_of_batches', models.PositiveSmallIntegerField(null=True)),
                ('seats_left', models.PositiveIntegerField(default=0)),
                ('gform_link', models.CharField(max_length=200)),
                ('is_link_active', models.BooleanField(default=True)),
                ('last_date_to_apply', models.DateField(default=main.models.get_deadline)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='CLSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.CharField(max_length=100)),
                ('fee', models.PositiveIntegerField()),
                ('fee_type', models.CharField(choices=[('PM', 'Per Month'), ('PY', 'Per Year'), ('PS', 'Per Sem'), ('PC', 'Per Course')], max_length=2)),
                ('timing', models.CharField(max_length=150)),
                ('seats_left', models.PositiveIntegerField(default=0)),
                ('gform_link', models.CharField(max_length=200)),
                ('is_link_active', models.BooleanField(default=True)),
                ('last_date_to_apply', models.DateField(default=main.models.get_deadline)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='FormStatusSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('A', 'Approved'), ('R', 'Rejected'), ('W', 'Waiting')], max_length=1)),
                ('last_modified', models.DateField(auto_now=True)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'ApplicationFormStatus',
                'verbose_name_plural': 'ApplicationFormStatus',
            },
        ),
        migrations.CreateModel(
            name='PTSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.CharField(max_length=100)),
                ('fee', models.PositiveIntegerField()),
                ('fee_type', models.CharField(choices=[('PM', 'Per Month'), ('PY', 'Per Year'), ('PS', 'Per Sem'), ('PC', 'Per Course')], max_length=2)),
                ('timing', models.CharField(max_length=150)),
                ('number_of_batches', models.PositiveSmallIntegerField()),
                ('seats_left', models.PositiveIntegerField(default=0)),
                ('gform_link', models.CharField(max_length=200)),
                ('is_link_active', models.BooleanField(default=True)),
                ('last_date_to_apply', models.DateField(default=main.models.get_deadline)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='SHSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('till_class', models.CharField(max_length=10)),
                ('fee', models.PositiveIntegerField()),
                ('fee_type', models.CharField(choices=[('PM', 'Per Month'), ('PY', 'Per Year'), ('PS', 'Per Sem'), ('PC', 'Per Course')], max_length=2)),
                ('timing', models.CharField(max_length=150)),
                ('board', models.CharField(max_length=50)),
                ('seats_left', models.CharField(default='NULL', max_length=100)),
                ('gform_link', models.CharField(max_length=200)),
                ('is_link_active', models.BooleanField(default=True)),
                ('last_date_to_apply', models.DateField(default=main.models.get_deadline)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='SourceSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ehub_id', models.PositiveIntegerField()),
                ('type', models.CharField(choices=[('PT', 'Private Tuition'), ('SH', 'School'), ('CL', 'College'), ('CC', 'Coaching Centre')], max_length=2)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=20)),
                ('name', models.CharField(default='NULL', max_length=200)),
                ('street', models.CharField(default='NULL', max_length=200)),
                ('city', models.CharField(default='NULL', max_length=200)),
                ('state', models.CharField(default='NULL', max_length=200)),
                ('pincode', models.PositiveIntegerField(null=True)),
                ('contact_num', models.CharField(default='NULL', max_length=13)),
                ('starting_year', models.PositiveSmallIntegerField(null=True)),
                ('affiliation', models.CharField(max_length=100, null=True)),
                ('college_type', models.CharField(max_length=50, null=True)),
                ('average_success_ratio', models.DecimalField(decimal_places=1, max_digits=3, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('rating', models.DecimalField(decimal_places=1, default=10, max_digits=3, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('additional_info', models.TextField()),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Source',
                'verbose_name_plural': 'Sources',
            },
        ),
        migrations.CreateModel(
            name='UserSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(default='NULL', max_length=200)),
                ('password', models.CharField(max_length=20)),
                ('dob', models.DateField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('street', models.CharField(default='NULL', max_length=200)),
                ('city', models.CharField(default='NULL', max_length=200)),
                ('state', models.CharField(default='NULL', max_length=200)),
                ('pincode', models.PositiveIntegerField(default='NULL')),
                ('contact_num', models.CharField(default='NULL', max_length=13)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.AddField(
            model_name='formstatusset',
            name='source_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.SourceSet'),
        ),
        migrations.AddField(
            model_name='formstatusset',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.UserSet'),
        ),
    ]
