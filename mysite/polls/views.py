from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .models import *
from django.http import JsonResponse
import json
import datetime

import stripe
stripe.api_key = 'sk_test_51KtIX5GbVPHpvVe8wwUpSDBxqlRtA38D04boTNLJ9I4tU6ELPVNrHVCN4cYah59HoFY799hdxXZizalb6HgG7fRR00jM3bHGHm'

def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'polls/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items': 0}
    context = {'items':items, 'order':order}
    return render(request, 'polls/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items': 0}
    context = {'items':items, 'order':order}
    return render(request, 'polls/checkout.html', context)

def charge(request):
    if request.method == 'POST':
        print('Data:', request.POST)
    
    amount = int(float(request.POST['cost']))

    customer = stripe.Customer.create(
        email=request.POST['email'],
        name=request.POST['name'],
        source=request.POST['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer,
        amount=amount*100,
        currency='usd',
        description='Payment'
    )
    
    return redirect(reverse('success'))

def successMsg(request):
	return render(request, 'polls/success.html')

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action: ', action)
    print('Product: ', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete=True
        order.save()

        order.get_cart_total = 0

    else:
        print('user is not logged in')
    return JsonResponse('Payment complete', safe=False)
