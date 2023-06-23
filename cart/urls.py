from django.urls import path
from . import views
urlpatterns=[
 path('',views.index,name='cart'),
 path('checkout/',views.checkout,name='checkout'),
 path('addcart/',views.add_cart,name='addcart'),
#  path('removecart/',views.,name='removecart'),


]