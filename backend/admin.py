from django.contrib import admin

from backend.models import Coupon, Item, Order, OrderItem

admin.site.register(Order)
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Coupon)
