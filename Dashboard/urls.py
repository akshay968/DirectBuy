from django.urls import path,include
from . import views
urlpatterns = [
 path('',view=views.dashboard,name='dashboard'),
 path('orders/',view=views.my_orders,name='orders'),
 path('orderdetail/<int:order_id>/',view=views.order_detail,name='orderdetail'),
 path('OrderedProducts/',view=views.ordered_products,name='OrderedProducts'),
 path('SoldProducts/',view=views.sold_products,name='SoldProducts'),
 path('transactions/',view=views.transactions,name='transactions'),
 path('submitreview/',view=views.submit_rating,name='submitreview'),

 path('change_password/',view=views.dashboard,name='change_password'),
]
