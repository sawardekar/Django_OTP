# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otpapp', '0003_auto_20171127_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='token_number',
            field=models.IntegerField(max_length=50, verbose_name='token number'),
        ),
    ]
