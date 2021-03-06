# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-23 23:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20161123_2123'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('given_name', models.CharField(max_length=100)),
                ('company_name', models.CharField(max_length=100)),
                ('email_address', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=12)),
                ('note', models.TextField()),
            ],
        ),
    ]
