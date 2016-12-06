# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-06 14:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('modules', '0001_initial'),
        ('persons', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('archived', models.BooleanField(default=False, verbose_name='В архиве')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('status', models.CharField(choices=[('h', 'Скрыт'), ('p', 'Опубликован')], default='h', max_length=1, verbose_name='Статус публикации')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(default='', max_length=256, verbose_name='Название образовательной программы')),
                ('chief', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='persons.Person', verbose_name='Руководитель образовательной программы')),
                ('choice_modules', models.ManyToManyField(to='modules.ChoiceModulesPool', verbose_name='Пул модулей по выбору')),
                ('educational_program_trajectories', models.ManyToManyField(to='modules.EducationalProgramTrajectoriesPool', verbose_name='Траектории образовательной программы')),
                ('general_base_modules', models.ManyToManyField(to='modules.GeneralBaseModulesPool', verbose_name='Общепрофессиональные базовые модули')),
            ],
            options={
                'verbose_name': 'программа',
                'verbose_name_plural': 'программы',
            },
        ),
    ]
