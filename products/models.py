from django.db import models
from django.urls import reverse
from accounts.models import Account
# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to='category/images/', blank=True)
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def get_url(self):
        return reverse('products_by_category',args=[self.slug])
    # def get_url(self):
    #     return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.category_name
class Product(models.Model):
    name =models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    vendor=models.ForeignKey(Account, null=True, blank=True,related_name='vendor_products',on_delete=models.CASCADE)
    category=models.ForeignKey('Category',related_name='products',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/images/', blank=True)
    description=models.TextField(max_length=2000)
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    discount=models.DecimalField(max_digits=5,decimal_places=2,default=0)
    # variants=models.('Variant', on_delete=models.SET_NULL,related_name='product_variants')
    # virtualproduct=models.BooleanField(default=0)
    # productfile=models.FileField()
    def get_url(self):
        return reverse('product_detail', args=[self.slug])
class Variant(models.Model):
    variant_name=models.CharField(max_length=50,null=False)
    product=models.ForeignKey(Product,related_name='Variant',on_delete=models.CASCADE,null=True,blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0)


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.subject
    
# class SubVariation(models.Model): 
#     name=models.CharField(max_length=100)
#     variation=models.ForeignKey(Variation,on_delete=models.CASCADE,related_name='sub_variations')
