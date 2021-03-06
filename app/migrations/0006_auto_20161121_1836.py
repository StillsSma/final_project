# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-21 18:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20161120_1642'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=50)),
                ('quantity', models.IntegerField()),
                ('description', models.CharField(max_length=100)),
                ('grind', models.CharField(choices=[('whole bean', 'WB'), ('fine', '#3'), ('standard', '#7'), ('coarse', '#10')], max_length=20)),
            ],
        ),
        migrations.RenameField(
            model_name='invoice',
            old_name='is_filled',
            new_name='production',
        ),
        migrations.AddField(
            model_name='invoice',
            name='roaster',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='invoice',
            name='shipping',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Invoice'),
        ),
    ]
