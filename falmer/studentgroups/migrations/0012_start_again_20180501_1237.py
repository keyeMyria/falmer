# Generated by Django 2.0.2 on 2018-05-01 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('studentgroups', '0010_auto_20180301_2123'),
    ]

    operations = [
        migrations.DeleteModel(name='GroupAwarded'),
        migrations.DeleteModel(name='Award'),
        migrations.DeleteModel(name='AwardAuthority'),
    ]
