# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='activation_key',
            field=models.CharField(default=b'key', max_length=40, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='key_expires',
            field=models.DateTimeField(default=datetime.date.today),
            preserve_default=True,
        ),
    ]
