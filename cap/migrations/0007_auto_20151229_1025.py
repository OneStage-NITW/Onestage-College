# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-29 10:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cap', '0006_organisation_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platform',
            name='organisations',
            field=models.ManyToManyField(blank=True, null=True, related_name='platform_orgs', to='cap.Organisation'),
        ),
    ]