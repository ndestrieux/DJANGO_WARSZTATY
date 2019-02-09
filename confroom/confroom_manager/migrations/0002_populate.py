# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from confroom_manager.models import *


def populate(apps, schema_editor):
    Room.objects.create(name="Paris", capacity=5, have_projector=False)
    Room.objects.create(name="Warsaw", capacity=8, have_projector=True)


class Migration(migrations.Migration):

    dependencies = [
        ('confroom_manager', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate),
    ]