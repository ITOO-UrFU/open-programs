# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-12 22:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='component',
            name='dev_description',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='component',
            name='json',
            field=jsonfield.fields.JSONField(blank=True, null=True, verbose_name='JSON'),
        ),
        migrations.AlterField(
            model_name='component',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cms.ComponentType'),
        ),
        migrations.AlterField(
            model_name='component',
            name='weight',
            field=models.IntegerField(default=0, verbose_name='Вес'),
        ),
        migrations.AlterField(
            model_name='container',
            name='dev_description',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='container',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cms.ContainerType'),
        ),
        migrations.AlterField(
            model_name='container',
            name='weight',
            field=models.IntegerField(default=0, verbose_name='Вес'),
        ),
    ]
