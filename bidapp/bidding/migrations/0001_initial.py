# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('paypal_email', models.EmailField(max_length=254)),
                ('default_shipping_method', models.IntegerField(default=1, choices=[(1, b'USPS'), (2, b'FedEx'), (3, b'UPS'), (4, b'DHL')])),
                ('default_shipping_detail', models.CharField(max_length=100, null=True, blank=True)),
                ('default_payment_detail', models.CharField(max_length=200, null=True, blank=True)),
                ('user', models.OneToOneField(related_name='seller', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
