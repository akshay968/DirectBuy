from django.urls import path
from . import views
urlpatterns=[
 path('', views.messages_page, name='messages'),
 path('<int:vendor_id>',views.contact_vendor,name='contact_vendor'),
 # path('<int:pk>', views.one_to_one, name='onetoone_chat'),

]