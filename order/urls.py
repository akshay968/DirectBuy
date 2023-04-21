from django.urls import path
from . import views
urlpatterns=[
 path('placeorder/',views.placeorder,name='placeorder'),
 path('payment/',views.paymenthandler,name='paymenthandler'),

]