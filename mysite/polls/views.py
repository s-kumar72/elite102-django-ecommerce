from django.shortcuts import render
from django.http import HttpResponse

def store(request):
    context = {}
    return render(request, 'polls/store.html', context)

def cart(request):
    context = {}
    return render(request, 'polls/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'polls/checkout.html', context)