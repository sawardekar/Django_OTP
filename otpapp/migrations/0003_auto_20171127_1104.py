# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otpapp', '0002_auto_20171124_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(help_text='Field to save the phone number of the user.', max_length=15, verbose_name='phone number'),
        ),
    ]
