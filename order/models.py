from django.db import models
from accounts.models import Account
from products.models import Product,Variant
# Create your models here.

class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100) # this is the total amount paid
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.payment_id


class ShippingAddress(models.Model):
     name=models.CharField(max_length=30, null=True, blank=True)
     mobilenumber= models.CharField(max_length=15)
     country=models.CharField(max_length=30)
     pincode=models.CharField(max_length=10)
     housenumber=models.CharField(max_length=20)
     area=models.CharField(max_length=250)
     town=models.CharField(max_length=10)
     state=models.CharField(max_length=10)
     addresstype=models.BooleanField(default=0)
     user=models.ForeignKey(Account,on_delete=models.CASCADE,related_name='Addresses')
class Order(models.Model):
            user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
            payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
            order_number = models.CharField(max_length=20)
            first_name = models.CharField(max_length=50)
            last_name = models.CharField(max_length=50)
            phone = models.CharField(max_length=15)
            email = models.EmailField(max_length=50)
            address_line_1 = models.CharField(max_length=50)
            address_line_2 = models.CharField(max_length=50, blank=True)
            country = models.CharField(max_length=50)
            state = models.CharField(max_length=50)
            city = models.CharField(max_length=50)
            order_note = models.CharField(max_length=100, blank=True)
            order_total = models.FloatField(default=0)
            tax = models.FloatField(default=2)
            ip = models.CharField(blank=True, max_length=20)
            is_ordered = models.BooleanField(default=False)
            created_at = models.DateTimeField(auto_now_add=True)
            updated_at = models.DateTimeField(auto_now=True)

class OrderedProduct(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE,related_name='order_user')
    vendor = models.ForeignKey(Account, on_delete=models.CASCADE,related_name='order_vendor')
    order= models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    STATUS = (
            ('New','New'),
            ('OrderReceived', 'OrderReceived'),
            ('shipped', 'shipped'),
            ('Completed', 'Completed'),
        )
    status = models.CharField(max_length=100, choices=STATUS, default='OrderReceived')    
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='ordered_product')
    variant = models.ForeignKey(Variant, blank=True,related_name='buyproduct_variant',on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shipping_address=models.ForeignKey(ShippingAddress,on_delete=models.SET_NULL,null=True)
    
    def __str__(self):
        return self.product.product_name    
   