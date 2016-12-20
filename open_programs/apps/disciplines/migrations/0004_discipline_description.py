# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disciplines', '0003_discipline_form'),
    ]

    operations = [
        migrations.AddField(
            model_name='discipline',
            name='description',
            field=models.TextField(blank=True, max_length=16384, null=True, verbose_name='Короткое описание'),
        ),
    ]
