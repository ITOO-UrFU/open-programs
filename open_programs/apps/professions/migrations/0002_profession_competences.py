# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competences', '0001_initial'),
        ('professions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profession',
            name='competences',
            field=models.ManyToManyField(to='competences.Competence', verbose_name='Компетенции'),
        ),
    ]
