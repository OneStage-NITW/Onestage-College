# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-04 19:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cap', '0010_auto_20151230_0604'),
    ]

    operations = [
        migrations.AddField(
            model_name='platformdetails',
            name='picture_folder',
            field=models.CharField(max_length=180, null=True),
        ),
    ]
