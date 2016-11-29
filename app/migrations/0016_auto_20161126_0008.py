# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-26 00:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20161124_1949'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.AlterField(
            model_name='profile',
            name='access_level',
            field=models.CharField(choices=[('c', 'Customer Service'), ('r', 'Roasting'), ('p', 'Production'), ('d', 'Delivery')], max_length=20),
        ),
    ]