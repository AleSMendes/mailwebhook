# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2021-11-17 13:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dj_iagentesms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webhookmessagedetail',
            name='codigosms',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
