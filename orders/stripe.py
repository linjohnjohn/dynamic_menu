from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

import json
import stripe

from .models import Order

stripe.api_key = 'sk_test_51H3NC3LegJFM7u3CmJgAZRSyTYlW5foBWOKatWPqCEHZSWZwnE94Y9pns4m1eVR8sqwshv4knkJf8HwHuxKvE5l900YLLGA2yg'

# def createIntent(dollarAmount):
#     return stripe.PaymentIntent.create(
#         amount=int(dollarAmount * 100),
#         currency='usd',
#         # Verify your integration in this guide by including this parameter
#         metadata={'integration_check': 'accept_a_payment'},
#     )

def createCheckoutSession(order, cartEntries):
    line_items = []
    for entry in cartEntries:
        modifier_names = [m.name for m in entry.modifiers.all()]
        if entry.variant:
            details = [entry.variant.name] + modifier_names
        else:
            details = ['Regular'] + modifier_names
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': entry.item.name,
                    'description': ', '.join(details)
                },
                'unit_amount': int(entry.unit_price * 100)
            },
            'quantity': entry.quantity
        })
    session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=line_items,
    metadata={
        'order-id': order.id
    },
    mode='payment',
    success_url='http://localhost:8001/checkout_success/',
    cancel_url='http://localhost:8001/checkout/',
    )
    
    return session

@csrf_exempt
def webhook(request):
    payload = request.body
    event = None
    print(payload)
    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object # contains a stripe.PaymentIntent
        print('PaymentIntent was successful!')
    elif event.type == 'payment_method.attached':
        payment_method = event.data.object # contains a stripe.PaymentMethod
        print('PaymentMethod was attached to a Customer!')
        # ... handle other event types
    elif event.type == 'checkout.session.completed':
        session = event['data']['object']
        order_id = session['metadata']['order-id']
        order = Order.objects.get(id=order_id)
        order.complete = True
        order.save()
        print(session)
    else:
        # Unexpected event type
        return HttpResponse(status=400)

    return HttpResponse(status=200)