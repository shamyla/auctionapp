# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bidding', '0002_auto_20170302_1601'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuctionEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shipping_method', models.IntegerField(choices=[(1, b'USPS'), (2, b'FedEx'), (3, b'UPS'), (4, b'DHL')])),
                ('shipping_detail', models.CharField(max_length=100, blank=True)),
                ('payment_detail', models.CharField(max_length=200, blank=True)),
                ('start_time', models.DateTimeField(help_text='Format (Hour & Minute are optional): 10/25/2006 14:30')),
                ('end_time', models.DateTimeField(help_text='Format (Hour & Minute are optional): 10/25/2006 14:30')),
                ('starting_price', models.DecimalField(default=Decimal('0.00'), max_digits=5, decimal_places=2)),
                ('shipping_fee', models.DecimalField(default=Decimal('0.00'), max_digits=5, decimal_places=2)),
                ('reserve_price', models.DecimalField(default=Decimal('0.00'), max_digits=5, decimal_places=2, blank=True)),
                ('item', models.ForeignKey(related_name='auction_events', to='bidding.Item')),
                ('winning_bidder', models.ForeignKey(related_name='won_auctions', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(default=Decimal('0.00'), help_text='All bids are final. Price in US dollars.', max_digits=5, decimal_places=2)),
                ('auction_event', models.ForeignKey(related_name='bids', to='bidding.AuctionEvent')),
                ('bidder', models.ForeignKey(related_name='bids', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('payment_status', models.IntegerField(default=1, choices=[(1, b'Processing'), (2, b'Cleared'), (3, b'Disputed'), (4, b'Refunded')])),
                ('invoice_number', models.CharField(unique=True, max_length=200)),
                ('auction_event', models.ForeignKey(related_name='sales', to='bidding.AuctionEvent')),
            ],
        ),
    ]
