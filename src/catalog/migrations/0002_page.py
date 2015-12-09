# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-09 09:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('keywords', models.TextField()),
                ('slug', models.SlugField()),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
