from django.shortcuts import render, reverse, redirect
from items.models import Item, Variant, Modifier
from .models import OrderItem, Order


def cart(request):
    items, order, cartItems = cart_details(request)
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'orders/cart.html', context)

def add_to_cart(request, id):
    if request.method == 'GET':
        item = Item.objects.get(pk=id)
        context = { 'item': item }
        return render(request, 'orders/add.html', context)
    elif request.method == 'POST':
        print('hi')
        data = request.POST
        print(request.POST)
        variant = data.get('variant', 'regular')
        modifiers = data.get('modifiers', [])
            
        item = Item.objects.get(id=id)
        order, created = Order.objects.get_or_create(complete=False)

        orderItem, created = OrderItem.objects.create(order=order, item=item)

        if variant != 'regular':
            variant = Variant.objects.get(id=variant)
            orderItem.variant = variant
        
        for modifier in modifiers:
            modifier = Modifier.objects.get(id=modifier)
            orderItem.modifiers.add(modifier)
        
        orderItem.quantity += 1

        orderItem.save()

        return redirect(reverse('menu'))

# def cart_details(request):
