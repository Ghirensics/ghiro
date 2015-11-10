# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('analyses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hash',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('cipher', models.CharField(default=b'MD5', max_length=6, db_index=True, choices=[(b'sha1', b'SHA1'), (b'sha224', b'SHA224'), (b'sha384', b'SHA384'), (b'crc32', b'CRC32'), (b'sha256', b'SHA256'), (b'sha512', b'SHA512'), (b'md5', b'MD5')])),
                ('public', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('matches', models.ManyToManyField(to='analyses.Analysis', blank=True)),
                ('owner', models.ForeignKey(related_name='owned_hashes', editable=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='hash',
            name='list',
            field=models.ForeignKey(editable=False, to='hashes.List'),
        ),
    ]
