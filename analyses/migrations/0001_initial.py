# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image_id', models.CharField(max_length=72, editable=False)),
                ('thumb_id', models.CharField(max_length=72, null=True, editable=False, blank=True)),
                ('file_name', models.CharField(max_length=255, editable=False)),
                ('analysis_id', models.CharField(db_index=True, max_length=24, null=True, editable=False, blank=True)),
                ('state', models.CharField(default=b'W', max_length=1, editable=False, db_index=True, choices=[(b'W', b'Waiting'), (b'C', b'Completed'), (b'P', b'Processing'), (b'Q', b'Queued'), (b'F', b'Failed')])),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('completed_at', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'get_latest_by': 'created_at',
            },
        ),
        migrations.CreateModel(
            name='AnalysisMetadataDescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(unique=True, max_length=255, editable=False, db_index=True)),
                ('description', models.TextField(editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('state', models.CharField(default=b'O', max_length=1, editable=False, db_index=True, choices=[(b'O', b'Open'), (b'C', b'Closed')])),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(related_name='owned_cases', editable=False, to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(related_name='cases', db_index=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'get_latest_by': 'created_at',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('analysis', models.ForeignKey(related_name='comments', editable=False, to='analyses.Analysis')),
                ('owner', models.ForeignKey(related_name='owned_comments', editable=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('analysis', models.ForeignKey(related_name='favorites', editable=False, to='analyses.Analysis')),
                ('owner', models.ForeignKey(related_name='owned_favorites', editable=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('analysis', models.ManyToManyField(to='analyses.Analysis')),
                ('owner', models.ForeignKey(related_name='owned_tags', editable=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='analysis',
            name='case',
            field=models.ForeignKey(related_name='images', on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to='analyses.Case', null=True),
        ),
        migrations.AddField(
            model_name='analysis',
            name='owner',
            field=models.ForeignKey(related_name='owned_images', editable=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
