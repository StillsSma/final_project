# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-27 23:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_invoice_delivery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='item',
            field=models.CharField(max_length=100),
        ),
    ]
