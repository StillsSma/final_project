# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-26 16:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20161126_0008'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='customer',
            field=models.CharField(choices=[('1', 'sam'), ('2', 'jack')], default=1, max_length=20),
            preserve_default=False,
        ),
    ]
