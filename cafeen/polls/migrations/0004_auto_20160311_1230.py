# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-11 11:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_events_waregroups'),
    ]

    operations = [
        migrations.CreateModel(
            name='Waresingroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RenameField(
            model_name='events',
            old_name='eventid',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='waregroups',
            old_name='wgid',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='wares',
            old_name='wareid',
            new_name='id',
        ),
        migrations.AddField(
            model_name='waresingroup',
            name='ware',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Wares'),
        ),
        migrations.AddField(
            model_name='waresingroup',
            name='waregroup',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Waregroups'),
        ),
    ]