# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-03 13:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('matte', '0002_remoteimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='MSLStudentGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msl_description', models.TextField(default='')),
                ('msl_group_id', models.IntegerField(unique=True)),
                ('msl_image_url', models.URLField(default='')),
                ('last_sync', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='MSLStudentGroupCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='StudentGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='mslstudentgroup',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentgroups.MSLStudentGroupCategory'),
        ),
        migrations.AddField(
            model_name='mslstudentgroup',
            name='group',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='studentgroups.StudentGroup'),
        ),
        migrations.AddField(
            model_name='mslstudentgroup',
            name='msl_image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='matte.MatteImage'),
        ),
    ]