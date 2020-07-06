from django.db import models

from items.models import Variant, Modifier, Item

# Create your models here.

class Order(models.Model):
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200)
    
    @property
    def price(self):
        price = 0
        for i in self.order_items.all():
            price += i.price
        return price

class OrderItem(models.Model):
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL, related_name='order_items')
    item = models.ForeignKey(Item, null=True, on_delete=models.SET_NULL)
    variant = models.ForeignKey(Variant, null=True, on_delete=models.SET_NULL)
    modifiers = models.ManyToManyField(Modifier)
    quantity = models.IntegerField(default=0)

    @property
    def price(self):
        price = self.item.price

        if self.variant:
            price += self.variant.markup
        
        for m in self.modifiers.all():
            price += m.markup
        
        return price