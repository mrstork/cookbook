# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 19:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20170327_1910'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipeinstruction',
            name='order',
        ),
    ]
