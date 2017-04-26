from django.contrib import admin
from .models import Seller, Item, ItemCategory, AuctionEvent, Bid, Sales
# Register your models here.

admin.site.register(AuctionEvent)
admin.site.register(Bid)
admin.site.register(Item)
admin.site.register(ItemCategory)
admin.site.register(Seller)
admin.site.register(Sales)
# admin.site.register(User)