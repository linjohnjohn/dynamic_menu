from django.contrib import admin

# Register your models here.
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra=0

class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline
    ]

admin.site.register(Order)
admin.site.register(OrderItem)
