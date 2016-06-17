# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-12 18:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0028_merge'),
        ('surveys', '0002_allow_multiple_submissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveysIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
