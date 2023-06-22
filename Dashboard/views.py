from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from order.models import Order,OrderedProduct
from accounts.models import Account
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.http import HttpResponse
from order.models import Payment
from django.db.models import Q

# from cart.views import _cart_id
# from carts.models import Cart, CartItem
import requests

@login_required(login_url = 'login')
def dashboard(request):
    # return HttpResponse('dashboard')
    user=Account(id=request.user.id)
    orders = Order.objects.order_by('-created_at').filter(user=user, is_ordered=True)
    print(request.user)
    orders_count = orders.count()
    print(orders_count)
    user = request.user
  
    context = {
        'orders_count': orders_count,
        'userprofile': user,
    }
    return render(request, 'dashboard/dashboard.html', context)



@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'dashboard/my_orders.html', context)
def sold_products(request):
    orders = OrderedProduct.objects.filter(vendor=request.user, ordered=True).order_by('-created_at')
    context = {
        'sold_products': orders,
    }
    return render(request, 'dashboard/sold_products.html', context)
def ordered_products(request):
    orders = OrderedProduct.objects.filter(user=request.user, ordered=True).order_by('-created_at')
    context = {
         'ordered_products': orders,
    }
    return render(request, 'dashboard/ordered_products.html', context)

def transactions(request):
    transactions = Payment.objects.filter(Q(user=request.user) | Q(vendor=request.user))
    context = {
         'payments': transactions,
    }
    return render(request, 'dashboard/transactions.html', context)
# @login_required(login_url='login')
# def order_detail(request, order_id):
#     order_detail = OrderProduct.objects.filter(order__order_number=order_id)
#     order = Order.objects.get(order_number=order_id)
#     subtotal = 0
#     for i in order_detail:
#         subtotal += i.product_price * i.quantity

#     context = {
#         'order_detail': order_detail,
#         'order': order,
#         'subtotal': subtotal,
#     }
#     return render(request, 'accounts/order_detail.html', context)

@login_required(login_url='login')
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    order_detail = OrderedProduct.objects.filter(order=order)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity

    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'dashboard/order_detail.html', context)