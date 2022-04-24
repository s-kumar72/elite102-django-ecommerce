from django.shortcuts import render
from django.http import HttpResponse
from .models import *

def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'polls/store.html', context)

def cart(request):
    context = {}
    return render(request, 'polls/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'polls/checkout.html', context)