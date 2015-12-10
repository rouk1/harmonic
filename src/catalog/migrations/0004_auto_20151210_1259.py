# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-10 12:59
from __future__ import unicode_literals

import colorfield.fields
from django.db import migrations, models
import harmonic.fields


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_section_title_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('bio', harmonic.fields.MarkdownField()),
                ('bio_fr', harmonic.fields.MarkdownField(null=True)),
                ('bio_en', harmonic.fields.MarkdownField(null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='section',
            name='title_color',
            field=colorfield.fields.ColorField(default='#000000', max_length=10),
        ),
    ]
