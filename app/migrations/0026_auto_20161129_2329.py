# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-30 04:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_invoice_customer_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='customer_discount',
            field=models.CharField(max_length=20),
        ),
    ]
