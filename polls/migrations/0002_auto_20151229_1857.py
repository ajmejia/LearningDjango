# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='poll',
            options={'permissions': (('vote', 'Can vote on polls'), ('view_results', 'Can watch results'))},
        ),
    ]
