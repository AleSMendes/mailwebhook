# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2021-11-19 13:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dj_iagentesms', '0003_webhookmessagedetail_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webhookmessagedetail',
            name='shortcode',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
