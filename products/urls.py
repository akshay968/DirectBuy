from django.urls import path,include
from . import views

urlpatterns =  [
    path('',views.index , name='index'),
    path('add_product/', views.add_product, name='add_product'),
    path('sell/',views.sell_page,name='sell'),
    path('product_detail/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('edit_product/<pk>/', views.edit_product, name='edit_product'),
    path('<slug:category_slug>/',views.index , name='products_by_category'),
]
