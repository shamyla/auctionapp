# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bidding', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('condition', models.IntegerField(choices=[(1, b'Used'), (2, b'Used Like New'), (3, b'New')])),
                ('status', models.IntegerField(default=1, choices=[(1, b'Idle'), (2, b'Running'), (3, b'On Hold'), (4, b'Sold'), (5, b'Expired'), (6, b'Disputed')])),
            ],
        ),
        migrations.CreateModel(
            name='ItemCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('parent', models.ForeignKey(blank=True, to='bidding.ItemCategory', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.ForeignKey(related_name='auction_items', to='bidding.ItemCategory'),
        ),
        migrations.AddField(
            model_name='item',
            name='seller',
            field=models.ForeignKey(related_name='auction_items', to=settings.AUTH_USER_MODEL),
        ),
    ]
