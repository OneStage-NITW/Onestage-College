# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-04 20:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cap', '0011_platformdetails_picture_folder'),
    ]

    operations = [
        migrations.AddField(
            model_name='platformdetails',
            name='picture_number',
            field=models.IntegerField(default=0),
        ),
    ]
