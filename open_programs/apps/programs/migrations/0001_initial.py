# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-02 16:16
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('modules', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('choice_pool', models.ManyToManyField(to='modules.ChoicePool', verbose_name='Пул модулей по выбору')),
                ('educational_program_trajectories', models.ManyToManyField(to='modules.ModulesPool', verbose_name='Траектория образовательной программы')),
                ('general_base_modules', models.ManyToManyField(to='modules.Module', verbose_name='Общепрофессиональные базовые модули')),
            ],
        ),
    ]
