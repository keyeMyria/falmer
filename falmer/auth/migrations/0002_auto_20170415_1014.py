# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-15 10:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('falmer_auth', '0001_squashed_0003_magiclinktoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='falmeruser',
            name='name',
            field=models.CharField(default='tbi', max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='falmeruser',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='falmeruser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
