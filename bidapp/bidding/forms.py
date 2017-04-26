import datetime
from decimal import Decimal
from django.utils import timezone
from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.forms.util import ValidationError
from django.contrib.admin import widgets as adminwidgets
# from django.contrib.localflavor.us.forms import USPhoneNumberField, USZipCodeField

from .models import Seller, Item, AuctionEvent, Bid, Sales
from .constants import AUCTION_ITEM_STATUS_RUNNING
#
class AuctionSearchForm(forms.Form):
    query = forms.CharField(max_length=200, required=False, label='')
    
    def search(self):
        cleaned_data = self.cleaned_data
        cleaned_query = cleaned_data.get('query', '') 
        if cleaned_query:
            matching_auctions = AuctionEvent.objects.get_current_auctions().filter(Q(item__title__icontains=cleaned_query) | Q(item__description__icontains=cleaned_query))
        else:
            matching_auctions = AuctionEvent.objects.get_current_auctions()
            
        return matching_auctions

class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['paypal_email', 'default_shipping_method', 'default_shipping_detail', 'default_payment_detail']

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'condition', 'category']

    def __init__(self, data=None, seller=None, *args, **kwargs):
        self.seller = seller
        super(ItemForm, self).__init__(data, *args, **kwargs)

    def save(self, force_insert=False, force_update=False, commit=True):
        item = super(ItemForm, self).save(commit=False)
        item.seller = self.seller
        item.save()
        return item

class AuctionEventForm(forms.ModelForm):
    class Meta:
        model = AuctionEvent
        fields = ['shipping_method', 'shipping_detail', 'payment_detail', 'start_time', 'end_time', 'starting_price', 'shipping_fee', 'reserve_price']

    def clean_start_time(self):
        cleaned_data = self.cleaned_data
        cleaned_start_time = cleaned_data.get('start_time')
        if cleaned_start_time < datetime.datetime.now():
            raise ValidationError('Specified time occurs in the past.')
        return cleaned_start_time

    def clean_end_time(self):
        cleaned_data = self.cleaned_data
        cleaned_end_time = cleaned_data.get('end_time')
        if cleaned_end_time < datetime.datetime.now():
            raise ValidationError('Specified time occurs in the past.')
        return cleaned_end_time
    
    def clean(self):
        cleaned_data = self.cleaned_data
        cleaned_start_time = cleaned_data.get('start_time')
        cleaned_end_time = cleaned_data.get('end_time')
        if cleaned_start_time and cleaned_end_time and cleaned_end_time < cleaned_start_time:
            raise ValidationError('End time must be greater than start time.')
        
        cleaned_starting_price = cleaned_data.get('starting_price')
        cleaned_reserve_price = cleaned_data.get('reserve_price')
        if cleaned_starting_price and cleaned_reserve_price and cleaned_reserve_price < cleaned_starting_price:
            raise ValidationError('Reserve price must be higher than starting price.')
        
        return cleaned_data

    def save(self, item=None, force_insert=False, force_update=False, commit=True):
        if not item:
            raise Exception('AuctionEvent save method requires items to be passed in.')
        auction_event = super(AuctionEventForm, self).save(commit=False)
        item.status = AUCTION_ITEM_STATUS_RUNNING
        item.save()
        auction_event.item = item
        auction_event.save()
        return auction_event

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
    
    def __init__(self, data=None, auction_event=None, bidder=None, *args, **kwargs):
        self.auction_event = auction_event
        self.bidder = bidder
        super(BidForm, self).__init__(data, *args, **kwargs)

    def clean_amount(self):
        cleaned_data = self.cleaned_data
        cleaned_amount = cleaned_data.get('amount', Decimal('0.00'))
        if self.auction_event.bids.count():
            if cleaned_amount < self.auction_event.bids.order_by('-amount')[0].amount:
                raise ValidationError('Your bid has to be higher than the current price.')
        return cleaned_amount

    def clean(self):
        cleaned_data = self.cleaned_data
        current_time = timezone.now()
        if current_time > self.auction_event.end_time:
            raise ValidationError('This auction event has expired.')
        return cleaned_data
    
    def save(self, force_insert=False, force_update=False, commit=True):
        bid = super(BidForm, self).save(commit=False)
        bid.auction_event = self.auction_event
        bid.bidder = self.bidder
        bid.save()
        self.auction_event.winning_bidder = bid.bidder
        self.auction_event.save()
        return bid

class PaymentForm(forms.Form):
    paypal_email = forms.EmailField(label='Enter your PayPal email.')

class SalesForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = ['payment_status']
