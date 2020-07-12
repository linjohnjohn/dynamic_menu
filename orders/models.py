from django.contrib.auth.models import User 
from django.contrib.sessions.models import Session 
from django.db import models

from items.models import Variant, Modifier, Item
from customer.models import Customer
# Create your models here.

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    complete_date = models.DateField(null=True)
    stripe_checkout_id = models.CharField(max_length=200)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.order_items.all()
        return sum([item.total_price for item in orderitems])

    @property
    def get_num_items(self):
        orderitems = self.order_items.all()
        return sum([item.quantity for item in orderitems])

class OrderItem(models.Model):
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL, related_name='order_items')
    item = models.ForeignKey(Item, null=True, on_delete=models.SET_NULL)
    variant = models.ForeignKey(Variant, null=True, on_delete=models.SET_NULL)
    modifiers = models.ManyToManyField(Modifier)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)

    @property
    def unit_price(self):
        price = self.item.price

        if self.variant:
            price += self.variant.markup
        
        for m in self.modifiers.all():
            price += m.markup
        
        return price
    
    @property
    def total_price(self):
        return self.unit_price * self.quantity