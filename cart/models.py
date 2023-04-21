from django.db import models
from accounts.models import Account
from products.models import Product,Variant
# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    variant = models.ForeignKey(Variant, blank=True,related_name='cartitem_varaint',on_delete=models.SET_NULL,null=True)    
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True,related_name='cart_items')
    quantity = models.IntegerField()
    price=models.IntegerField()
    def sub_total(self):
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product