# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-25 12:25
from __future__ import unicode_literals

from django.db import migrations, models
import falmer.events.models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_event_student_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='brandingperiod',
            name='slug',
            field=models.SlugField(default=falmer.events.models.random_number_as_string),
        ),
    ]
