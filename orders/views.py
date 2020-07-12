from django.shortcuts import render, reverse, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login, logout as django_logout, logout
from django.contrib.sessions.models import Session

import stripe
import json, datetime
from items.models import Item, Variant, Modifier, Category
from customer.models import Customer
from .models import OrderItem, Order
from .forms import CreateUserForm
from .stripe import createCheckoutSession
import pdb

def login(request):
    if request.method == 'GET':
        cart_entries, order = cart_details(request)
        form = CreateUserForm()
        context = {'order': order}
        return render(request, 'orders/login.html', context)
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            django_login(request, user)
            messages.success(request, 'Welcome back %s' % user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR Password is Incorrect')
            return render(request, 'orders/login.html')

def logout(request):
    django_logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('login')

def register(request):
    if request.method == 'GET':
        order, cart_entries = cart_details(request)
        form = CreateUserForm()
        context = {'form': form, 'order': order}
        return render(request, 'orders/register.html', context)
    elif request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            django_login(request, user)
            messages.success(request, 'Account was created for ' + user.email)
            return redirect('home')
        else:
            context = {'form': form}
            return render(request, 'orders/register.html', context)


def menu(request):
    cartEntries, order = cart_details(request)
    categories = Category.objects.all()
    context = { 'categories': categories, 'cartEntries': cartEntries, 'order': order}
    return render(request, 'orders/menu.html', context)

def checkout(request):
    if request.method == 'GET':
        cartEntries, order = cart_details(request)
        # intent = createIntent(order.get_cart_total)
        session = createCheckoutSession(request, order, cartEntries)
        context = {'cartEntries': cartEntries, 'order': order, 'session_id': session.id}
        return render(request, 'orders/checkout.html', context)
    elif request.method == 'POST':
        transaction_id = datetime.datetime.now().timestamp()
        data = json.loads(request.body)

        if request.user.is_authenticated:
            pass
        else:
            name = data['form']['name']
            email = data['form']['email']
            phone = data['form']['phone']

            cartEntries, order = cart_details(request)
            customer, created = Customer.objects.get_or_create(
                email=email,
            )

            customer.phone = phone
            customer.name = name
            customer.save()

            order = Order.objects.create(
                customer=customer,
                complete=False
            )

            for entry in cartEntries:
                item = entry['item']
                variant = entry['variant']
                modifiers = entry['modifiers']
                quantity = entry['quantity']

                orderItem = OrderItem.objects.create(
                    order=order,
                    item=item,
                    variant=variant,
                    quantity=quantity
                )

                for m in modifiers:
                    orderItem.modifiers.add(m)

            total = float(data['form']['total'])    
            order.transaction_id = transaction_id

            if total == order.get_cart_total:
                order.complete = True
            order.save()

            return JsonResponse('Payment complete', safe=False)

def checkout_success(request):
    return render(request, 'orders/checkout_success.html')

def cart(request):
    cartEntries, order = cart_details(request)
    context = {'cartEntries': cartEntries, 'order': order}
    return render(request, 'orders/cart.html', context)

def add_to_cart(request, id):
    if request.method == 'GET':
        cartEntries, order = cart_details(request)
        item = Item.objects.get(pk=id)
        context = { 'item': item, 'cartEntries': cartEntries, 'order': order }
        return render(request, 'orders/add.html', context)
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            if not request.session.session_key:
                request.session.create()
            session_id = request.session.session_key
            print(session_id)
            session = Session.objects.get(session_key=session_id)
            order, created = Order.objects.get_or_create(session=session, complete=False)
        else:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)

        data = json.loads(request.body)
        variant = data.get('variant', 'regular')
        modifiers = data.get('modifiers', [])
        quantity = data.get('quantity', 1)

        item = Item.objects.get(id=id)
        orderItem = OrderItem.objects.create(order=order, item=item, quantity=quantity)

        if variant != 'regular':
            variant = Variant.objects.get(id=variant)
            orderItem.variant = variant
        
        for modifier in modifiers:
            modifier = Modifier.objects.get(id=modifier)
            orderItem.modifiers.add(modifier)

        orderItem.save()

        return JsonResponse("Added to Cart", safe=False)
    
def update_cart(request):
    data = json.loads(request.body)
    orderItem = data.get('orderItem', None)
    action = data.get('action', 'add')
    orderItem = OrderItem.objects.filter(id=orderItem)
    
    if orderItem.exists():
        orderItem = orderItem.first()
        
        if action == 'add':
            orderItem.quantity += 1
            orderItem.save()
        elif action == 'remove':
            orderItem.quantity -= 1
            if orderItem.quantity <= 0:
                orderItem.delete()
            else:
                orderItem.save()
        return JsonResponse("Cart Updated", safe=False)

def cart_details(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        cartEntries = order.order_items.all()
    else:
        if not request.session.session_key:
            request.session.create()
        session_id = request.session.session_key
        print(session_id)
        session = Session.objects.get(session_key=session_id)
        order, created = Order.objects.get_or_create(session=session, complete=False)
        cartEntries = order.order_items.all()
        # cart = json.loads(request.COOKIES.get('cart', "[]"))
        # cartEntries = []
        # cartTotal = 0
        # numItems = 0
        # for entry in cart:
        #     item = entry.get('item', None)
        #     if item == None:
        #         continue
        #     item = Item.objects.filter(pk=item)
        #     if item.exists():
        #         item = item.first()
        #     else:
        #         continue

        #     variant = entry.get('variant', 'regular')
        #     if variant != 'regular':
        #         variant = Variant.objects.filter(pk=variant)
        #         if variant.exists():
        #             variant = variant.first()
        #         else:
        #             continue
        #     else:
        #         variant = None

        #     modifiers = entry.get('modifiers', [])
        #     modifiers = Modifier.objects.filter(pk__in=modifiers)

        #     price = item.price

        #     if variant:
        #         price += variant.markup
            
        #     for m in modifiers:
        #         price += m.markup

        #     quantity = int(entry.get('quantity', 1))
        #     total_price = price * quantity

        #     numItems += quantity

        #     cartEntries.append({
        #         'item': item,
        #         'variant': variant,
        #         'modifiers': modifiers,
        #         'unit_price': price,
        #         'total_price': price,
        #         'quantity': quantity
        #     })
        #     cartTotal += total_price
        
        # order = { 'get_cart_total': cartTotal, 'get_num_items': numItems }
    return cartEntries, order